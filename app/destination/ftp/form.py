from flask.ext.wtf import Form, TextField, ValidationError, \
                          Required, PasswordField
                          
""" 
Form element variable name should be start with 'dst_'
"""
    
class SettingForm(Form):   
    dst_ftp_path = TextField('Path', validators=[Required()])
    dst_ftp_host = TextField('Path', validators=[Required()])
    dst_ftp_port = TextField('Path', validators=[Required()], default=21)
    dst_ftp_username = TextField('Path', validators=[Required()])
    dst_ftp_password = TextField('Path', validators=[Required()])
