from deta import Deta
from dotenv import load_dotenv
import os

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")
deta = Deta(DETA_KEY)

db = deta.Base("attendance")

def insert_user(username, name, email, password):
    return db.put({"key": username, "name":name, "email":email, "password":password, "present_dates":[]})

def fetch_all_users():
    res = db.fetch()
    return res.items


def get_user(username):
    return db.get(username)


def update_user(username, updates):
    return db.update(updates, username)


