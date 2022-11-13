import datetime
import pymongo
from pymongo import MongoClient

from Webscraper import getDiningHall
#make cleint and root database
client = MongoClient("mongodb+srv://BCBites:Baldwin@cluster0.vvuy5vd.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db

#initialize collection for each dining hall
carney = db.carney
lower = db.lower
stuart = db.stuart

carney.create_index([('ID', pymongo.ASCENDING)], unique=True)
lower.create_index([('ID', pymongo.ASCENDING)], unique=True)
stuart.create_index([('ID', pymongo.ASCENDING)], unique=True)

def refresh_menu():
    #clears collections
    carney.delete_many({})
    lower.delete_many({})
    stuart.delete_many({})

    #gets new data
    lower_items = getDiningHall("Lower Live")
    carney_items = getDiningHall("Carney's ")
    stuart_items = getDiningHall("Stuart Hall")

    #puts new data into collections 
    if carney_items:
        try:
            carney.insert_many(carney_items)
        except pymongo.errors.BulkWriteError:
            print("Found Duplicate")

    if lower_items:
        try:
            lower.insert_many(lower_items)
        except pymongo.errors.BulkWriteError:
            print("Found Duplicate")
    if stuart_items:
        try:
            stuart.insert_many(stuart_items)
        except pymongo.errors.BulkWriteError:
            print("Found Duplicate")

refresh_menu()

def get_dinner(dining_hall):
    dinner = dining_hall.find({"Meal Time": "DINNER"})
    for item in dinner:
        print(item)
    return dinner

def get_lunch(dining_hall):
    lunch = dining_hall.find({"Meal Time": "DINNER"})
    for item in lunch:
        print(item)
    return lunch

def get_breakfast(dining_hall):
    breakfast = dining_hall.find({"Meal Time": "DINNER"})
    for item in breakfast:
        print(item)
    return breakfast

def get_current_menu(dining_hall):
    now = datetime.datetime.now()
    today11 = now.replace(hour=11, minute=0, second=0, microsecond=0)
    today2 = now.replace(hour=20, minute=30, second=0, microsecond=0)

    if now < today11:
        get_breakfast(dining_hall)
    elif now < today2:
        get_lunch(dining_hall)
    else:
        get_dinner(dining_hall)

get_current_menu(lower)

#Dinner 4:30 - 8:30
#Lunch 11:00 - 2:30
#Breakfast 9:00 - 11:00