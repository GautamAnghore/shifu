from flask import Flask 
app = Flask(__name__)

#import views
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'some_Secret_key_XtksCaSEdc98'

from users import users
#from users import views

app.register_blueprint(users)