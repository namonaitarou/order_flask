from flask import Flask
from flask_migrate import Migrate
from models import db, User
from flask_login import LoginManager
from auth.views import auth_bp
from menu.views import menu_bp
from order.views import order_bp

app = Flask(__name__)

app.config.from_object("config.Config")

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_message = "認証していません:ログインしてください"

login_manager.login_view = "auth.login"

app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from views import *

if __name__ == "__main__":
    app.run()