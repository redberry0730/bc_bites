from datetime import date
from datetime import time
from datetime import datetime
import pymongo
import json
from pymongo import MongoClient
from bson.json_util import dumps, loads

from Webscraper import getDiningHall
#make client and root database
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
    #refresh_menu()
    now = datetime.now()
    today11 = now.replace(hour=11, minute=0, second=0, microsecond=0)
    today2 = now.replace(hour=20, minute=30, second=0, microsecond=0)

    if now < today11:
        return dumps(list(get_breakfast(dining_hall)))
    elif now < today2:
        return dumps(list(get_lunch(dining_hall)))
    else:
        return dumps(list(get_dinner(dining_hall)))

def get_most_voted(dining_hall):
    most_votes = dining_hall.find().sort({"Votes", -1}).limit(1)
    return most_votes

#lower.update_one({"Meal Name": "Cod Caprese"}, {"$inc": { "Votes": 1 }})

#Dinner 4:30 - 8:30
#Lunch 11:00 - 2:30
#Breakfast 9:00 - 11:00

#id = [{"_id": {"$oid": "6370813ff02cae1f6f1ea8de"}, "Serve_Date": "11/12/2022", "Meal Time": "BREAKFAST", "Meal Name": "Cage Free Hard Boiled Egg", "Meal Price": "1.49", "Votes": 0, "URL": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTs_NR5DjsdjyU90vOqVWjpX2kEIzetJ8b8wz3K2y1e45a4veEMh7oj6HF5aq4&s"}, {"_id": {"$oid": "6370813ff02cae1f6f1ea8df"}, "Serve_Date": "11/12/2022", "Meal Time": "BREAKFAST", "Meal Name": "Chocolate Chip Oatmeal Pancakes", "Meal Price": "2.59", "Votes": 0, "URL": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdtxPD0HffocDs52Rfdw5eJ4-2vnSywduHNkg5SnGGF2JDohJOi4cof7COasI&s"}, {"_id": {"$oid": "6370813ff02cae1f6f1ea8e0"}, "Serve_Date": "11/12/2022", "Meal Time": "BREAKFAST", "Meal Name": "Scrambled Eggs", "Meal Price": "4.39", "Votes": 0, "URL": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLzCeimFKaQv1duOiiy0rHmrnbr0vmaUY-wZ9vDP1DkpxqBGiVINVDb1qOZA&s"}, {"_id": {"$oid": "6370813ff02cae1f6f1ea8e1"}, "Serve_Date": "11/12/2022", "Meal Time": "BREAKFAST", "Meal Name": "Cage Free 2 Egg Omelet Made to Order", "Meal Price": "8.99", "Votes": 0, "URL": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFoLSEO_XINZHM8BwYNn_nXKdQjrFb4rc0Wym1lNc0sFCvC-D4dQMZJCvVrB8&s"}, {"_id": {"$oid": "6370813ff02cae1f6f1ea8e2"}, "Serve_Date": "11/12/2022", "Meal Time": "BREAKFAST", "Meal Name": "Egg White Omelet", "Meal Price": "8.99", "Votes": 0, "URL": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpmpO5lXDWonu-GYtl2jUalh628Z1MEfL6Qk6dmwR3cIRo3qyBCeZEYKSf26g&s"}, {"_id": {"$oid": "6370813ff02cae1f6f1ea8e3"}, "Serve_Date": "11/12/2022", "Meal Time": "BREAKFAST", "Meal Name": "Tofu Scramble", "Meal Price": "4.39", "Votes": 0, "URL": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTo-bjq4oUzkMG-Z3i2VRReOebWaQQV5uAkJVrFoFVMrI6KDW48fryKb2XppQ&s"}]

#Function to extract necessary information from the IDs
#ex = []
#for i in id:
#    arr = []
#    arr.append(i["Meal Time"])
#    arr.append(i["Meal Name"])
#    arr.append(i["Meal Price"])
#    arr.append(i["Votes"])
#    arr.append(i["URL"])
#    ex.append(arr)
#added function using code 

def menu_format(dining_hall):
    a = get_current_menu(dining_hall)
    a = json.loads(a)
    arr1 = []
    for i in a:
        arr1.append([i["Meal Time"], i["Meal Name"], i["Meal Price"], i["Votes"], i["URL"], i["_id"]])
    return arr1
