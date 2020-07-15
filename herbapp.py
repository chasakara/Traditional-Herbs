import os
from flask import Flask, redirect, render_template, flash, url_for, request, session, abort
from flask_pymongo import PyMongo
from flask_ckeditor import CKEditor
from bson.objectid import ObjectId
import datetime
import bcrypt
import re
import math
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config['MONGODB_NAME'] = "traditional-Herbs"
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


mongo = PyMongo(app)
CKEditor(app)


@app.route('/')
@app.route("/index")
def index():
    herbs = mongo.db.herbs
    featured = ([herb for herb in herbs.aggregate
                ([{"$sample": {"size": 4}}])])
    return render_template('index.html', featured=featured)


@app.route('/all_herbs')
def all_herbs():
    today = datetime.datetime.now().strftime('%d/%B/%Y - %H:%M')
    # If there is a user logged: Username is printed in the Nav
    if 'username' in session:
        # Puts the herb in order Newest to oldest
        limit_per_page = 8
        current_page = int(request.args.get('current_page', 1))
        # get total of all the herbs in db
        herbs = mongo.db.herbs
        number_of_all_rec = herbs.count()
        pages = range(1, int(math.ceil(number_of_all_rec /
                                       limit_per_page)) + 1)
        herbs = herbs.find().sort('_id', -1).skip(
        (current_page - 1)*limit_per_page).limit(limit_per_page)
        return render_template("all_herbs.html",
                               session_name=session['username'],
                               herbs=herbs, today=today,
                               title='All Herbs', current_page=current_page,
                               pages=pages,
                               number_of_all_rec=number_of_all_rec)
    # Puts the herbs in order Newest to oldest but with out the login username
    limit_per_page = 8
    current_page = int(request.args.get('current_page', 1))
    # get total of all the herbs in db
    herbs = mongo.db.herbs
    number_of_all_rec = herbs.count()
    pages = range(1, int(math.ceil(number_of_all_rec /
                                   limit_per_page)) + 1)
    herbs = herbs.find().sort('_id', -1).skip((current_page - 1)
                                               *limit_per_page).limit(limit_per_page)
    return render_template("all_herbs.html", title='All Herbs',
                           current_page=current_page, pages=pages,
                           number_of_all_rec=number_of_all_rec)


@app.route('/my_herbs')
def my_herbs():
    session_name = session['username']
    return render_template("all_herbs.html",
                           session_name=session['username'],
                           herbs=mongo.db.herbs.find(
                            {'username': session_name}),
                             title="My Herbs")


@app.route('/herb/<herb_id>')
def herb(herb_id):
    herb = mongo.db.herbs.find_one({'_id': ObjectId(herb_id)})
# reviews = mongo.db.reviews.find({'_id': ObjectId(herb_id)})
    if 'username' in session:
        return render_template('herb.html',
                               session_name=session['username'],
                               herb=herb)
    return render_template('herb.html', herb=herb, )


@app.route('/add_herb', methods=['POST', 'GET'])
def add_herb():
    today_string = datetime.datetime.now().strftime('%d/%m/%y')
    today_iso = datetime.datetime.now()
    if 'username' in session:
        if request.method == 'POST':
            herbs = mongo.db.herbs
            herbs.insert({
                'username': session['username'],  #Now gets the username from session
                'herb_name': request.form.get('herb_name'),
                'herb_cure': request.form.get('herb_cure'),
                'herb_description': request.form.get('herb_description'),
                'herb_preparation': request.form.get('herb_preparation').splitlines(),
                'herb_usage': request.form.get('herb_usage').splitlines(),
                'herb_image': request.form.get('herb_image'),
                'date_added': today_string,
                'date_iso': today_iso})
            flash('Your Herb was successfully added')
            return redirect(url_for('all_herbs'))
        return render_template("add_herb.html",
                               session_name=session['username'])
    flash('You must be logged in to add a new herb')
    return redirect(url_for('login'))


@app.route('/edit_herb/<herb_id>', methods=['POST', 'GET'])
def edit_herb(herb_id):
    if 'username' in session:
        herb = mongo.db.herbs.find_one({'_id': ObjectId(herb_id)})
        if session['username'] == herb['username']:
            if request.method == 'POST':
                herbs = mongo.db.herbs
                herbs.update({'_id': ObjectId(herb_id)},
                               {'username': request.form.get('username'),
                                'herb_name': request.form.get('herb_name'),
                                'herb_cure': request.form.get('herb_cure'),
                                'herb_description': request.form.get('herb_description'),
                                'herb_preparation': request.form.get('herb_preparation'),
                                'herb_usage': request.form.get('herb_usage'),
                                'herb_image': request.form.get('herb_image'),
                                'your_review': request.form.get('your_review'),
                                'date_added': request.form.get('date_added'),
                                'update_iso': datetime.datetime.now()})
                flash(' You have Successfully Updated Your Herb', 'success')
                return redirect(url_for('my_herbs', herb=herb))
            return render_template('edit_herb.html',
                                   session_name=session['username'],
                                   herb=herb)
    flash('Sorry! You must be logged in first')
    return redirect(url_for('login'))


