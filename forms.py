from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class ReviewForm(FlaskForm):
    content = TextAreaField("Review", validators=[DataRequired()])
    rating = IntegerField("Rating", validators=[DataRequired(), NumberRange(min=1, max=5)])