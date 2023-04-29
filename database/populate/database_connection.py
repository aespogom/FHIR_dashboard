import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def connect():
    '''
    Handles the connection to the database hostes in Azure
    '''
    DRIVER=os.getenv("DRIVER")
    SERVER=os.getenv("SERVER")
    DATABASE=os.getenv("DATABASE")
    UID=os.getenv("UID")
    PWD=os.getenv("PWD")

    try:
        cnxn = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Uid={UID};Pwd={PWD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = cnxn.cursor()
        print("Database connected")
        return cursor
    except Exception as e:
        print("Not connected, ", e)

def execute_query(query: str, params=()):
    '''
    Handles the execution of any query to the database
    Opens and closes the connection
    '''
    cursor = connect()
    try:
        cursor.execute(query, params)
        cursor.commit()
    except Exception as e:
        print('An error has ocurred: ', e)
    cursor.close()
    print('Connection closed')
