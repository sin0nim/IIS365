# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, current_app, session, request, flash

from flask_login import login_required, current_user
from .forms import LoginForm
from app.models import Users, House, Purchase, db

from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual
# from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader, DEFAULT_PAGE_SIZE
from flask_admin.babel import gettext

from app.admin import bp
from app.models import Users

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

class UsersModelView(sqla.ModelView):
    can_delete = False  # disable model deletion
    can_create = False  # disable model create
    can_edit = False    # disable model edit
    column_exclude_list = ['password', ] # don't view
    
    
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

class MyHouseModelView(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    column_searchable_list = ['rooms', 'living_area', 'nfloor', 'rental_period', 'price']
    column_filters = ['rooms', 'living_area', 'nfloor', 'rental_period', 'price']
    create_modal = True
    edit_modal = True
    can_export = True   # включить csv экспорт вида модели
    
    '''
    form_ajax_refs = {
        'active_user': QueryAjaxModelLoader('user', db.session, Users, filters=["is_active=True"])
    }
    
    form_ajax_refs = {
        'user': {
            'fields': ['username', 'user_type', 'email'],
            'page_size': 10
        }
    }
     '''
    
    @expose('/')
    def index(self):
        realty = House.query.filter_by(holder=current_user.id).all()
        return self.render('/admin/my_houses.html', realty=realty)
   
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

class MyPurchaseModelView(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    column_searchable_list = ['rooms', 'living_area', 'nfloor', 'price']
    column_filters = ['rooms', 'living_area', 'nfloor', 'price']
    create_modal = True
    edit_modal = True
    can_export = True   # включить csv экспорт вида модели
    
    @expose('/')
    def index(self):
        realty = Purchase.query.filter_by(owner=current_user.id).all()
        return self.render('/admin/my_purchases.html', realty=realty)
    
    '''
    form_ajax_refs = {
        'active_user': QueryAjaxModelLoader('username', db.session, Users, filters=["is_active=True"])
    }
    '''
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))    
   

class HouseModelView(sqla.ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    column_searchable_list = ['rooms', 'living_area', 'nfloor', 'rental_period', 'price']
    column_filters = ['rooms', 'living_area', 'nfloor', 'rental_period', 'price']

    '''
    form_ajax_refs = {
        'Users': {
            'fields': ['username', 'user_type', 'last_seen'],
            'page_size': 10
        }
    }
    '''
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

class PurchaseModelView(sqla.ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    column_searchable_list = ['rooms', 'living_area', 'nfloor', 'price']
    column_filters = ['rooms', 'living_area', 'nfloor', 'price']
    '''
    form_ajax_refs = {
        'Users': {
            'fields': ['username', 'user_type', 'last_seen'],
            'page_size': 10
        }
    }
    '''
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))    
   
class AdminIndex(AdminIndexView):
    @bp.route('/')
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return self.render('admin/index.html')
    
    # def get_class_name(self):
    #     return self.__class__.__name__
    
    @bp.route('/home/')
    @expose('/home/')
    def main_view(self):
        print('*****AdminIndex - expose-main_view')
        # login.logout_user()
        return redirect(url_for('index'))

class UserFilter(BaseSQLAFilter):
    def __init__(self, column, name, options=None, data_type=None):
        super(UserFilter, self).__init__(name, options, data_type)
        
        self.column = column

class UserEqualFilter(UserFilter):
    def apply(self, query, value):
        return query.filter(self.column == value)
    
    def operation(self):
        return gettext('equals')
    
    #, Вы можете проверить значения. Если значение недействительно,
    # вернуть `False`, поэтому фильтр будет проигнорирован.
    def validate(self, value):
        return True # ?
    
    # Вы можете "очистить" значения, прежде чем они будут
    # переданы на уровень доступа к вашим данным
    def clean(self, value):
        return value

class UserGreaterFilter(UserFilter):
    def apply(self, query, value):
        return query.filter(self.column >= value)
    
    def operation(self):
        return gettext('greater')

class UserLessFilter(UserFilter):
    def apply(self, query, value):
        return query.filter(self.column <= value)
    
    def operation(self):
        return gettext('less')
    '''
        form = LoginForm(request.form):
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
            
            if username == 'susan' and password == 'cat':
                login.login_user(user)
                redirect(url_for('.index'))
            else:
                flash('Неправильный логин или пароль')
                return redirect(url_for('.login_view'))
            
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
    '''
