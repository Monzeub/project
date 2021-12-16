import sqlite3
from fastapi import FastAPI, Request 
import uvicorn
app = FastAPI()
import pandas as pd
from datetime import datetime


    
@app.post('/retrieve_MRR')
async def retrieve_MRR(payload : Request):
    values_dict = await payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    def readdata():
        MRR_query =''' SELECT Product.Companies_id, SUM(Quote_lines.Line_price) AS MRR FROM Quote
            LEFT JOIN Quote_lines ON Quote_lines.Quote_id = Quote.Quote_id
            LEFT JOIN Product ON Quote_lines.Product_id = Product.Product_id               
            WHERE Quote.Accepted = 1 
            AND Companies_id = '{}'
            '''.format(values_dict['Companies_id'])

        results = pd.read_sql_query(MRR_query, dbase)
        print(results)
    readdata()

@app.post('/retrieve_ARR')
async def retrieve_ARR(Payload : Request):
    values_dict = await Payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)
    
    MRR_query =dbase.execute(''' SELECT Product.Companies_id, SUM(Quote_lines.Line_price) AS MRR FROM Quote
            LEFT JOIN Quote_lines ON Quote_lines.Quote_id = Quote.Quote_id
            LEFT JOIN Product ON Quote_lines.Product_id = Product.Product_id               
            WHERE Quote.Accepted = 1 
            AND Companies_id = '{}'
            '''.format(str(values_dict['Companies_id'])))
  
    MRR = MRR_query.fetchall()[0][1]
    ARR = MRR * 12

    companyname = dbase.execute(''' SELECT Name FROM Companies
                    WHERE Companies_id = '{}'
                    '''.format(str(values_dict['Companies_id'])))
    Company_name = companyname.fetchall()[0][0]
    
    print("Bonjour ", Company_name, " voici votre ARR:", ARR, "EUR")
    
    return MRR_query, companyname


@app.post('/Number_of_customers')
async def retrieve_ARR(Payload : Request):
    values_dict = await Payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    
    Number_customer_query = dbase.execute(''' SELECT Companies_id, COUNT(DISTINCT Client_id) AS Total_number_customer FROM Quote
                        LEFT JOIN Quote_lines ON Quote_lines.Quote_id = Quote.Quote_id
                        LEFT JOIN Product ON Product.Product_id = Quote_lines.Product_id
                        WHERE Companies_id ={}
                        '''.format(str(values_dict['Companies_id'])))
    
    Number_customer = Number_customer_query.fetchall() [0][1]


    print ("Your number of customers:", Number_customer)

@app.post('/Average_revenues_customers')
async def retrieve_ARR(Payload : Request):
    values_dict = await Payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    MRR_query =dbase.execute(''' SELECT Product.Companies_id, SUM(Quote_lines.Line_price) AS MRR FROM Quote
            LEFT JOIN Quote_lines ON Quote_lines.Quote_id = Quote.Quote_id
            LEFT JOIN Product ON Quote_lines.Product_id = Product.Product_id               
            WHERE Quote.Accepted = 1 
            AND Companies_id = '{}'
            '''.format(str(values_dict['Companies_id'])))
  
    MRR = MRR_query.fetchall()[0][1]
    ARR = MRR * 12

    Number_customer_query = dbase.execute(''' SELECT Companies_id, COUNT(DISTINCT Client_id) AS Total_number_customer FROM Quote
                        LEFT JOIN Quote_lines ON Quote_lines.Quote_id = Quote.Quote_id
                        LEFT JOIN Product ON Product.Product_id = Quote_lines.Product_id
                        WHERE Companies_id ={}
                        '''.format(str(values_dict['Companies_id'])))
    
    Number_customer = Number_customer_query.fetchall() [0][1]

    Average_revenues_customers = ARR / Number_customer
    print("Your average revenues per customer is", Average_revenues_customers)

@app.post('/TABLE')
async def retrieve_ARR(Payload : Request):
    values_dict = await Payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)
    def readdata():
        tablecustomer = ''' SELECT Clients.Client_id, Clients.Name, Quote_lines.Quantity, Product.Name, Quote_lines.Line_price FROM Quote_lines
            JOIN Product ON Quote_lines.Product_id = Product.Product_id
            JOIN Clients ON Quote.Client_id= Clients.Client_id
            JOIN Quote ON Quote.Quote_id = Quote_lines.Quote_id
            JOIN Companies ON Product.Companies_id = Companies.Companies_id
            WHERE Companies.Companies_id = {}
            AND Quote.Accepted = 1
            '''.format(values_dict['Companies_id'])
        results = pd.read_sql_query(tablecustomer, dbase)
        print(results)

    readdata()

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
