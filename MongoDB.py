from datetime import date
from datetime import time
from datetime import datetime
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads

from Webscraper import getDiningHall
#make cleint and root database
client = MongoClient("mongodb+srv://BCBites:Baldwin@cluster0.vvuy5vd.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db

#initialize collection for each dining hall
carney = db.carney
lower = db.lower
stuart = db.stuart

carney.create_index([('Meal Name', 1), ('Meal Time', 1)], unique=True)
lower.create_index([('Meal Name', 1), ('Meal Time', 1)], unique=True)
stuart.create_index([('Meal Name', 1), ('Meal Time', 1)], unique=True)

def refresh_menu():
    #gets new data
    lower_items = getDiningHall("Lower Live")
    carney_items = getDiningHall("Carney's ")
    stuart_items = getDiningHall("Stuart Hall")

    #clears collections if new day
    first = lower_items[0]
    first_time = datetime.strptime(first["Serve_Date"], "%m/%d/%Y")
    if date.today() > first_time.date():
        print("Clearing All")
        carney.delete_many({})
        lower.delete_many({})
        stuart.delete_many({})

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
    #for item in dinner:
     #   print(item)
    return dinner

def get_lunch(dining_hall):
    lunch = dining_hall.find({"Meal Time": "LUNCH"})
    #for item in lunch:
      #  print(item)
    return lunch

def get_breakfast(dining_hall):
    breakfast = dining_hall.find({"Meal Time": "BREAKFAST"})
    #for item in breakfast:
     #   print(item)
    return breakfast

def get_current_menu(dining_hall):
    now = datetime.now()
    today11 = now.replace(hour=11, minute=0, second=0, microsecond=0)
    today2 = now.replace(hour=20, minute=30, second=0, microsecond=0)

    if now < today11:
        return dumps(list(get_breakfast(dining_hall)))
    elif now < today2:
        return dumps(list(get_lunch(dining_hall)))
    else:
        return dumps(list(get_dinner(dining_hall)))

#lower.update_one({"Meal Name": "Cod Caprese"}, {"$inc": { "Votes": 1 }})
#print(get_current_menu(lower))

#Dinner 4:30 - 8:30
#Lunch 11:00 - 2:30
#Breakfast 9:00 - 11:00
