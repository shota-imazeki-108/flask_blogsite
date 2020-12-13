from flask_wtf import FlaskForm
from wtforms import SubmitField


class GirlsGeneratePostForm(FlaskForm):
    # word = StringField('Word', validators=[DataRequired()])
    submit = SubmitField('Post')
