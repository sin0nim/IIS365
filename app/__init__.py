from flask import Flask, request, current_app
from config import Config
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib import sqla
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from app.admin.routes import HouseModelView, PurchaseModelView, AdminIndex

migrate = Migrate()
# login.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()
admin = Admin(name='Flask-Admin', index_view=AdminIndex(), template_mode = 'bootstrap4')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    
    from app.models import Users, House, Purchase
    
    from app.models import db, login
    
    admin.init_app(app)
    admin.add_view(sqla.ModelView(Users, db.session))
    admin.add_view(HouseModelView(House, db.session))
    admin.add_view(PurchaseModelView(Purchase, db.session))
    # admin.add_link(AdminIndex(name='Login/Logout', endpoint='admin.login_view'))
    
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.house import bp as house_bp
    app.register_blueprint(house_bp, url_prefix='/house')
    
    from app.purchase import bp as purchase_bp
    app.register_blueprint(purchase_bp, url_prefix='/purchase')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin', name='admin_panel', template_mode='bootstrap3')
    
    if not app.debug and not app.testing:
        '''
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config[    'MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        '''
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/rr.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('RealtyRadar startup')
    
    return app

# from app import routes, models
