from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
from importlib.metadata import requires 
import requests
from lxml.html import fragment_fromstring
from pandas_datareader import data as web

import http.cookiejar
import urllib.parse
import urllib.request
import re as regex

def get_acoes():
    url = 'http://www.fundamentus.com.br/resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]
    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min': '',
            'pl_max': '',
            'pvp_min': '',
            'pvp_max': '',
            'psr_min': '',
            'psr_max': '',
            'divy_min': '',
            'divy_max': '',
            'pativos_min': '',
            'pativos_max': '',
            'pcapgiro_min': '',
            'pcapgiro_max': '',
            'pebit_min': '',
            'pebit_max': '',
            'fgrah_min': '',
            'fgrah_max': '',
            'firma_ebit_min': '',
            'firma_ebit_max': '',
            'margemebit_min': '',
            'margemebit_max': '',
            'margemliq_min': '',
            'margemliq_max': '',
            'liqcorr_min': '',
            'liqcorr_max': '',
            'roic_min': '',
            'roic_max': '',
            'roe_min': '',
            'roe_max': '',
            'liq_min': '',
            'liq_max': '',
            'patrim_min': '',
            'patrim_max': '',
            'divbruta_min': '',
            'divbruta_max': '',
            'tx_cresc_rec_min': '',
            'tx_cresc_rec_max': '',
            'setor': '',
            'negociada': 'ON',
            'ordem': '1',
            'x': '28',
            'y': '16'}
    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')
    pattern = regex.compile('<table id="resultado".*</table>', regex.DOTALL)
    content = regex.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = OrderedDict()
    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update({rows.getchildren()[0][0].getchildren()[0].text: {'Cotacao': todecimal(rows.getchildren()[1].text),
                                                                        'P/L': todecimal(rows.getchildren()[2].text),
                                                                        'P/VP': todecimal(rows.getchildren()[3].text),
                                                                        'PSR': todecimal(rows.getchildren()[4].text),
                                                                        'DY': todecimal(rows.getchildren()[5].text),
                                                                        'P/Ativo': todecimal(rows.getchildren()[6].text),
                                                                        'P/Cap.Giro': todecimal(rows.getchildren()[7].text),
                                                                        'P/EBIT': todecimal(rows.getchildren()[8].text),
                                                                        'P/ACL': todecimal(rows.getchildren()[9].text),
                                                                        'EV/EBIT': todecimal(rows.getchildren()[10].text),
                                                                        'EV/EBITDA': todecimal(rows.getchildren()[11].text),
                                                                        'Mrg.Ebit': todecimal(rows.getchildren()[12].text),
                                                                        'Mrg.Liq.': todecimal(rows.getchildren()[13].text),
                                                                        'Liq.Corr.': todecimal(rows.getchildren()[14].text),
                                                                        'ROIC': todecimal(rows.getchildren()[15].text),
                                                                        'ROE': todecimal(rows.getchildren()[16].text),
                                                                        'Liq.2meses': todecimal(rows.getchildren()[17].text),
                                                                        'Pat.Liq': todecimal(rows.getchildren()[18].text),
                                                                        'Div.Brut/Pat.': todecimal(rows.getchildren()[19].text),
                                                                        'Cresc.5anos': todecimal(rows.getchildren()[20].text)}})
        
    return list(result.items())


def todecimal(string):
    string = string.replace('.', '')
    string = string.replace(',', '.')
    if (string.endswith('%')):
        string = string[:-1]
        return Decimal(string) / 100
    else:
        return Decimal(string)


def getValuesFundos():
    url = 'http://www.fundamentus.com.br/fii_resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]
    data = {'papel': '',
            'segmento': '',
            'cotacao': '',
            'ffo_yield': '',
            'dividend_yield': '',
            'pvp': '',
            'valor_mercado': '',
            'liquidez': '',
            'qtd_imoveis': '',
            'aluguel_m2': '',
            'cap_rate': '',
            'vacancia_media': ''}
    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')
    pattern = regex.compile(
        '<table id="tabelaResultado".*</table>', regex.DOTALL)
    content = regex.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = OrderedDict()
    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update({rows.getchildren()[0][0].getchildren()[0].text: {'segmento': rows.getchildren()[1].text,
                                                                        'cotacao': rows.getchildren()[2].text,
                                                                        'ffo_yield': rows.getchildren()[3].text,
                                                                        'dividend_yield': rows.getchildren()[4].text,
                                                                        'pvp': rows.getchildren()[5].text,
                                                                        'valor_mercado': rows.getchildren()[6].text,
                                                                        'qtd_imoveis': rows.getchildren()[7].text,
                                                                        'aluguel_m2': rows.getchildren()[8].text,
                                                                        'cap_rate': rows.getchildren()[9].text,
                                                                        'vacancia_media': rows.getchildren()[10].text}})
    return list(result.items())


def getByTicketCurrent(ticker):
    cotacao = web.DataReader(f"{ticker}.SA", data_source="yahoo")
    row = cotacao.iloc[-1]
    return row.to_json()

def getTicketByInterval(ticker,inicio, fim):
    start = convertDate(inicio)
    end = convertDate(fim)
    cotacao = web.DataReader(f"{ticker}.SA", data_source="yahoo", start = start, end = end)
    return cotacao.to_json()

def convertDate(datestr):
    day = int(datestr.split('-')[0])
    month = int(datestr.split('-')[1])
    year = int(datestr.split('-')[2])
    return f'{year}-{month}-{day}'


def getMoedaCotacao():
    requestUrl = requests.get("http://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL,ETH-BRL")
    requestUrl_dic = requestUrl.json()
    return {
        "dolar": requestUrl_dic["USDBRL"]["bid"],
        "euro": requestUrl_dic["EURBRL"]["bid"],
        "btc": requestUrl_dic["BTCBRL"]["bid"],
        "ethereum": requestUrl_dic["ETHBRL"]["bid"],
    }