from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("SUPABASE_URL","")
key = os.getenv("SUPABASE_KEY","")

client: Client = create_client(uri,key)

def sign_up(email,password,**kwargs):
    return client.auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": kwargs
        }
    })

def sign_in(email,password,**kwargs):
    return client.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

def sign_out():
    return client.auth.sign_out()
