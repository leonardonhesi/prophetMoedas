import pandas   as pd
import pymongo
from pymongo    import MongoClient

client = MongoClient("mongodb://moedas:mo3d4s@ds035603.mlab.com:35603/moedas?retryWrites=false")
db     = client['moedas']

def saveData(df, colection='dolar'):
    col      = db[colection]
    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    col.insert_one({"index":colection,"data":data_dict})
    return True

def getdbData(colection='dolar'):
    col          = db[colection]
    data_from_db = col.find_one({"index":colection})
    if (data_from_db):
        df = pd.DataFrame(data_from_db["data"])
        df['dataCotacao'] = df['data'].dt.strftime('%Y-%m-%d')
        df.set_index("data", inplace=True)
    else:
        df = pd.DataFrame()
    return df