@app.route('/delete_herb/<herb_id>')
def delete_herb(herb_id):
    if 'username' in session:
        herbs = mongo.db.herbs.find_one({'_id': ObjectId(herb_id)})
        if session['username'] == herbs['username']:
            herbs = mongo.db.herbs.remove({'_id': ObjectId(herb_id)})
            return redirect(url_for('all_herbs'))
        flash('Sorry! You must be logged in first')
        return redirect(url_for('login'))
    flash('Sorry! You must be logged in first')
    return redirect(url_for('login'))


@app.route('/add_review', methods=['POST', 'GET'])
def add_review():
    today_string = datetime.datetime.now().strftime('%d/%m/%y')
    today_iso = datetime.datetime.now()
    if 'username' in session:
        if request.method == 'POST':
            reviews = mongo.db.reviews
            reviews.insert({
                'username': session['username'],
                'your_review': request.form.get('your_review'),
                'date_added': today_string,
                'date_iso': today_iso})
            flash('Your Review has been successfully added')
            return redirect(url_for('all_reviews'))
        return render_template("add_review.html",
                               session_name=session['username'])
    flash('You must be logged in to add a review')
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        time = datetime.datetime.now()
        existing_email = users.find_one({'email': request.form['userEmail']})
        if existing_email is None:
            hashpass = bcrypt.hashpw(request.form['userPassword'].
                                     encode('utf-8'), bcrypt.gensalt())
            users.insert({
                'name': request.form['username'].capitalize(),
                'email': request.form['userEmail'].lower(),
                'password': hashpass,
                'user_herbs': [],
                'reg_date': time
            })
            session['username'] = request.form['username']
            session['logged_in'] = True
            flash('Hello' + session['username'] +
                  'You have successfull signedup')
            return redirect(url_for('all_herbs',))
        flash('That email or username already exists')
        return render_template('signup.html')
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['userEmail']})
        if login_user:
            if bcrypt.checkpw(request.form['userPassword'].encode('utf-8'),
                              login_user['password']):
                session['username'] = login_user['name']
                session['logged_in'] = True
                flash('Welcome Back ' +
                      session['username'] + ' You are now Logged In')
                return redirect(url_for('index'))
            flash('This Username or Password is invalid')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    flash('You are now logged out')
    return redirect(url_for('login'))


# Account Settings
@app.route("/account_settings/<username>")
def account_settings(username):
    '''
    Account settings page - displays username,
    buttons for change_username, change_password
    and delete_account pages.
    '''
    users = mongo.db.users
    print("TESTING SOMETHING")
    print(users.find_one({'username': session['username']}))
    # prevents guest users from viewing the page
    if 'username' in session:
        users = mongo.db.users
    users.find_one({'username': session['username']})
    return render_template('account_settings.html',
                           username=username, title='Account Settings')


# Delete Account
@app.route("/delete_account/<username>", methods=['GET', 'POST'])
def delete_account(username):
    '''
    DELETE.
    Remove user's account from the database as well as all herbs
    created by this user. Before deletion of the account, user is asked
    to confirm it by entering password.
    '''
    # prevents guest users from viewing the form
    if 'username' in session:
        user = mongo.db.users.find_one({"name": username.capitalize()})
        print("xxxxxx")
        print("USERNAME", user)
    # checks if password matches existing password in database

        all_user_herbs = user.get("user_herbs")
        for herb in all_user_herbs:
            herbs = mongo.db.herbs
            herbs.remove({"_id": herb})
        # remove user from database,clear session and redirect to the home page
        flash("Your account has been deleted.")
        session.pop("username", None)
        users = mongo.db.users
        users.remove({"_id": user.get("_id")})
        return redirect(url_for("index"))
    else:
        flash("Password is incorrect! Please try again")
        return redirect(url_for("account_settings", username=username))


@app.route('/all_reviews')
def all_reviews():
    return render_template('all_reviews.html',
                           reviews=mongo.db.reviews.find().sort("_id", -1))


'''
1. Grab the herb._id and pass it into your addreview route.
2. Modify the add_review route so that it expects a herb_id, and so that when s review is added, it also adds a review.herb_id field into the database.
3. When displaying a herb, use reviews.find with "herb_id": herb_id to get all reviews that have that herb_id.`
'''
 

@app.errorhandler(404)
def page_not_found(error):
    app.logger.info(f'Page not found: {request.url}')
    return render_template('errors/404.html', error=error)


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)



