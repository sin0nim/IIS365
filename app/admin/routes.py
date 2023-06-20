# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, current_app, session, request, flash

from flask_login import login_required, current_user
from .forms import LoginForm
from app.models import Users, House, Purchase, db

from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib import sqla

from app.admin import bp

from app import admin


'''
@bp.route('/', methods=['GET'])
@bp.route('/index/', methods=['GET', 'POST'])
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    
    menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.logout', 'title': 'Выйти'}]
        
    return render_template('admin/index.html', menu=menu, title='Админ-панель')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")
        
    return render_template('admin/login.html', title='Админ-панель')

@bp.route('/logout')
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))

def logout_admin():
    session.pop('admin_logged', None)

def login_admin():
    session['admin_logged'] = True

def isLogged():
    return True if session.get('admin_logged') else False
'''
def get_user(user):
    return db.session.query(Users).filter_by(username=user).first()

class HouseModelView(sqla.ModelView):
    def is_accessible(self):
        print('*****HouseModelViev - is_accessible', current_user.is_authenticated)
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        print('*****HouseModelView - inaccessible_callback')
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin.login_view', next=request.url))

class PurchaseModelView(sqla.ModelView):
    def is_accessible(self):
        print('*****PurchaseModelView - is_accessible', current_user.is_authenticated)
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        print('*****PurchaseModelViev - inaccessible_callback')
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin.login_view', next=request.url))    
   

class AdminIndex(AdminIndexView):
    # @bp.route('/')
    @expose('/')
    def index(self):
        # if not current_user.is_authenticated:
        #     return redirect(url_for('.login_view'))
        return self.render('admin/index.html')
    
    def get_class_name(self):
        return self.__class__.__name__
    
    @bp.route('/login/', methods=['GET', 'POST'])
    @expose('/login/')
    def login_view(self):
        print('*****AdminIndex - expose-login_view')
        if current_user.is_authenticated:
            logout_user()
            return redirect(url_for('admin.index'))
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate_on_submit():
            # username = form('username')
            # password = form('password')
            # print('*****username =', username, '  password =',password)
            user = get_user(form.username.data)
            print('##### user =', user)
            if not user is None:
                login_user(user)
                return redirect(url_for('admin.index'))
            else:
                flash('Wrong username')
                return redirect(url_for('admin.login_view'))
            # проверка введённых данных
            '''
            if username == 'susan' and password == 'cat':
                login.login_user(user)
                redirect(url_for('.index'))
            else:
                flash('Неправильный логин или пароль')
                return redirect(url_for('.login_view'))
            '''
        return self.render('admin/login.html', form=form)
        # self._template_args['form'] = form
        # return super(AdminIndex, self).index()
    
    @bp.route('/logout/')
    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('admin.index'))
    
    @bp.route('/register/', methods=['GET', 'POST'])
    @expose('/register/', methods=['GET', 'POST'])
    def register_view(self):
        return self.render('admin/register.html')
    
    @bp.route('/reset_password_request/', methods=['GET', 'POST'])
    def reset_password_request_view(self):
        return self.render('admin/reset_password_request.html')
    
    def is_accessiblle(self):
        return current_user.is_authenticated
