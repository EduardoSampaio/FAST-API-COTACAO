from fastapi import FastAPI
from routers.cotacaoRouter import routerCotacao

app = FastAPI()

app.include_router(routerCotacao)

@app.get('/')
def ok():
  return "API RUNNING V1"

