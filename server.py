from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-ey' 


@app.route('/', methods=['GET'])
def get_home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return redirect(f'https://cloud-proj.auth.us-east-1.amazoncognito.com/login?client_id=66jeh24nesfrshvc5n2q8n072q&response_type=code&scope=email+openid&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fcallback')

@app.route('/logout')
def logout():
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
            session['user'] = { 'email': 'extracted_email_from_id_token' }
            return redirect(url_for('get_home'))
        else:
            return 'Error fetching tokens', 400
    else:
        return 'Authorization code not found', 400

@app.route('/is_authenticated', methods=['GET'])
def is_authenticated():
    if 'id_token' in session:
        return jsonify({'authenticated': True}), 200
    else:
        return jsonify({'authenticated': False}), 401

@app.route('/contact', methods=['GET'])
def get_contact():
    return render_template("contact.html")


@app.route('/headache', methods=['GET'])
def get_heaadache():
    return render_template("headache.html")

@app.route('/cold', methods=['GET'])
def get_cold():
    return render_template("cold.html")

@app.route('/stomach', methods=['GET'])
def get_stomach():
    return render_template("stomach.html")


if __name__ == '__main__':
    app.run(debug=True)
