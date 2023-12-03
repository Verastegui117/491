from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import db_name
import jwt

def get_username_and_email_from_token(token):
    try:
        # Decode the token
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        # Extract username and email
        username = decoded_token.get('cognito:username')
        email = decoded_token.get('email')

        return username, email

    except jwt.DecodeError:
        # Handle invalid token
        return "Invalid Token", None

    except jwt.ExpiredSignatureError:
        # Handle expired token
        return "Token Expired", None

app = Flask(__name__)

app.secret_key = 'rand'

app.config['SQLALCHEMY_DATABASE_URI'] = db_name

db = SQLAlchemy()

db.init_app(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


@app.route('/', methods=['GET'])
def get_home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    session['logged_in'] = True
    return redirect(f'https://cloud-proj.auth.us-east-1.amazoncognito.com/login?client_id=66jeh24nesfrshvc5n2q8n072q&response_type=code&scope=email+openid&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fcallback')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.clear()
    return redirect(url_for('get_home')) 

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        token_url = 'https://cloud-proj.auth.us-east-1.amazoncognito.com/oauth2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': '66jeh24nesfrshvc5n2q8n072q',
            'code': code,
            'redirect_uri': 'http://localhost:5000/callback'
        }
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            tokens = response.json()
            session['id_token'] = tokens['id_token']
            username, email = get_username_and_email_from_token(tokens['id_token'])
            session['email'] = email
 
            return redirect(url_for('get_home'))
        else:
            return 'Error fetching tokens', 400
    else:
        return 'Authorization code not found', 400

@app.route('/is_authenticated', methods=['GET'])
def is_authenticated():
    if 'id_token' in session:
        return True
    else:
        return False

@app.route('/contact', methods=['GET'])
def get_contact():
    return render_template("contact.html")


@app.route('/headache', methods=['GET'])
def get_heaadache():
    return render_template("headache.html")

@app.route('/cold', methods=['GET'])
def get_cold():
    return render_template("cold.html")

@app.route('/lethargy', methods=['GET'])
def get_lethargy():
    return render_template("lethargy.html")

@app.route('/stomach', methods=['GET'])
def get_stomach():
    return render_template("stomach.html")

@app.route('/forum', methods=['GET'])
def get_forum():
    return render_template("forum.html")


@app.route('/add-comment', methods=['POST'])
def add_comment():

    if not is_authenticated():
        return redirect(url_for('login'))
    else:
        data = request.form

        # Validate input data
        if not data or 'content' not in data:
            return jsonify({'message': 'Missing required fields'}), 400

        # Create a new comment instance
        new_comment = Comments(
            username=session['email'],
            content=data['content']
        )
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('get_comments'))

@app.route('/comments')
def get_comments():
    # Query all comments from the database
    comments = Comments.query.all()

    # Convert the comments to a list of dictionaries to make them JSON serializable
    comments_list = [
        {
            'id': comment.id,
            'username': comment.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for comment in comments
    ]

    # Render an HTML template with comments data
    return render_template('forum.html', comments=comments_list)


if __name__ == '__main__':
    app.run(debug=True)
