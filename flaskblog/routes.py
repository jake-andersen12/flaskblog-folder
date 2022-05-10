import os
import secrets
from PIL import Image
from flask import  render_template, url_for, flash, redirect, request
from wtforms import form
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required

##this is a list of dictionaries.
posts = [
    {'author': 'Jake Andersen',
    'title': 'Blog Post 1',
    'content': 'First post content',
    'date_posted': 'October 11, 2021'
    },
    {'author': 'Emillie Whitlock',
    'title': 'Blog Post 2',
    'content': 'Second post content',
    'date_posted': 'October 15, 2021'
    },
       {'author': 'Sean Connery',
    'title': 'Playing Indiannas Father',
    'content': 'It was a surreal experience...',
    'date_posted': 'October 12, 2021'
    }
]

@app.route('/')
@app.route('/home')
@app.route('/home2')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
   return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in!', 'success') #'success' is the bootstrap class
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):     #user.password checks the database. form.password.data checks what was entered on the form.
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next') #args is a dictionairy, but you don't want to access it using square brackets because if a next doesn't exist, it will return an error. That's why we use the get() method instead.
                return redirect(next_page) if next_page  else redirect(url_for('home')) #this is a turnary conditional in Python.
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required  #this is a decorator from flask_login. It adds it to our account route. This let's the extension know that we need to login in order to access this route. But you also need to tell it where the extenstion is located (done on the __init__.py file)
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file=image_file, form=form)