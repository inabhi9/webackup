from flask.ext.wtf import Form, TextField, ValidationError, \
                          Required, PasswordField
                          
""" 
Form element variable name should be start with 'src_'
"""
    
class SettingForm(Form):   
    src_host = TextField('Host', validators=[Required()])
    src_port = TextField('Port', validators=[Required()], default=3306)
    src_ex_db = TextField('Database')
    src_username = TextField('Username', validators=[Required()])
    src_password = PasswordField('Password')
