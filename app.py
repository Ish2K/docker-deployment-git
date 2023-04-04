# basic fastapi app

from fastapi import FastAPI, HTTPException
import mysql.connector
from fastapi.requests import Request
import json
from pydantic import BaseModel

app = FastAPI()

class Database(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/widgets')
async def get_widgets():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()


    cursor.execute("SELECT * FROM widgets")

    row_headers=[x[0] for x in cursor.description] #this will extract row headers

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()

    return json.dumps(json_data)

@app.post("/create-database")
async def create_database(db: Database):
    try:
        mydb = mysql.connector.connect(
          host="mysqldb",
          user="root",
          password="p@ssw0rd1"
        )

        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE {}".format(db.name))

        return {"message": "Database created successfully"}

    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Database creation failed: {}".format(error))
    
@app.post("/create-table")
async def create_table(db: Database):
    try:
        mydb = mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="p@ssw0rd1",
            database=db.name
        )
        cursor = mydb.cursor()

        cursor.execute("DROP TABLE IF EXISTS widgets")
        cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
        cursor.close()

        return {"message": "Table widgets created successfully"}

    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Database creation failed: {}".format(error))
