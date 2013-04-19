from flask.ext.wtf import Form, TextField, ValidationError, \
                          Required, PasswordField, BooleanField
                          
""" 
Form element variable name should be start with 'src_'
"""
    
class SettingForm(Form):   
    src_host = TextField('Host', validators=[Required()])
    src_port = TextField('Port', validators=[Required()], default=27017)
    src_ex_db = TextField('Database')
    src_ex_coll = TextField('Collection')
    src_username = TextField('Username')
    src_password = PasswordField('Password')
    src_ex_repairdb = BooleanField('Repair database')
