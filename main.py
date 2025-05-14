from fastapi import FastAPI
from router.router_cep import router as router_cep
from router.router_frete import router as router_frete

app = FastAPI()
app = FastAPI(debug=True)

app.include_router(router_cep, prefix="/api", tags=["cep"])
app.include_router(router_frete, prefix="/api", tags=["frete"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)