from fastapi import FastAPI, HTTPException
import httpx
import re

app = FastAPI()

cep_cache = {}

def validar_cep(cep: str) -> bool:
    return re.fullmatch(r"\d{5}-?\d{3}", cep) is not None

async def consultar_cep_externo(cep: str) -> dict:
    url = f"https://viacep.com.br/ws/{cep}/json/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=404, detail="CEP não encontrado")

@app.get("/cep/{cep}")
async def buscar_cep(cep: str):
    cep = cep.replace("-", "")
    
    if not validar_cep(cep):
        raise HTTPException(status_code=400, detail="Formato de CEP inválido")
    
    if cep in cep_cache:
        return {"data": cep_cache[cep], "cache": True}
    
    dados_cep = await consultar_cep_externo(cep)
    cep_cache[cep] = dados_cep
    
    return {"data": dados_cep, "cache": False}

@app.get("/cache/{cep}")
async def consultar_cache(cep: str):
    cep = cep.replace("-", "")
    
    if cep in cep_cache:
        return {"data": cep_cache[cep]}
    else:
        raise HTTPException(status_code=404, detail="CEP não encontrado no cache")

@app.get("/cache")
async def consultar_todo_cache():
    return {"data": cep_cache}


@app.get("/frete/{cep_origem}/{cep_destino}")
async def calcular_frete(cep_origem: str, cep_destino: str):
    if not (validar_cep(cep_origem) and validar_cep(cep_destino)):
        raise HTTPException(status_code=400, detail="Formato de CEP inválido")
    
    distancia = abs(int(cep_origem[:5]) - int(cep_destino[:5]))  
    
    valor_frete = distancia * 0.1  
    
    return {"cep_origem": cep_origem, "cep_destino": cep_destino, "distancia": distancia, "valor_frete": valor_frete}