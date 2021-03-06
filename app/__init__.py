from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment



app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
migrate = Migrate(app, db)
moment = Moment(app)



from app.auth import blueprint as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app.reagent import blueprint as reagent_blueprint
app.register_blueprint(reagent_blueprint, url_prefix='/reagent_add')

from app.order import blueprint as order_blueprint
app.register_blueprint(order_blueprint, url_prefix='/order')

from app.admin import blueprint as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')
