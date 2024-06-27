# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os #é usada para acessar variáveis de ambiente ou manipular o sistema de arquivos

# import variáveis de ambiente
commodities = ['CL=F', 'GC=F', 'SI=F']

load_dotenv()

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

#Extract
def search_commodities(symbol, period='5d', interval='1d'):
    ticker = yf.Ticker(symbol)
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
def save_postgres(df, schema='public'):
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Date', schema=schema)
    
#Load
if __name__ == "__main__":
    concat_data = search_all_commodities(commodities)
    # print(concat_data) debug
    save_postgres(concat_data, schema='public')
