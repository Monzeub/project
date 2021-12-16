import sqlite3
import uvicorn
import requests
from fastapi import FastAPI, Request
import pandas as pd
from datetime import datetime

app = FastAPI()


@app.post("/register_client")
async def register_pey(payload: Request):
    
    values_dict = await payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    queryregisterclient = dbase.execute('''
                    INSERT INTO Clients
                    (Name, Email, Phone , Adress) 
                    VALUES ("{named}", "{email}", "{phone}", "{adress}")             
                    ''' .format(named = values_dict['Name'], email = str(values_dict[ 'Email' ]), phone = str(values_dict[ 'Phone_number' ]),adress = str(values_dict[ 'Adress' ])))
    
    
    dbase.close()
    return "Client created"

@app.post("/insert_credit_card")
async def register_pey(payload: Request):
    
    values_dict = await payload.json()

    dbase = sqlite3.connect('API_database .db', isolation_level=None)


    querycard = dbase.execute('''
    INSERT INTO Credit_card(Credit_card_id, Client_id, Currency)
    VALUES ("{creditcard}", "{clientid}", "{currency}")
    '''.format(creditcard = values_dict['Credit_card_id'], clientid = values_dict['Client_id'], currency = str(values_dict['Currency'])))
    return "Credit card inserted"


@app.post("/register_company")
async def register_pey(payload: Request):
    
    values_dict = await payload.json()

    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    query_company = dbase.execute('''
                    INSERT INTO Companies(Companies_id, Name, Adress, Bank) 
                    VALUES ("{Companies_id}","{Name}","{Adress}", "{Bank}")             
                    '''.format(Companies_id = str(values_dict['Companies_id']), Name=str(values_dict['Name']),Adress=str(values_dict['Adress']), Bank= str(values_dict["Bank"])))
    return "Company inserted"

@app.post("/insert_product")
async def register_pey(payload: Request):
    
    values_dict = await payload.json()

    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    query_product= dbase.execute('''
                    INSERT INTO Product(Name,Price_exclude_VAT,Price_with_VAT, Currency, Companies_id) 
                    VALUES ("{Name}", "{Price_exclude_VAT}","{Price_with_VAT}", "{Currency}", "{Companies_id}")             
                    '''.format(Name=str(values_dict['Name']), Price_exclude_VAT = (values_dict['Price_exclude_VAT']), Price_with_VAT = 0 , Currency=str(values_dict['Currency']), Companies_id= str(values_dict['Companies_id'])))


    Final_price = dbase.execute('''
                    UPDATE Product 
                    SET Price_with_VAT = Price_exclude_VAT * 1.21 
                    ''')

    
    return "Product inserted"

@app.post("/insert_quote") #company fait cette action
async def insert_quote(payload: Request):
    
    values_dict = await payload.json()

    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    datel = requests.get('http://api.exchangeratesapi.io/v1/latest?access_key=65c8383a65058f6e7365011c66c6ae04').json()
    dateotd = datel["date"]

    query_client = dbase.execute ('''
                    SELECT Client_id FROM Clients
                    WHERE Client_id = {}
                    ''' .format(str(values_dict['Client_id'])))

    client_results = query_client.fetchall()[0][0]

    insert_quote = dbase.execute ('''
                    INSERT INTO Quote (Date,Currency, Price_exclude_VAT, Price_with_VAT,Accepted,Client_id)
                    VALUES ("{Date}", "{Currency}","{Price_exclude_VAT}", "{Price_with_VAT}", "{Accepted}", "{Client}")
                    ''' .format(Date=dateotd, Currency="EUR", Price_exclude_VAT = 0, Price_with_VAT = 0, Accepted = 0, Client = client_results))



@app.post("/insert_quote_line") #le client fait cette action
async def register_pey(payload: Request):
    
    values_dict = await payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    query_quote = dbase.execute('''
                    SELECT Quote_id FROM Quote 
                    WHERE Quote_id = {}
                    ''' .format(str(values_dict['Quote_id'])))
    quote_results = query_quote.fetchall()[0][0]
    

    query_quote_line = dbase.execute('''
                  INSERT INTO Quote_lines(Quantity,Line_price,Quote_id, Product_id)
                  VALUES ("{Quantity}","{Line_price}","{Quote_id}", "{Product_id}")
                  '''.format(Quantity = values_dict['Quantity'],Line_price = 0 ,Quote_id = quote_results, Product_id = values_dict['Product_id']))

    return "Quote_line inserted"

