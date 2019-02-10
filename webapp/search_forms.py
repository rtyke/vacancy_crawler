from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SmallSearchForm(FlaskForm):
    search = StringField(
        '',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField('Найти', render_kw={"class": "btn btn-primary"})


class SearchForm(FlaskForm):
    search = StringField(
        'Поисковое слово',
        # validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    city = StringField(
        '',
        render_kw={"class": "form-control"}
    )
    spec = SelectField(
        'Специализация',
        choices=[('0', 'Любая'), ('1', 'IT'), ('2', 'Медицина'), ('3', 'Банки'), ('4', 'Страхование'), ('5', 'Юристы'), ('6', 'Маркетинг, PR'), ('7', 'Бухгалтерия'), ('8', 'Кадры')]
    )
    submit = SubmitField('Найти', render_kw={"class": "btn btn-primary"})


