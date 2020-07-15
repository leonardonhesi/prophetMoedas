import pandas as pd
from datetime import datetime
from mongodb  import saveData
from data     import get
from bs4      import BeautifulSoup
import requests

def pegaLMEAtual():
    try:
        dRet = dict()
        url = "https://www.lme.com/Metals/Non-ferrous/Copper#tabIndex=0"
        resp     = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        # Obter a data
        data = soup.find('div', {'class': 'delayed-date left'})
        dRet['data'] = data.text
        dRet['data'] = datetime.strptime(dRet['data'].split('for')[1].strip(),'%d %B %Y' ) 
        # Primeira tabela
        table = soup.find_all('table')[0]
        td = table.find('td', text='Cash')
        dRet['lme'] = td.findNext('td').text 
        table = soup.find_all('table')[0]
        td = table.find('td', text='3-months')
        dRet['lme3m'] = td.findNext('td').text 
        # Segunda tabela
        table = soup.find_all('table')[1]
        td = table.find('td', text='Opening Stock')
        dRet['stock'] = td.findNext('td').text
        df = pd.DataFrame([dRet], columns =['data','lme','lme3m','stock'])
        df['data']      = pd.to_datetime(df['data']).dt.normalize()
        df              = df.set_index('data')
        return df
    except:
        return pd.DataFrame([]) 


def pegarDolar(dDataDe="01-01-2008", dDataAte="07-10-2020", cBoletim ="Abertura"):
    try:
        url      = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        url      += "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        url      += "?@moeda='USD'&@dataInicial='"
        url      += dDataDe
        url      += "'&@dataFinalCotacao='"
        url      += dDataAte
        url      +="'&$top="
        url      += "10000"
        url      += "&$filter=tipoBoletim%20eq%20'"
        url      += cBoletim
        url      += "'&$format=json&$select=cotacaoCompra,"
        url      +="cotacaoVenda,dataHoraCotacao,tipoBoletim"
        header   = { 'Accept': 'application/json' }
        resp     = requests.get(url, headers=header).json()
        df = pd.DataFrame(resp['value'], columns =['cotacaoCompra','cotacaoVenda','dataHoraCotacao','tipoBoletim'])
        df = df.drop(['tipoBoletim'], axis=1)
        df['dataHoraCotacao']      = pd.to_datetime(df['dataHoraCotacao']).dt.normalize()
        df.columns                 = ['cotacaoCompra', 'cotacaoVenda', 'data']
        df                         = df.set_index('data')
        return df
    except:
        return pd.DataFrame([])

def unique(df_novo, df_antigo):
    key_diff   = set(df_novo.index).difference(df_antigo.index)
    where_diff = df_novo.index.isin(key_diff)
    resultado  = df_novo[where_diff]
    return resultado

def dolar():
    dHoje     = datetime.now().strftime('%m-%d-%Y') 
    df_atual  = get(Datafrom='dolar')
    df_novo   = pegarDolar(dDataDe=dHoje, dDataAte=dHoje, cBoletim ="Abertura")
    df_tosave = unique(df_novo, df_atual)
    saveData(df_tosave, colection='dolar')
    return True

def lme():
    df_atual  = get(Datafrom='lme')
    df_novo   = pegaLMEAtual()
    df_tosave = unique(df_novo, df_atual)
    saveData(df_tosave, colection='lme')
    return True

def geral():
    df_dolar  = get(Datafrom='dolar')
    df_lme    = get(Datafrom='geral')
    result    = df_dolar.join(df_lme, how='outer')
    saveData(result, colection='geral')
    return True