import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

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
    db= client[os.getenv("MONGO_DBNAME", "disposble_email")]
    #  TTL index exists for auto-deleting old emails (7 days)
    db.emails.create_index("date", expireAfterSeconds=604800)
    return db


def close_db_connection():
    global client
    if client is not None:
        client.close()
        client = None
        
def save_email(db, email_dict):
    result = db.emails.insert_one(email_dict)
    return str(result.inserted_id)
    

def get_emails_by_inbox(db, inbox_name):
    emails = list(db.emails.find({"inbox": inbox_name}).sort("date", -1))
    for e in emails:
        e["_id"] = str(e["_id"])
    return emails

def get_email_by_id(db, email_id):
    try:
        obj_id = ObjectId(email_id)
    except Exception:
        return None  # Invalid id format
    email = db.emails.find_one({"_id": obj_id})
    if email:
        email["_id"] = str(email["_id"])
    return email
  

def delete_email_by_id(db, email_id):
    try:
        obj_id = ObjectId(email_id)
    except Exception:
        return False  # Invalid id format
    result = db.emails.delete_one({"_id": obj_id})
    return result.deleted_count > 0

if __name__ == "__main__":   
   # Get the database
   dbname = get_database()