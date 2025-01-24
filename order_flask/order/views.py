from flask import render_template, request, redirect, url_for, flash, Blueprint
from models import db, Menu, User, Order
from forms import MenuForm, LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

order_bp = Blueprint('order', __name__, url_prefix='/order')


#現ログインユーザーの注文の品RD
@order_bp.route("/order", methods=["GET", "POST"])
@login_required
def order():
    
    orders = Order.query.filter_by(student_id=current_user.id).all()
    
    return render_template("order/order.html", orders=orders)

@order_bp.route("/order/delete/<int:order_id>", methods=["GET", "POST"])
@login_required
def order_delete(order_id):
    
    order = Order.query.get_or_404(order_id)
    
    db.session.delete(order)
    db.session.commit()
    
    return redirect(url_for("order.order"))