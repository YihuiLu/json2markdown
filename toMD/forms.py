# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class MDForm(FlaskForm):
    packets = TextAreaField('输入JSON/字典值')  # ,
    args = StringField('Extra Arg Values', validators=[Length(0, 200)])
    ultra = StringField('Extra Arg Default Names', validators=[Length(0, 200)])
    des = StringField('Function Description', validators=[Length(0, 200)])
    submit = SubmitField()
