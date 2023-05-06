from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class PostForm(FlaskForm):
    post = TextAreaField('Say Something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
