from flask.ext.wtf import Form, TextField, ValidationError, \
                          Required, PasswordField
                          
""" 
Form element variable name should be start with 'dst_'
"""
    
class SettingForm(Form):   
    dst_ex_path = TextField('Path', validators=[Required()])
    dst_host = TextField('Path', validators=[Required()])
    dst_port = TextField('Path', validators=[Required()], default=21)
    dst_username = TextField('Path', validators=[Required()])
    dst_password = TextField('Path', validators=[Required()])
