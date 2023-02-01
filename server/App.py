from flask import Flask, redirect, url_for, render_template, request
import sys

sys.path.insert(1, '/Users/arymehr/Documents/CS Projects/Numpy-Assistant/ML')
from responses import Bot


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        query = request.form["query"]
        response = bot.ask_dnn(query)
        return render_template('index.html', response=response)
    else:
        return render_template('index.html', response=None)

if __name__ == '__main__':
    bot = Bot()
    app.run(debug=True, port=8080, host='0.0.0.0')