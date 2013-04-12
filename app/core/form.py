from flask.ext.wtf import Form, TextField, ValidationError,\
                          Required, PasswordField
                          
                          
    
class LoginForm(Form):
    field_username = TextField('Username', validators=[Required()])
    field_password = PasswordField('Password', validators=[Required()])