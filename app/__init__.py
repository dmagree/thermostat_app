import os

from dash import Dash
from flask import Flask 

from .google_oauth import GoogleOAuth

# configure app
server = Flask(__name__)
app = Dash(
	__name__,
	server=server,
	url_base_pathname='/',
	auth='auth',
)

# configure google oauth using environment variables
server.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
server.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ["GOOGLE_OAUTH_CLIENT_ID"]
server.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]

# allow for insecure transport for local testing (remove in prod)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# designate list of authorized emails
authorized_emails = [
	"someone@gmail.com",
]

auth = GoogleOAuth(
    app,
    authorized_emails,
)
