from flask import render_template, request, redirect, url_for, flash, Blueprint
from app import app
from werkzeug.exceptions import NotFound

@app.errorhandler(NotFound)
def show_404_page(error):
    msg = error.description
    print('エラー内容:',msg)
    return render_template('errors/404.html', msg=msg), 404