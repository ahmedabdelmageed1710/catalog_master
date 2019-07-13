from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
         json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['email']
    output += '!</h1>'
    print "done!"
    return output


def createUser(login_session):
    newUser = User(email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['email']
        del login_session['user_id']
        del login_session['access_token']
        return redirect(url_for('showCategories'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON API to view Category Information
@app.route('/catalog/JSON')
def categoriesJSON():
    categories = session.query(Category)
    return jsonify(categories=[r.serialize for r in categories])


# JSON API to view category items
@app.route('/catalog/<catalogId>/items/JSON')
def itemsJSON(catalogId):
    category = session.query(Category).filter_by(id=catalogId).one()
    return jsonify(items=[r.serialize for r in category.items])


# JSON API to view item Information
@app.route('/catalog/<catalogId>/item/<itemId>/JSON')
def itemJSON(catalogId, itemId):
    item = session.query(Item).filter_by(id=itemId).one()
    return jsonify(item=item.serialize)


# Show all categories
@app.route('/')
def showCategories():
    categories = session.query(Category)
    items = session.query(Item).order_by(desc(Item.id))
    return render_template(
        'categories.html', categories=categories, items=items)


# Show category items
@app.route('/catalog/<categoryName>/items')
def categoryItems(categoryName):
    category = session.query(Category).filter_by(name=categoryName).one()
    items = session.query(Item).filter_by(category_id=category.id)
    categories = session.query(Category)
    return render_template(
        'categoryItems.html',
        items=items, category=category, categories=categories)


# Show item
@app.route('/catalog/<categoryName>/<itemTitle>')
def item(categoryName, itemTitle):
    category = session.query(Category).filter_by(name=categoryName).one()
    item = session.query(Item).filter_by(title=itemTitle).one()
    return render_template('item.html', item=item)


# Create a new item
@app.route('/item/new', methods=['GET', 'POST'])
def newItem():
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        item = Item(title=request.form['title'],
                    description=request.form['description'],
                    category_id=request.form['category_id'],
                    user_id=login_session['user_id'])
        session.add(item)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        categories = session.query(Category)
        return render_template('newItem.html', categories=categories)


# Edit item
@app.route('/catalog/<itemTitle>/edit', methods=['GET', 'POST'])
def editItem(itemTitle):
    if 'email' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(title=itemTitle).one()
    if login_session['user_id'] != item.user_id:
        return '''<script>function myFunction()
         {alert('You are not authorized to edit this item.');}
         </script><body onload='myFunction()'>'''
    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        item.category_id = request.form['category_id']
        session.add(item)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        categories = session.query(Category)
        return render_template(
            'editItem.html', item=item, categories=categories)


# delete item
@app.route('/catalog/<itemTitle>/delete', methods=['GET', 'POST'])
def deleteItem(itemTitle):
    if 'email' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(title=itemTitle).one()
    if login_session['user_id'] != item.user_id:
        return '''<script>function myFunction()
         {alert('You are not authorized to delete this item.');}
         </script><body onload='myFunction()'>'''
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteItem.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
