import os
from dotenv import load_dotenv
from pymongo import MongoClient

#global variable to hold the MongoDB client
client = None
def connect_to_mongo():
    global client
    if client is None:
        load_dotenv()
        CONNECTION_STRING = os.getenv('MONGO_URI')
        client = MongoClient(CONNECTION_STRING)
    return client

def get_database():
    client = connect_to_mongo()
    return client[os.getenv("MONGO_DBNAME", "mydatabase")]

def close_db_connection():
    global client
    if client is not None:
        client.close()
        client = None

if __name__ == "__main__":   
   # Get the database
   dbname = get_database()