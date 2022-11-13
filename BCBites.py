from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'POST':
        return redirect('/carney')
    return render_template("home.html")

@app.route('/carney', methods=['GET', 'POST']) 
def carney():
    return render_template("Carney.html")
    
@app.route('/lower', methods=['GET', 'POST']) 
def lower():
    return render_template("Lower.html")

@app.route('/stuart', methods=['GET', 'POST']) 
def carney():
    return render_template("Stuart.html")

if __name__ == '__main__':
   app.run(debug=True)