from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from models import db, Menu, User, Order
from forms import MenuForm, LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')


#adminと他者のメニュー表示
@menu_bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    
    menus = Menu.query.all()
    orders = Order.query.all()
    
    if request.method == "POST":
        student_id = current_user.id
        food_id = request.form["food_id"]
        
        order = Order(student_id=student_id, food_id=food_id)
        
        db.session.add(order)
        db.session.commit()
        
        return redirect(url_for("menu.index"))
    
    if current_user.grade == 4 and current_user.class_number == 1 and current_user.number == 1:
        return render_template("menu/admin_index.html", orders=orders)
    else:
        return render_template("menu/index.html", menus=menus)

#全ログインユーザーの注文確認
@menu_bp.route("/menu_index")
@login_required
def admin_index():
    
    menus = Menu.query.all()
    
    return render_template("menu/menu_index.html", menus=menus)


#メニューのCRUD
@menu_bp.route("/menu/create", methods=["GET", "POST"])
@login_required
def menu_create():
    form = MenuForm()
    
    if form.validate_on_submit():
        
        food_name = form.food_name.data
        price = form.price.data
        img = form.img.data
        
        filename = secure_filename(img.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        img.save(file_path)
        
        
        menu = Menu(food_name=food_name, price=price, img=filename)
        db.session.add(menu)
        db.session.commit()
        
        flash('登録しました。')
        
        return redirect(url_for("menu.admin_index"))
    
    return render_template("menu/menu_create_form.html", form=form)

@menu_bp.route("/menu/update/<int:food_id>", methods=["GET", "POST"])
@login_required
def menu_update(food_id):
    
    target_data = Menu.query.get_or_404(food_id)
    
    form = MenuForm(obj=target_data)
    
    if request.method == "POST" and form.validate():
        target_data.food_name = form.food_name.data
        target_data.price = form.price.data
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], target_data.img)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        img = form.img.data
        filename = secure_filename(img.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        img.save(file_path)
        target_data.img = filename
        
        db.session.commit()
        
        flash('変更しました')
        
        return redirect(url_for("menu.admin_index"))
    
    return render_template("menu/menu_update_form.html", form=form, edit_id = target_data.food_id)

@menu_bp.route("/menu/delete/<int:food_id>")
@login_required
def menu_delete(food_id):
    
    menu = Menu.query.get_or_404(food_id)
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], menu.img)
    os.remove(file_path)
    
    db.session.delete(menu)
    db.session.commit()
    
    return redirect(url_for("menu.admin_index"))