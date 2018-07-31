from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, AnyOf, Length


class RequestedWord(FlaskForm):
    word = StringField('Word', validators=[DataRequired(), Length(min=2, max=30)])
    language = StringField('Language',
                           validators=[DataRequired(), AnyOf(values=['en', 'es'])])
    submit = SubmitField('Submit word')
