# Delete Account
@app.route("/delete_account/<username>", methods=['GET', 'POST'])
def delete_account(username):
    '''
    DELETE.
    Remove user's account from the database as well as all recipes
    created by this user. Before deletion of the account, user is asked
    to confirm it by entering password.
    '''
    # prevents guest users from viewing the form
    if 'username' not in session:
        flash('You must be logged in to delete an account!')
    users = mongo.db.users
    users.find_one({"username": username})
    # checks if password matches existing password in database
    if check_password_hash(user["password"],
                           request.form.get("confirm_password_to_delete")):
        # Removes all user's recipes from the Database
        all_user_recipes = user.get("user_recipes")
        for recipe in all_user_recipes:
            recipes_coll.remove({"_id": recipe})
        # remove user from database,clear session and redirect to the home page
        flash("Your account has been deleted.")
        session.pop("username", None)
        users_coll.remove({"_id": user.get("_id")})
        return redirect(url_for("home"))
    else:
        flash("Password is incorrect! Please try again")
        return redirect(url_for("account_settings", username=username))


# Account Settings
@app.route("/account_settings/<username>")
def account_settings(username):
    '''
    Account settings page - displays username,
    buttons for change_username, change_password
    and delete_account pages.
    '''
    # prevents guest users from viewing the page
    if 'username' not in session:
        flash('You must be logged in to view that page!')
    username = users_coll.find_one({'username':
                                    session['username']})['username']
    return render_template('account_settings.html',
                           username=username, title='Account Settings')


# Change username
@app.route("/change_username/<username>", methods=['GET', 'POST'])
def change_username(username):
    '''
    UPDATE.
    Allows user to change the current username.
    It calls the ChangeUsernameForm class from forms.py.
    Checks if the new username is unique and not exist in database,
    then clear the session and redirect user to login page.
    '''
    # prevents guest users from viewing the form
    if 'username' not in session:
        flash('You must be logged in to change username!')
    users = users_coll
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        # checks if the new username is unique
        registered_user = users.find_one({'username':
                                         request.form['new_username']})
        if registered_user:
            flash('Sorry, username is already taken. Try another one')
            return redirect(url_for('change_username',
                                    username=session["username"]))
        else:
            users.update_one(
                {"username": username},
                {"$set": {"username": request.form["new_username"]}})
        # clear the session and redirect to login page
        flash("Your username was updated successfully.\
                    Please, login with your new username")
        session.pop("username",  None)
        return redirect(url_for("login"))

    return render_template('change_username.html',
                           username=session["username"],
                           form=form, title='Change Username')


# Change password
@app.route("/change_password/<username>", methods=['GET', 'POST'])
def change_password(username):
    '''
    UPDATE.
    Allows user to change the current password.
    It calls the ChangePasswordForm class from forms.py.
    Checks if the current password is correct, validate new password.
    Then if new password matchs confirm password field,
    insert it to the database.
    '''
    # prevents guest users from viewing the form
    if 'username' not in session:
        flash('You must be logged in to change password!')
    users = users_coll
    form = ChangePasswordForm()
    username = users.find_one({'username': session['username']})['username']
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get("confirm_new_password")
    if form.validate_on_submit():
        # checks if current password matches existing password in database
        if check_password_hash(users.find_one({'username': username})
                               ['password'], old_password):
            # checks if new passwords match
            if new_password == confirm_password:
                # update the password and redirect to the settings page
                users.update_one({'username': username},
                                 {'$set': {'password': generate_password_hash
                                           (request.form['new_password'])}})
                flash("Success! Your password was updated.")
                return redirect(url_for('account_settings', username=username))
            else:
                flash("New passwords do not match! Please try again")
                return redirect(url_for("change_password",
                                        username=session["username"]))
        else:
            flash('Incorrect original password! Please try again')
            return redirect(url_for('change_password',
                            username=session["username"]))
    return render_template('change_password.html', username=username,
                           form=form, title='Change Password')

