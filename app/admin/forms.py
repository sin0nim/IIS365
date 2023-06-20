from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Users

'''
class LoginForm(FlaskForm):
    user = StringField('Имя', validators=[DataRequired()])
    psw = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
'''
class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
    
