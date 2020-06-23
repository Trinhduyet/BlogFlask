
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
import random
from flaskblog import mail
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, ChangePasswordForm,RequestResetForm)
from flaskblog.users.utils import save_picture
users = Blueprint('users', __name__)



def send_reset_email(user):
    random_code = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
    txt = "code {} author"
    txtbody = txt.format(random_code)
    msg = Message('Password Reset Request',
                  sender='trinhnv.hvitclan@gmail.com',
                  recipients=[user.email])
    msg.body = txtbody
    mail.send(msg)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)

        # hasing passs  
        # user = User(username=form.username.data,
        # hasing passs            email=form.email.data)
        # user.set_password(form.password.data)             
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # check hasing pass
        # user = User.query.filter_by(username=form.username.data).first()
        # if user and user.check_password(form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        email= form.email.data
        #if user and user.password == form.password.data:
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login_user(user)
            # send_reset_email(user)
            return redirect(url_for('users.author_mail',email=email))
            # next_page = request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email  and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Mail     


@users.route("/change-pwd", methods=['GET', 'POST'])
@login_required
def account():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if user and form.password.data == form.re_password.data:
            user.password = form.password.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
        else:
            flash('Your password not match!', 'danger')
        return redirect(url_for('users.account'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Change Password', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/author_mail", methods=['GET', 'POST'])
def author_mail():
    random_code = '123456'
    email = request.args['email']
    user = User.query.filter_by(email=email).first()
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        if random_code == form.emailcode.data:
            login_user(user)
            return redirect(url_for('main.home'))
    return render_template('author_mail.html', title='very Code', form=form)

