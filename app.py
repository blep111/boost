import os
from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import quote, unquote
from token_manager import TokenManager

# Initialize the Flask application
app = Flask(__name__)

# Initialize the token manager
token_manager = TokenManager()

# Set up Flask app configuration (SECRET_KEY for CSRF protection, etc.)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ebc9973ecd508f7fae8d110e00b776077654ba7e17fc2149e66bdaa168580de5')

@app.route('/')
def index():
    # Retrieve the Facebook token if available and valid
    fb_token = token_manager.get_token('facebook')

    if fb_token:
        print(f"Facebook Access Token: {fb_token}")
    else:
        print("Facebook Access Token is not available or expired.")
    
    return render_template('index.html')

@app.route('/quote', methods=['POST'])
def quote_string():
    if request.method == 'POST':
        input_string = request.form['input_string']
        quoted_string = quote(input_string)
        return render_template('index.html', quoted_string=quoted_string)

@app.route('/unquote', methods=['POST'])
def unquote_string():
    if request.method == 'POST':
        input_string = request.form['input_string']
        unquoted_string = unquote(input_string)
        return render_template('index.html', unquoted_string=unquoted_string)

@app.route('/set_token', methods=['POST'])
def set_token():
    """Route to manually set an access token."""
    access_token = request.form['access_token']
    expires_in = int(request.form['expires_in'])  # expiration time in seconds

    # Store the token in TokenManager (for Facebook in this case)
    token_manager.set_token('facebook', access_token, expires_in)
    
    return redirect(url_for('index'))

@app.route('/refresh_token', methods=['POST'])
def refresh_token():
    """Route to manually refresh the access token."""
    access_token = request.form['access_token']
    expires_in = int(request.form['expires_in'])

    # Refresh the token in TokenManager
    token_manager.refresh_token('facebook', access_token, expires_in)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)