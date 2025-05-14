#importa model
from fastapi import HTTPException
from httpx import AsyncClient
import re

class CepController:
    def __init__(self, cep_cache: dict):
        self.cep_cache = cep_cache

    def validar_cep(self, cep: str) -> bool:
        return re.fullmatch(r"\d{5}-?\d{3}", cep) is not None

    async def consultar_cep_externo(self, cep: str) -> dict:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        async with AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=404, detail="CEP não encontrado")