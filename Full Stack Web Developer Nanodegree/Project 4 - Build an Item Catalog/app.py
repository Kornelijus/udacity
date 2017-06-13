#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask import session as login_session, flash
from flask import make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, CategoryItem
import random
import string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import requests
import json

app = Flask(__name__)
engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
client_secrets = json.loads(open("client_secrets.json", "r").read())
CLIENT_ID = client_secrets["web"]["client_id"]


@app.context_processor
def global_variables():
    '''
    Since the user can log in from any page, we need the state to be
    accessible from any template.
    '''
    state = "".join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session["state"] = state

    '''
    Since all templates need to know if the user is logged in or the user's id,
    we need to include the user's id in every template.
    '''
    user_id = login_session.get("user_id", None)

    '''
    Since every page displays the category list, we need to include it
    in every template.
    '''
    catlist = session.query(Category).all()

    return dict(state=state, catlist=catlist, user_id=user_id)


@app.route("/login", methods=["POST"])
def google_login():
    '''
    If state of the server doesn't match the state of the client,
    return 401 with an error message.
    '''
    if request.args.get("state") != login_session["state"]:
        return jsonify(message="Invalid state parameter."), 401
    auth_code = request.data

    '''
    Try exchanging the authentication code for credentials.
    If the exchange fails,
    return 401 with the error message.
    '''
    try:
        oauth_flow = flow_from_clientsecrets("client_secrets.json",
                                             scope="")
        oauth_flow.redirect_uri = "postmessage"
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        return jsonify(message="Failed to exchange auth code."), 401
    token_info_url = "https://www.googleapis.com/oauth2/v1/tokeninfo"
    token_info_params = {
        "access_token": credentials.access_token
    }
    token_info = requests.get(token_info_url, params=token_info_params).json()

    '''
    If the API returns an error,
    return 401 with the error message.
    '''
    if token_info.get("error") is not None:
        return jsonify(message=token_info.get("error")), 401
    gid = credentials.id_token["sub"]

    '''
    If the token is does not belong to the user,
    return 401 with an error message.
    '''
    if token_info["user_id"] != gid:
        return jsonify(message="Token ID doesn't match user ID."), 401

    '''
    If the token wasn't issued to this app,
    return 401 with an error message.
    '''
    if token_info["issued_to"] != CLIENT_ID:
        return jsonify(
            message="Token client ID doesn't match app client ID."), 401
    stored_credentials = login_session.get("credentials")
    stored_gid = login_session.get("gid")

    '''
    If the user is already logged in, there's no need to repeat everything.
    return 200 with a message.
    '''
    if stored_credentials is not None and gid == stored_gid:
        return jsonify(message="User is already logged in."), 200

    '''
    login_session["credentials"] = credentials
    Since trying to store credentials in login_session returns:
    OAuth2Credentials object is not JSON serializable,
    storing access_token instead.
    '''
    login_session["access_token"] = credentials.access_token
    login_session["gid"] = gid

    '''
    Get user info using the API.
    '''
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_params = {
        "access_token": credentials.access_token,
        "alt": "json"
    }
    user_info = requests.get(user_info_url, params=user_info_params).json()

    '''
    Store user info in login_session.
    '''
    login_session["username"] = user_info["name"]
    login_session["email"] = user_info["email"]

    '''
    Check if the user with this email already exists in the database.
    If they don't, add them to the database.
    '''
    user_id = get_user_id(login_session["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session["user_id"] = user_id

    '''
    Finally, redirect to index.
    '''
    return redirect(url_for(".catalog_index"))


@app.route("/logout")
def google_logout():
    access_token = login_session.get("access_token")
    '''
    If the user is not logged in,
    return a 401
    '''
    if access_token is None:
        return jsonify(message="User is not logged in."), 401

    '''
    Revoke the user's token using the API.
    '''
    token_revoke_url = "https://accounts.google.com/o/oauth2/revoke"
    token_revoke_params = {
        "token": access_token
    }
    token_revoke = requests.get(token_revoke_url, params=token_revoke_params)

    '''
    If the API returns a 200,
    delete user info from login_session.
    Else, return a 400.
    '''
    if token_revoke.status_code == 200:
        del login_session["access_token"]
        del login_session["gid"]
        del login_session["username"]
        del login_session["email"]
        del login_session["user_id"]
    else:
        return jsonify(message="Failed to revoke token."), 400

    return redirect(request.referrer)


@app.route("/")
@app.route("/catalog/")
def catalog_index():
    latest_items = session.query(CategoryItem).all()[-5:]
    for i in latest_items:
        i.href = "{}/{}".format(i.category_id, i.user_id)
    return render_template("main.html", items=latest_items)


@app.route("/catalog.json")
def catalog_endpoint():
    catlist = [i.dict() for i in session.query(Category).all()]
    return jsonify(category=catlist)


@app.route("/catalog/<int:category_id>/")
def category_index(category_id):
    cat = session.query(Category).get(category_id)
    return render_template("main.html",
                           cat=cat,
                           items=cat.items)


@app.route("/catalog/<int:category_id>/add/", methods=["GET", "POST"])
def category_item_add(category_id):
    cat = session.query(Category).get(category_id)

    '''
    If GET, render a template containing a form to add items.
    '''
    if request.method == "GET":
        if "username" in login_session:
            return render_template("itemform.html",
                                   cat=cat,
                                   new=True)
        else:
            return jsonify(message="You are not authorized to add items."), 401

    '''
    If POST, add new item.
    '''
    if request.method == "POST":
        if "username" in login_session:
            item = CategoryItem(name=request.form["name"],
                                description=request.form["desc"],
                                category_id=cat.id,
                                user_id=login_session["user_id"])
            session.add(item)
            session.commit()
        return redirect(url_for(".category_index",
                                category_id=category_id))


@app.route("/catalog/<int:category_id>/<int:item_id>/")
def category_item_show(category_id, item_id):
    item = session.query(CategoryItem).get(item_id)
    cat = session.query(Category).get(category_id)
    author = get_user(item.user_id).name

    return render_template("itemshow.html",
                           cat=cat,
                           item=item,
                           author=author)


@app.route("/catalog/<int:category_id>/<int:item_id>/edit/",
           methods=["GET", "POST"])
def category_item_edit(category_id, item_id):
    item = session.query(CategoryItem).get(item_id)

    '''
    If GET, render a template containing a form to edit items.
    '''
    if request.method == "GET":
        if ("username" in login_session and
                item.user_id == login_session["user_id"]):
            return render_template("itemform.html",
                                   new=False,
                                   item=item)
        else:
            return jsonify(
                message="You are not authorized to edit this item."), 401

    '''
    If POST, edit item.
    '''
    if request.method == "POST":
        if ("username" in login_session and
                item.user_id == login_session["user_id"]):
            item.name = request.form["name"]
            item.description = request.form["desc"]
            session.add(item)
            session.commit()
        return redirect(url_for(".category_index",
                                category_id=category_id))


@app.route("/catalog/<int:category_id>/<int:item_id>/delete/",
           methods=["GET", "POST"])
def category_item_delete(category_id, item_id):
    item = session.query(CategoryItem).get(item_id)
    cat = session.query(Category).get(category_id)

    '''
    If GET, render a template containing a form that
    asks the user if they actually want to delete the item.
    '''
    if request.method == "GET":
        if ("username" in login_session and
                item.user_id == login_session["user_id"]):
            return render_template("itemdelete.html",
                                   cat=cat,
                                   item=item)
        else:
            return jsonify(
                message="You are not authorized to delete this item."), 401

    '''
    If POST, delete item.
    '''
    if request.method == "POST":
        if ("username" in login_session and
                item.user_id == login_session["user_id"]):
            session.delete(item)
            session.commit()
        return redirect(url_for(".category_index",
                                category_id=category_id))


def create_user(login_session):
    '''
    Create user from login_session and return the user's id.
    '''
    user = User(name=login_session["username"], email=login_session["email"])
    session.add(user)
    session.commit()
    created_user = session.query(User).filter_by(
        email=login_session["email"]).one()
    return created_user.id


def get_user(user_id):
    '''
    Get user object with this id and return it.
    If not found, return None.
    '''
    try:
        user = session.query(User).get(user_id)
        return user
    except BaseException:
        None


def get_user_id(email):
    '''
    Try finding an user with this email and return the user's id.
    If not found, return None.
    '''
    try:
        user = session.query(User).filter_by(
            email=login_session["email"]).one()
        return user.id
    except BaseException:
        return None


if __name__ == "__main__":
    '''
    Time to get hacked!
    '''
    app.secret_key = "123456"
    app.run(host="0.0.0.0",
            port=8000,
            debug=True)
