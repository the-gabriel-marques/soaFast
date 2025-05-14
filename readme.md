1º clonar o projeto e entrar na pasta do projeto  e executar o comando abaixo
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
e
```
python -m venv fastapi_env
```
2º
Windows: 
```
fastapi_env\Scripts\activate
```
macOS/Linux: 
```
source fastapi_env/bin/activate
```
3º
```
pip install fastapi uvicorn
```
e 
```
pip install httpx
```

4º
```
pip freeze > requirements.txt
uvicorn main:app --reload
```
5º (instalar em outro local) passo 1 e passo 2 
pip install -r requirements.txt
