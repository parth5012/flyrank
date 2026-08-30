
from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("DATABASE_URL",'')

# check_same_thread=False is unique and required for SQLite
connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
engine = create_engine(url, connect_args=connect_args)

