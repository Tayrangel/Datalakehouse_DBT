# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os #é usada para acessar variáveis de ambiente ou manipular o sistema de arquivos

# import variáveis de ambiente
commodities = ['CL=F', 'GC=F', 'SI=F']

#Extract
def search_commodities(symbol, period='5d', interval='1d'):
    ticker = yf.Ticker('CL=F')
    data = ticker.history(period=period, interval=interval)[['Close']]
    data['symbol'] = symbol
    return data

#Concat
def search_all_commodities(commodities):
    all_data = []
    for symbol in commodities:
        data = search_commodities(symbol)
        all_data.append(data)
    return pd.concat(all_data)

#Save

    
#Load
if __name__ == "__main__":
    concat_data = search_all_commodities(commodities)
    print(concat_data) 