@app.post("/update_quote_line")
async def insert_quote_line(payload: Request):
    
    values_dict = await payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    queryclient = dbase.execute('''
                    SELECT Client_id FROM Clients
                    ''')
    listeclient1 = queryclient.fetchall()
    listeclient = [x for elem in listeclient1 for x in elem]
    
    for a in listeclient:

        querychoperquotelines = dbase.execute(''' SELECT Quote_lines.Quote_Lines_id FROM Quote_lines
        JOIN Quote ON Quote.Quote_id = Quote_lines.Quote_id
        JOIN Clients ON Clients.Client_id = Quote.Client_id
        WHERE Clients.Client_id = {Client_id}
        '''.format(Client_id = a))
        listequotelines1 = querychoperquotelines.fetchall()
        listequotelines = [x for elem in listequotelines1 for x in elem]
        

        for i in listequotelines:
            
            Price_exclude_VAT = dbase.execute (''' SELECT Product.Price_exclude_VAT FROM Product
                            LEFT JOIN Quote_lines ON Product.Product_id = Quote_lines.Product_id
                            WHERE Quote_Lines_id= {Quote_lines_id}
                            '''.format( Quote_lines_id= i))
            

            Price_exclude_VAT_results = Price_exclude_VAT.fetchall()[0][0]
            Quantity_quote_lines = dbase.execute('''
                                SELECT  Quantity FROM Quote_lines
                                WHERE Quote_Lines_id = {Quote_Lines_id}
                                '''.format(Quote_Lines_id= i))
            
            Quantity_quote_lines_results = Quantity_quote_lines.fetchall()[0][0]
            New_Price_exclude_VAT = Price_exclude_VAT_results * Quantity_quote_lines_results
                


            Updated_Price_exclude_VAT = dbase.execute('''
                                        UPDATE Quote_lines 
                                        SET Line_price = {New_Price_exclude_VAT1}
                                        WHERE Quote_Lines_id = {Quote_Lines_id}
                                        '''.format(New_Price_exclude_VAT1 = New_Price_exclude_VAT, Quote_Lines_id= i ))

        
   
    return "Quote lines updated"

@app.post("/update_quote")
async def update_quote(payload: Request):

    values_dict = await payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)
    
    data= dbase.execute('''
            SELECT Quote_id, SUM (Line_price) as total_price FROM Quote_lines
            WHERE Quote_id = {Quote_id}
            GROUP BY Quote_id
            '''.format(Quote_id = values_dict['Quote_id']))

    
    data_results = data.fetchall()[0][1]

    print(data_results)

    update_quote = dbase.execute ('''
            UPDATE Quote
            SET Price_exclude_VAT = {data_results1}
            WHERE Quote_id = {Quote_id}
            '''.format (data_results1 = data_results, Quote_id = values_dict['Quote_id']))

    
    Final_price = dbase.execute('''
                    UPDATE Quote
                    SET Price_with_VAT = Price_exclude_VAT * 1.21 
                    ''')



@app.post("/display_quote")
async def register_pey(payload: Request):
    
    values_dict = await payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    data = ''' 
        SELECT  *
        FROM Quote_lines LEFT JOIN Quote
        ON (Quote_lines.Quote_id = Quote.Quote_id)
        WHERE Quote.Quote_id = {Quote_id1}
    
    '''.format(Quote_id1 = values_dict['Quote_id'])

    pd.read_sql_query(data, dbase)

    results = pd.read_sql_query(data, dbase)

    print(results)

@app.post("/accepted_quote")
async def update_quote(payload: Request):

    values_dict = await payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)

    query_active_subscription = dbase.execute(''' 
                    UPDATE Quote
                    SET Accepted = 1
                    WHERE Quote_id = {Quote_id}
                    '''.format(Quote_id = values_dict['Quote_id']))
    
    return "Quote Accepted"

@app.post("/display_invoice")
async def display_invoice(payload: Request):
    values_dict = await payload.json()
    dbase = sqlite3.connect('API_database .db', isolation_level=None)
    
    def readdata():
        mydata = ''' SELECT Companies.Name, Product.Name, Quote_lines.Quantity, Quote_lines.Line_price, Quote.Price_exclude_VAT, Invoice.Price_with_VAT, Invoice.Currency, Invoice.Price_customer, Invoice.Currency_customer FROM Quote_lines
        JOIN Product ON Quote_lines.Product_id = Product.Product_id
        JOIN Invoice ON Invoice.Quote_id = Quote_lines.Quote_id
        JOIN Quote ON Quote.Quote_id = Quote_lines.Quote_id
        JOIN Companies ON Product.Companies_id = Companies.Companies_id
        WHERE Quote_lines.Quote_id = {Quote_id}
        '''.format(Quote_id = values_dict["Quote_id"])
        results = pd.read_sql_query(mydata, dbase)
        print(results)

    readdata()
    
    
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
