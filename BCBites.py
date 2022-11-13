from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'POST':
        return redirect('vote')
    return render_template("home.html")

@app.route('/vote', methods=['GET', 'POST']) 
def vote():
    return "Hi"

if __name__ == '__main__':
   app.run(debug=True)