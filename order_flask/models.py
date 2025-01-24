from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


#ユーザー
class User(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    grade = db.Column(db.Integer, nullable=False)
    
    class_number = db.Column(db.Integer, nullable=False)
    
    number = db.Column(db.Integer, nullable=False)
    
    password = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


#メニュー一覧
class Menu(db.Model):
    
    __tablename__ = "menus"
    
    food_id = db.Column(db.Integer, primary_key=True)
    
    food_name = db.Column(db.String(50), nullable=False)
    
    price = db.Column(db.Integer, nullable=False)
    
    img = db.Column(db.String(100), nullable=False)
    
    order = db.relationship('Order', back_populates='food', cascade='all, delete-orphan')


#オーダー
class Order(db.Model):
    
    __tablename__ = 'orders'
    
    order_id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, nullable=False)
    
    food_id = db.Column(db.Integer,db.ForeignKey('menus.food_id', name='fk_order_food_id'))
    
    food = db.relationship('Menu', back_populates='order')