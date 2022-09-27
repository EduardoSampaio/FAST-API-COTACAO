from fastapi import APIRouter
from services.cotacaoService import *

routerCotacao = APIRouter(
  prefix="/cotacao",
  tags=["cotacao"],
  dependencies=[],
  responses={404: {"description": "Not found"}},
)


@routerCotacao.get('/acoes/')
def acoes(skip: int = 0, limit: int = 10):
  data = get_acoes()
  return data[skip:skip+limit]

@routerCotacao.get('/fiis/')
def getFiis(skip: int = 0, limit: int = 10):
  data = getValuesFundos()
  return data[skip:skip+limit]


@routerCotacao.get('/{ticker}/current')
def getTicketCurrent(ticker):
  return getByTicketCurrent(ticker)

@routerCotacao.get('/{ticker}/data-inicio/{inicio}/data-fim/{fim}')
def getByIntervalo(ticker,inicio,fim):
  return getTicketByInterval(ticker,inicio,fim)

@routerCotacao.get('/moedas')
def getMoedas():
  return getMoedaCotacao()

