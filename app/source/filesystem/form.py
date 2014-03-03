from flask.ext.wtf import Form, TextField, ValidationError, \
                          Required, PasswordField
                          
""" 
Form element variable name should be start with 'src_'
"""
    
class SettingForm(Form):   
    src_ex_fs_path = TextField('Path', validators=[Required()])
