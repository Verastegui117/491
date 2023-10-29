from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return render_template('index.html')

@app.route('/headache', methods=['GET'])
def get_heaadache():
    return render_template("headache.html")

@app.route('/cold', methods=['GET'])
def get_cold():
    return render_template("cold.html")
if __name__ == '__main__':
    app.run(debug=True)
