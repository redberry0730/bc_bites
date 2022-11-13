from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST']) 
def index():
    return render_template('home.html')

@app.route('/run', methods=['GET', 'POST']) 
def run():
    return redirect('/carney')

@app.route('/carney', methods=['GET', 'POST']) 
def carney():
    return render_template("Page-1.html")

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