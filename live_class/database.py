from pymongo import MongoClient
import os
from urllib.parse import quote_plus

username = quote_plus("user1")
password = quote_plus("nithin@12.A")

uri = f"mongodb+srv://{username}:{password}@prana-db.nthkhs7.mongodb.net/prana_db?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["prana_db"]

courses_collection = db["courses"]
enrollments_collection = db["enrollments"]
chats_collection = db["chats"]
