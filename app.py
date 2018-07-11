#===================
# PokeFlask 0.1 - A Python-Flask WebApp for Pokemon Fans
#===================

#===================
# Imports
#===================

from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import *
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os, random, string, datetime, json, httplib2, requests
# Import login_required from login_decorator.py
from login_decorator import login_required

#===================
# Flask app instance
#===================
app = Flask(__name__)

#===================
# Read CLIENT_SECRETS from Google API
#===================

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
print(CLIENT_ID)

#===================
# Database handling
#===================

# Connect to database
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()


#===================
# Google Login Authetication and Logout
#===================

# Login - Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# GConnect flow
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    request.get_data()
    code = request.data.decode('utf-8')

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
    # Submit request, parse response
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

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
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists, if it doesn't make a new one with Google Credentials
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # Output message after accepted Google login and redirection
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User-login Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Disconnect only if user ir logged in
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
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = redirect(url_for('showCatalog'))
        flash("You are now logged out.")
        return response
    else:
        # If the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Pokedex Catalog Homepage
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Items).order_by(desc(Items.date)).limit(3)
    return render_template('catalog.html',
                            categories = categories,
                            items = items)

# Pokemon for each type page
@app.route('/catalog/<path:category_name>/items/')
def showCategory(category_name):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category=category).order_by(asc(Items.name)).all()
    print items
    count = session.query(Items).filter_by(category=category).count()
    creator = getUserInfo(category.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('public_items.html',
                                category = category.name,
                                categories = categories,
                                items = items,
                                count = count)
    else:
        user = getUserInfo(login_session['user_id'])
        return render_template('items.html',
                                category = category.name,
                                categories = categories,
                                items = items,
                                count = count,
                                user=user)

# Shows a specific Pokemon
@app.route('/catalog/<path:category_name>/<path:item_name>/')
def showItem(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    creator = getUserInfo(item.user_id)
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('public_itemdetail.html',
                                item = item,
                                category = category_name,
                                categories = categories,
                                creator = creator)
    else:
        return render_template('itemdetail.html',
                                item = item,
                                category = category_name,
                                categories = categories,
                                creator = creator)

# Add a Pokemon Type to the Pokedex DB
@app.route('/catalog/addcategory', methods=['GET', 'POST'])
@login_required
def addCategory():
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'],
            user_id=login_session['user_id'])
        print newCategory
        session.add(newCategory)
        session.commit()
        flash('Type Successfully Added!')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('addcategory.html')

# Edit a Pokemon Type
@app.route('/catalog/<path:category_name>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_name):
    editedCategory = session.query(Category).filter_by(name=category_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    # See if the logged in user is the owner of the Type
    creator = getUserInfo(editedCategory.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != Type owner redirect them
    if creator.id != login_session['user_id']:
        flash ("You cannot edit this Type. This Type belongs to %s" % creator.name)
        return redirect(url_for('showCatalog'))
    # POST methods
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        flash('Type Successfully Edited!')
        return  redirect(url_for('showCatalog'))
    else:
        return render_template('editcategory.html',
                                categories=editedCategory,
                                category = category)

# Delete a Pokemon Type
@app.route('/catalog/<path:category_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_name):
    categoryToDelete = session.query(Category).filter_by(name=category_name).one()
    # See if the logged in user is the owner of Type
    creator = getUserInfo(categoryToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != Type owner redirect them
    if creator.id != login_session['user_id']:
        flash ("You cannot delete this Type. This Type belongs to %s" % creator.name)
        return redirect(url_for('showCatalog'))
    if request.method =='POST':
        session.delete(categoryToDelete)
        session.commit()
        flash('Type Successfully Deleted! '+categoryToDelete.name)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deletecategory.html',
                                category=categoryToDelete)

# Add a Pokemon to the Pokedex DB
@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def addItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'],
            description=request.form['description'],
            picture=request.form['picture'],
            # Only existing Pokemon types can be used
            category=session.query(Category).filter_by(name=request.form['category']).one(),
            date=datetime.datetime.now(),
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('Pokemon Successfully Added!')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('additem.html',
                                categories=categories)

# Edit a Pokemon
@app.route('/item/<path:item_name>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_name):
    editedItem = session.query(Items).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    # See if the logged in user is the owner of the Pokemon
    creator = getUserInfo(editedItem.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != Pokemon owner redirect them
    if creator.id != login_session['user_id']:
        flash ("You cannot edit this Pokemon. This Pokemon belongs to %s" % creator.name)
        return redirect(url_for('showCatalog'))
    # POST methods
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        if request.form['category']:
            category = session.query(Category).filter_by(name=request.form['category']).one()
            editedItem.category = category
        time = datetime.datetime.now()
        editedItem.date = time
        session.add(editedItem)
        session.commit()
        flash('Pokemon Successfully Edited!')
        return  redirect(url_for('showCategory',
                                category_name=editedItem.category.name))
    else:
        return render_template('edititem.html',
                                item=editedItem,
                                categories=categories)

# Delete a Pokemon
@app.route('/item/<path:item_name>/delet', methods=['GET', 'POST'])
@login_required
def deleteItem(item_name):
    itemToDelete = session.query(Items).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    # See if the logged in user is the owner of Pokemon
    creator = getUserInfo(itemToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != Pokemon owner redirect them
    if creator.id != login_session['user_id']:
        flash ("You cannot delete this Pokemon. This Pokemon belongs to %s" % creator.name)
        return redirect(url_for('showCatalog'))
    if request.method =='POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Pokemon Successfully Deleted! '+itemToDelete.name)
        return redirect(url_for('showCategory',
                                category_name=itemToDelete.category.name))
    else:
        return render_template('deleteitem.html',
                                item=itemToDelete)


#===================
# JSON
#===================
@app.route('/catalog/JSON')
def allItemsJSON():
    categories = session.query(Category).all()
    category_dict = [c.serialize for c in categories]
    for c in range(len(category_dict)):
        items = [i.serialize for i in session.query(Items)\
                    .filter_by(category_id=category_dict[c]["id"]).all()]
        if items:
            category_dict[c]["Item"] = items
    return jsonify(Category=category_dict)

@app.route('/catalog/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/catalog/items/JSON')
def itemsJSON():
    items = session.query(Items).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<path:category_name>/items/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category=category).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/item/<path:item_name>/JSON')
def ItemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Items).filter_by(name=item_name,\
                                        category=category).one()
    return jsonify(item=[item.serialize])



if __name__ == '__main__':
    app.secret_key = 'DEV_SECRET_KEY'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
