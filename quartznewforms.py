# forms.py

from wtforms import StringField, SelectField, Form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class QuartzSearchForm(Form):
    choices = [('QuartzSerialNumber', 'QuartzSerialNumber'),
               ('QuartzType', 'QuartzType'),
               ('ToolName', 'ToolName')]
    select = SelectField('Search for Quartz Parts:', choices=choices)
    search = StringField('')

class QuartzForm(Form):
    quartz_condition_types = [('New', 'New'),
                   ('Cleaned', 'Cleaned'),
                   ('Repaired', 'Repaired')
                   ]
    quartzserialnumber = StringField('QuartzSerialNumber')
    title = StringField('Title')
    quartz_type = StringField('QuartzType')
    micronpart = StringField('MicronPart')
    installation_date = StringField('InstallationDate')
    toolname = StringField('ToolName')
    quartz_condition_type = SelectField('Quartz_Condition', choices=quartz_condition_types)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(),Email(message='Invalid email'), Length(max=80)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password =  PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])