from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from models import Menu, User
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#メニューフォーム
class MenuForm(FlaskForm):
    
    food_name = StringField('メニュー名', validators=[DataRequired('メニュー名は必須入力です。'), 
                            Length(max=50, message='50文字以下で入力してください。')])
    
    price = IntegerField('値段', validators=[DataRequired('値段は必須入力です。'),
                            NumberRange(min=0, max=2000, message='0以上2000以下の整数を入力してください')])
    
    img = FileField('画像ファイル', validators=[DataRequired('画像ファイルは必須アップロードです')])
    
    submit = SubmitField('送信')
    
    def validate_food_name(self, food_name):
        
        menu = Menu.query.filter_by(food_name=food_name.data).first()
        
        if menu:
            raise ValidationError(f"メニュー名'{menu.img}'は既に存在します。別のメニュー名を入力してください。")
        
    def validate_img(self, img):
        filename = secure_filename(img.data.filename)
        print(filename)
        file_extension = os.path.splitext(filename)[1].lower().lstrip('.')
        print(file_extension)
        
        menu = Menu.query.filter_by(img=filename).first()
        
        if menu:
            raise ValidationError(f"画像'{filename}'は既に存在します。別の画像名にしてください。")
        
        if file_extension not in ALLOWED_EXTENSIONS:
            raise ValidationError(f"画像'{filename}'の拡張子が誤りです。確認してみてください")

#ログインフォーム
class LoginForm(FlaskForm):
    
    grade = RadioField('学年', choices=[(1, '一年生'),(2, '二年生'),(3, '三年生'),(4, 'その他')],
                        validators=[DataRequired('学年は必須入力です')]) 
    
    class_number = IntegerField('クラス名', validators=[DataRequired('クラス名は必須入力です'),
                                    NumberRange(min=0, max=10, message='0以上10以下の整数を入力してください')])
    
    number = IntegerField('番号', validators=[DataRequired('番号は必須入力です'),
                                    NumberRange(min=0, max=40, message='0以上40以下の整数を入力してください')])
    
    password = PasswordField('パスワード', validators=[Length(4,10,
                                    'パスワードの長さは４文字以上１０文字以内です')])
    
    submit = SubmitField('ログイン')
    
    def validate_password(self, password):
        if not (any(c.isalpha() for c in password.data) and any(c.isdigit() for c in password.data) and any(c in '!@#$%^&*()' for c in password.data)):
            raise ValidationError('パスワードに「英数字と記号:!@#$%^&*()」を含める必要があります')


#サインアップフォーム
class SignUpForm(LoginForm):
    
    submit = SubmitField('サインアップ')