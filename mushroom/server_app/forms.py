"""
    Create different forms for user to fill in
"""
from flask_wtf import Form
from flask_login import current_user
from wtforms import StringField, BooleanField, TextAreaField, \
    SubmitField, PasswordField, FileField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
import mushroom.persistence.db_manager as m
from mushroom.persistence.db_manager import filter_user

class RegistrationForm(Form):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    nickname = StringField('Nickname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        users = m.filter_user('username', username.data)
        if users:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        users = m.filter_user('email', email.data)
        if users:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember = BooleanField('remember', default=False)


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class UpdateAccountForm(Form):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = filter_user(field='username', value=username.data, first=True)
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = filter_user(field='email', value=email.data, first=True)
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
