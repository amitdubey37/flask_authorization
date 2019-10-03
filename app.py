from flask import render_template, redirect, session, flash, url_for
from myproject import app
from myproject.forms import RegistrationForm, LoginForm
from flask_login import login_required, login_user, logout_user
from myproject.models import User

@app.route("/", methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username, email, password)
        user.save()
        flash("User Created Successflully!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            session['user'] = user.json()
            return redirect(url_for('welcome'))
        else:
            flash('Invalid Credentials')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You're logged out!")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
