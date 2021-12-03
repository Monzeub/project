import requests
import sqlite3
from fastapi import FastAPI, Request 
import uvicorn
app = FastAPI()

@app.get("/")
def root():
  return {"message": "It works !"}



exchangerate = requests.get('http://api.exchangeratesapi.io/v1/latest?access_key=deaa05e1bb6d6cce5849a5933ec83061').json()

rate = exchangerate["rates"]

@app.post("/convert_currency")
async def convert_currency(payload: Request):
 
    values_dict = await payload.json()

    dbase = sqlite3.connect('API_database.db', isolation_level=None)

    query_cur = dbase.execute(''' 
               SELECT Currency FROM Quote 
               WHERE Client_id = {} 
               '''.format(str(values_dict['Client_id'])))
    
    querycur = query_cur.fetchall()[0][0]

    query_prix = dbase.execute(''' 
                SELECT Price_VAT_exclude FROM Quote 
                WHERE Client_id = {} 
                '''.format(str(values_dict['Client_id'])))
    
    queryprix = query_prix.fetchall()[0][0]

     

     
    queryprix = queryprix // rate[querycur]
        

    queryvat = dbase.execute(''' 
    UPDATE Quote 
    SET Price_VAT_exclude = {pricevat}
    WHERE Client_id = {} 
    '''.format(str(values_dict['Client_id']) , pricevat = str(queryprix)))

    querynewcur = dbase.execute('''
    UPDATE Quote
    SET Currency = "EUR"
    WHERE Client_id = {} 
    '''.format(str(values_dict['Client_id'])))
      
    
    
                        
    return queryvat, querynewcur






if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)

