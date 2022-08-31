from flask import Flask, request,session,abort, redirect,render_template, jsonify
from flask_cors import CORS, cross_origin

import requests
import os
import pathlib
import json

app = Flask(__name__)
app.secret_key = "sanskriti"
CORS(app)

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

current_user = "not_defined"

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", current_user_id=current_user)

GOOGLE_CLIENT_ID = "899477051975-7s9rub7s022pt1s33s0o0k80rgmul78g.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email","openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper



@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback", methods = ['GET', 'POST'])
def callback():
    global current_user
    
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    
    current_user = id_info.get("sub")
      
    with open('./static/json/user_id.json', 'r') as u:
        user_id_json_data = json.load(u)
        
    user_id_json_data[id_info.get("sub")] = { "user_name" : id_info.get("name") , "user_email" : id_info.get("email"), "user_dp": id_info.get("picture")}
    
    with open('./static/json/user_id.json', 'w') as y:
        json.dump(user_id_json_data, y)
        
    return redirect("/")


@app.route("/logout")
def logout():
     global current_user
     session.clear()
     current_user = "not_defined"
     return redirect("/")
 
if __name__ == '__main__':
    app.run()