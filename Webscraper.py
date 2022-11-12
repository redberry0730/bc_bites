import requests
import json

diningHalls = {"Lower Live": 21, "Carney's ": 23, "Stuart Hall": 28}
def getDiningHall(name):
    forbiddenNumbers = []
    if name == "Lower Live":
        forbiddenNumbers = ["95", "41", "28", "04", "09", "27", "05", "97", "31"]
    elif name == "Carney's ":
        forbiddenNumbers = ["47", "49", "95", "97", "05", "09", "50"]
    elif name == "Stuart Hall":
        forbiddenNumbers = ["95", "07", "05", "15", "09", "08"]
    webUrl = "https://web.bc.edu/dining/menu/todayMenu_PROD.json"
    allList = json.loads(requests.get(webUrl).text)
    diningList = []
    for i in range(len(allList)):
        if allList[i]["Location_Name"] == name:
            if allList[i]["Menu_Category_Number"] not in forbiddenNumbers and allList[i]["Selling_Price"][:-2] != ".00":
                dictionary = {"Meal Time":allList[i]["Meal_Name"], "Meal Name":allList[i]["Recipe_Print_As_Name"], "Meal Price": allList[i]["Selling_Price"][:-2]}
                diningList.append(dictionary)
    return json.dumps(diningList)


print(getDiningHall("Lower Live"))


