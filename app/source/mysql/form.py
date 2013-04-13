from flask.ext.wtf import Form, TextField, ValidationError, \
                          Required, PasswordField
                          
""" 
Form element variable name should be start with 'src_'
"""
    
class SettingForm(Form):   
    src_msql_host = TextField('Host', validators=[Required()])
    src_msql_port = TextField('Port', validators=[Required()], default=3306)
    src_msql_db = TextField('Database')
    src_msql_username = TextField('Username', validators=[Required()])
    src_msql_password = PasswordField('Password')
