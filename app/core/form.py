from flask.ext.wtf import Form, TextField, ValidationError, \
                          Required, PasswordField, BooleanField
                          
                          
    
class LoginForm(Form):
    field_username = TextField('Username', validators=[Required()])
    field_password = PasswordField('Password', validators=[Required()])

class OptionForm(Form):
    opt_cron = TextField('Cron')
    opt_compress = BooleanField('Compress')