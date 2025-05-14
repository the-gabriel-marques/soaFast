from fastapi import APIRouter, HTTPException
from controller.controller_cep import CepController

cep_control = CepController(cep_cache={})
router = APIRouter()

@router.get("/cep/{cep}")
async def buscar_cep(cep: str):
    cep = cep.replace("-", "")
    
    if not cep_control.validar_cep(cep):
        raise HTTPException(status_code=400, detail="Formato de CEP inválido")
    
    if cep in cep_control.cep_cache:
        return {"data":cep_control.cep_cache[cep], "cache": True}
    
    dados_cep = await cep_control.consultar_cep_externo(cep)
    cep_control.cep_cache[cep] = dados_cep
    
    return {"data": dados_cep, "cache": False}

@router.get("/cache/{cep}")
async def consultar_cache(cep: str):
    cep = cep.replace("-", "")
    
    if cep in cep_control.cep_cache:
        return {"data":cep_control.cep_cache[cep]}
    else:
        raise HTTPException(status_code=404, detail="CEP não encontrado no cache")

@router.get("/cache")
async def consultar_todo_cache():
    return {"data":cep_control.cep_cache}


