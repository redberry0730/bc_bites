from flask import Flask, render_template, request, redirect, url_for
import MongoDB
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=MongoDB.refresh_menu, trigger="interval", seconds=3600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/', methods=['GET', 'POST']) 
def index():
    return render_template('home.html')

@app.route('/run', methods=['GET', 'POST']) 
def run():
    return redirect('/dining')

@app.route('/dining', methods=['GET', 'POST']) 
def dining():
    if request.method == 'POST':
        getName = request.form['dining']
        getNameArr = getName.split(", ")
        if getNameArr[1] == "carney":
            MongoDB.carney.update_one({"_id": getNameArr[0]}, {"$inc": { "Votes": 1 }})
        if getNameArr[1] == "lower":
            MongoDB.lower.update_one({"_id": getNameArr[0]}, {"$inc": { "Votes": 1 }})
        if getNameArr[1] == "stuart":
            MongoDB.stuart.update_one({"_id": getNameArr[0]}, {"$inc": { "Votes": 1 }})
        return redirect('/thankyou')
    carney = MongoDB.menu_format(MongoDB.carney)
    lower = MongoDB.menu_format(MongoDB.lower)
    stuart = MongoDB.menu_format(MongoDB.stuart)
    return render_template("Page-1.html", data1 = carney, data2 = lower, data3 = stuart)

@app.route('/thankyou', methods=['GET', 'POST']) 
def thankyou():
    global home
    home = False
    if request.method == 'POST':
        return redirect('/')
    return render_template("thankyou.html")

@app.route('/home', methods=['GET', 'POST']) 
def home():
    global home
    home = False
    return redirect('/')

if __name__ == '__main__':
   app.run(debug=True)