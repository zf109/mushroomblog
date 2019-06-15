from flask import flash, redirect, get_flashed_messages, request as requested, url_for, abort
from flask_login import current_user, login_user, logout_user, login_required
from mushroom.persistence import db_manager as m
from mushroom.persistence.data_model import Post
from flask.views import View
import bcrypt

from mushroom.templates import render
from mushroom.server_app import save_picture

from .forms import LoginForm, PostForm, RegistrationForm, UpdateAccountForm
from .config import Config as conf


def _hashpassword(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode('utf-8')


def _checkpassword(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def _render(template_path, get_flashed_messages=get_flashed_messages,
        current_user=current_user, url_for=url_for, *args, **kwargs):
    return render(template_path, get_flashed_messages=get_flashed_messages, current_user=current_user,
                url_for=url_for, *args, **kwargs)


class IndexView(View):
    def dispatch_request(self):
        """Index page """
        # user = {'nickname': 'EvilerPizza'} # Test
        posts = m.load_latest_posts(10)
        return _render('index.html', title='latest', user=current_user, posts=posts)


class RegisterView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = _hashpassword(form.password.data)
            m.create_user(username=form.username.data, nickname=form.nickname.data,
                     email=form.email.data, password=hashed_password)
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        return _render('register.html', title='Register', form=form)


class LoginView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        """Login page """
        form = LoginForm()
        if form.validate_on_submit():
            user = m.filter_user('username', requested.form['username'], first=True)
            if not user:
                error = 'Invalid Credentials. Please try again.'
                return _render('login.html', title='Sign In', form=form, error=error, get_flashed_messages=get_flashed_messages)
            if not _checkpassword(requested.form['password'], user.password):
                error = 'Invalid password. Please try again.'
                return _render('login.html', title='Sign In', form=form, error=error, get_flashed_messages=get_flashed_messages)
            else:
                flash(f'Hello, {user.nickname}!')
                login_user(user, remember=form.remember.data)
                return redirect('/home')
        if requested.method == "GET":
            return _render('login.html', title='Sign In', form=form)


class LogoutView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        """Logout"""
        logout_user()
        return redirect(url_for('home'))

class HomeView(View):
    def dispatch_request(self):
        posts = m.load_latest_posts(10)
        return _render('home.html', title='Home', posts=posts)


class AccountView(View):
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            m.save_user(current_user)
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        elif requested.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return _render('account.html', title='Account',
                            image_file=image_file, form=form)


class AboutView(View):
    @login_required
    def dispatch_request(self):
        return _render('about.html', title='About')


class PostDeleteView(View):
    methods=['POST']
    @login_required
    def dispatch_request(self, post_id):
        post = m.get_post(post_id)
        if post.author != current_user:
            abort(403)
        m.delete_post(post.id)
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('home'))


class PostDetailView(View):
    def dispatch_request(self, post_id):
        post = m.get_post(post_id)
        return _render('post_detail.html', title='Post Detail', post=post)


class PostCreateView(View):
    methods=['GET', 'POST']
    @login_required
    def dispatch_request(self):
        form = PostForm()
        if form.validate_on_submit():
            m.create_post(title=form.title.data, body=form.content.data, author=current_user)
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))
        return _render('post_create.html', title='New Post',
                            form=form, legend='New Post')        


class PostUpdateView(View):

    methods=['GET', 'POST']
    @login_required
    def dispatch_request(self, post_id):
        post = m.get_post(post_id)
        if post.author != current_user:
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.content.data
            m.save_post(post)
            flash('Your post has been updated!', 'success')
            return redirect(url_for('post', post_id=post.id))
        elif requested.method == 'GET':
            form.title.data = post.title
            form.content.data = post.body
        return _render('post_create.html', title='Update Post',
                            form=form, legend='Update Post')
