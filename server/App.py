from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        query = request.form["query"]
        return render_template('index.html', response=query)
    else:
        return render_template('index.html', response=None)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')