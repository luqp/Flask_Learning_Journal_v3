from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class JournalForm(FlaskForm):

    title = StringField(
        'Title',
        validators=[DataRequired()],
        description="text"
    )

    date = DateField(
        'Date',
        format="%Y-%m-%d",
        description="date"
    )

    time_spent = IntegerField(
        'Time Spent',
        validators=[DataRequired()],
        description="text"
    )

    learned = TextAreaField(
        'What I Learned?',
        validators=[DataRequired()]
    )

    resources = TextAreaField(
        'Resources to Remember',
        validators=[DataRequired()]
    )
