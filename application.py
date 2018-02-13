from database_setup import Base, Category, Item, User
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import make_response, flash
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import requests
import random
import string
import httplib2

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('g_client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Katamari Catalog"

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Connecting to Google's oauth service to establish a secure log-in and create
# New users with unique IDs upon their first time logging in.


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('g_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = int(user_id)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id)
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('Successfully Logged Out')
        return redirect(url_for('showCategories'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        flash('Failed to revoke token for given user')
        return redirect(url_for('showCategories'))

# JSON ENDPOINTS


@app.route('/<category_name>/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(
        category_id=category.id).all()
    return jsonify(Item=[i.serialize for i in items])


@app.route('/<category_name>/<item_name>/JSON')
def itemItemJSON(category_name, item_name):
    items = session.query(Item).filter_by(name=item_name).one()
    return jsonify(Category_Items=items.serialize)


@app.route('/allcategories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[r.serialize for r in categories])

# Rendering the webpages based on the data in the database


@app.route('/')
@app.route('/home/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    newest_category = session.query(Category).order_by(
        desc(Category.timestamp)).limit(5)
    newest_item = session.query(Item).order_by(
        desc(Item.timestamp)).limit(5)
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories,
                               newest_category=newest_category,
                               newest_item=newest_item)
    else:
        return render_template('categories.html', categories=categories,
                               newest_category=newest_category,
                               newest_item=newest_item)


@app.route('/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


@app.route('/<category_name>/edit/', methods=['GET', 'POST'])
def editCategory(category_name):
    editedCategory = session.query(
        Category).filter_by(name=category_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        return """<script>function myFunction()
        {alert('You are not authorized to edit this category.
        Please create your own category in order to edit.');}
        </script><body onload='myFunction()'>"""
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited: %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)


@app.route('/<category_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_name):
    categoryToDelete = session.query(
        Category).filter_by(name=category_name).one()
    itemsToDelete = session.query(Item).filter_by(
        category_id=categoryToDelete.id)
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        return """<script>function myFunction()
        {alert('You are not authorized to delete this category.
        Please create your own category in order to delete.');}
        </script><body onload='myFunction()'>"""
    if request.method == 'POST':
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.delete(categoryToDelete)
        for item in itemsToDelete:
            session.delete(item)
        session.commit()
        return redirect(url_for('showCategories', category_name=category_name))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


@app.route('/<category_name>')
@app.route('/<category_name>/items/')
def showAllItems(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    creator = getUserInfo(category.user_id).one()
    items = session.query(Item).filter_by(
        category_id=category.id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicitems.html', items=items,
                               category=category, creator=creator)
    else:
        return render_template('items.html', items=items, category=category,
                               creator=creator)


@app.route('/<category_name>/<item_name>')
def showOneItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    creator = getUserInfo(category.user_id).one()
    item = session.query(Item).filter_by(name=item_name).one()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicitem.html', item=item, category=category,
                               creator=creator)
    else:
        return render_template('1item.html', item=item, category=category,
                               creator=creator)


@app.route('/<category_name>/new/', methods=['GET', 'POST'])
def newItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    if login_session['user_id'] != category.user_id:
        return """<script>function myFunction()
        {alert('You are not authorized to add items to this category.
        Please create your own category in order to add items.');}
        </script><body onload='myFunction()'>"""
    else:
        if request.method == 'POST':
            newItem = Item(name=request.form['name'],
                           description=request.form['description'],
                           size=request.form['size'], category_id=category.id,
                           user_id=category.user_id)
            session.add(newItem)
            flash('New Item %s Successfully Created' % (newItem.name))
            session.commit()
            return redirect(url_for('showAllItems', category_name=category_name))
    return render_template('newitem.html', category_name=category_name)


@app.route('/<category_name>/<item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    if login_session['user_id'] != category.user_id:
        return """<script>function myFunction()
                {alert('You are not authorized to edit items in this category.
                Please create your own category in order to edit items.');}
                </script><body onload='myFunction()'>"""
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['size']:
            editedItem.size = request.form['size']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showAllItems', category_name=category_name))
    else:
        return render_template('edititem.html',
                               category_name=category_name, item_name=item_name,
                               item=editedItem)


@app.route('/<category_name>/<item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    itemToDelete = session.query(Item).filter_by(name=item_name).one()
    if login_session['user_id'] != category.user_id:
        return """<script>function myFunction()
                {alert('You are not authorized to delete items in this category
                please create your own category in order to delete items.');}
                </script><body onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showAllItems', category_name=category_name))
    else:
        return render_template('deleteItem.html', item=itemToDelete,
                               category=category)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
