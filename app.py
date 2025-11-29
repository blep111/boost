import os
from flask import Flask, render_template, request
from urllib.parse import quote, unquote

# Create the Flask application instance
app = Flask(__name__)

# Use a secret key for session management and CSRF protection
# Make sure to set it via environment variable in production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ebc9973ecd508f7fae8d110e00b776077654ba7e17fc2149e66bdaa168580de5')

@app.route('/')
def index():
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

if __name__ == "__main__":
    app.run(debug=True)