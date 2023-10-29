from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
