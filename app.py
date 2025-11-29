# app.py

from flask import Flask, redirect, request, session, url_for, render_template
from authlib.integrations.flask_client import OAuth
import requests
import json
from config import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, REDIRECT_URI
from token_manager import add_token, get_token

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key
oauth = OAuth(app)

# Facebook OAuth setup
facebook = oauth.register(
    'facebook',
    client_id=FACEBOOK_CLIENT_ID,
    client_secret=FACEBOOK_CLIENT_SECRET,
    authorize_url='https://www.facebook.com/v13.0/dialog/oauth',
    access_token_url='https://graph.facebook.com/v13.0/oauth/access_token',
    api_base_url='https://graph.facebook.com/v13.0/',
    client_kwargs={'scope': 'email,public_profile'}
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    # Redirect to Facebook for login
    return facebook.authorize_redirect(redirect_uri=REDIRECT_URI)

@app.route('/auth/facebook/callback')
def auth():
    # Get the token and save it
    token = facebook.authorize_access_token()
    user_info = facebook.parse_id_token(token)

    # Save token to session and also to a file/database
    session['user'] = user_info
    session['token'] = token['access_token']
    add_token(user_info['sub'], token['access_token'])  # Save user token

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_info = session.get('user')
    return render_template('dashboard.html', user_info=user_info)

@app.route('/comment', methods=['POST'])
def comment():
    if 'token' not in session:
        return redirect(url_for('login'))

    # Get the token from session
    token = session['token']
    post_id = request.form['post_id']  # The post ID to comment on
    comment_message = request.form['comment_message']

    # Use the Facebook Graph API to post a comment
    comment_url = f'https://graph.facebook.com/v13.0/{post_id}/comments'
    params = {'access_token': token, 'message': comment_message}
    response = requests.post(comment_url, data=params)

    if response.status_code == 200:
        return f"Comment successfully posted!"
    else:
        return f"Error: {response.json()}"

if __name__ == '__main__':
    app.run(debug=True)