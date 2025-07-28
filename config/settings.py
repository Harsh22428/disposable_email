import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DBNAME = os.getenv("MONGO_DBNAME", "disposable_email")
SMTP_PORT = int(os.getenv("SMTP_PORT", 2525))  # default to 2525
