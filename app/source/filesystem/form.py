from flask.ext.wtf import Form, TextField, ValidationError,\
                          Required, PasswordField
                          
                          
    
class SettingForm(Form):
    field_path = TextField('Path', validators=[Required()])