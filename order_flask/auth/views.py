from flask import render_template, request, redirect, url_for, flash, Blueprint
from models import db, Menu, User, Order
from forms import MenuForm, LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


#ログイン
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
    
        grade = form.grade.data
        class_number = form.class_number.data
        number = form.number.data
        password = form.password.data
        
        user = User.query.filter_by(grade=grade, class_number=class_number, number=number).first()
        
        if user is not None and user.check_password(password):
            
            login_user(user)
            
            return redirect(url_for("menu.index"))
        
        flash("認証不備です")
    
    return render_template("auth/login_form.html", form=form)

#ログアウト
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    
    flash("ログアウトしました")
    
    return redirect(url_for("auth.login"))

#サインアップ
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()
    
    if form.validate_on_submit():
        
        grade = form.grade.data
        class_number = form.class_number.data
        number = form.number.data
        password = form.password.data
        
        user_check = User.query.filter_by(grade=grade, class_number=class_number, number=number).first()
        if user_check is not None:
            flash('このユーザーはすでに存在します')
            return redirect(url_for('auth.register'))
        
        user = User(grade=grade, class_number=class_number, number=number)
        
        
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash("ユーザー登録しました")
        
        return redirect(url_for("auth.login"))
    
    return render_template("auth/register_form.html", form=form)