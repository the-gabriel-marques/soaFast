from fastapi import APIRouter, HTTPException
from controller.controller_cep import CepController

cep_control = CepController(cep_cache={})
router = APIRouter()

@router.get("/frete/{cep_origem}/{cep_destino}")
async def calcular_frete(cep_origem: str, cep_destino: str):
    if not cep_control.validar_cep(cep_origem) and cep_control.validar_cep(cep_destino):
        raise HTTPException(status_code=400, detail="Formato de CEP inválido")
    
    distancia = abs(int(cep_origem[:5]) - int(cep_destino[:5]))  
    
    valor_frete = distancia * 0.1  
    
    return {"cep_origem": cep_origem, "cep_destino": cep_destino, "distancia": distancia, "valor_frete": valor_frete}

