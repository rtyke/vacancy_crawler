from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField(
        '',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField('Найти', render_kw={"class": "btn btn-primary"})


