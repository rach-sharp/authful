import requests
from flask import Flask, request, session, jsonify, redirect
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv, find_dotenv
import os

# setting up config
load_dotenv("/config/.env")

AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE')
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = 'https://' + AUTH0_DOMAIN + '/userinfo'

app = Flask(__name__)
app.secret_key = os.environ.get('AUTHFUL_SECRET_KEY')

app.debug = False

# todo set this to True once I have set up certbot certificates
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_DOMAIN"] = os.environ.get('AUTHFUL_DOMAIN')

oauth = OAuth(app)
auth0 = oauth.remote_app(
    'auth0',
    consumer_key=AUTH0_CLIENT_ID,
    consumer_secret=AUTH0_CLIENT_SECRET,
    request_token_params={
        'scope': 'openid profile',
        'audience': AUTH0_AUDIENCE
    },
    base_url='https://%s' % AUTH0_DOMAIN,
    access_token_method='POST',
    access_token_url='/oauth/token',
    authorize_url='/authorize',
)


# Format error response and append status code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.route('/callback')
def callback_handling():
    resp = auth0.authorized_response()
    if resp is None:
        raise AuthError({'code': request.args['error'],
                         'description': request.args['error_description']}, 401)

    url = 'https://' + AUTH0_DOMAIN + '/userinfo'
    headers = {'authorization': 'Bearer ' + resp['access_token']}
    resp = requests.get(url, headers=headers)
    user_info = resp.json()

    session['JWT_PAYLOAD'] = user_info

    session['PROFILE_KEY'] = {
        'user_id': user_info['sub'],
        'name': user_info['name'],
        'picture': user_info['picture']
    }

    if 'login_redirect' in session:
        return redirect(session["login_redirect"], code=302)
    else:
        return 'you are now logged in. please continue', 200


@app.route('/verify', methods=["GET", "POST"])
def verify():
    """Verify a user according to some criteria"""
    if 'PROFILE_KEY' not in session or 'name' not in session['PROFILE_KEY']:
        return 'no session currently', 401
    if session['PROFILE_KEY']['name'] == "rachel94sharp@gmail.com":
        http_code = 200
    else:
        http_code = 401
    return 'verification page', http_code


@app.route('/login', methods=["GET", "POST"])
def login():
    session['login_redirect'] = request.args["redirect"]
    return auth0.authorize(callback=AUTH0_CALLBACK_URL)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return "ok", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
