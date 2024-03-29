# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app.models import db
from app.auth import bp
from .forms import LoginForm, EditProfileForm, RegistrationForm
from .forms import ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from app.models import Users
from flask import request
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        user.last_seen = datetime.utcnow()
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', title='Register')

@bp.route('/reg_an', methods=['GET', 'POST'])
def reg_an():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Congratulations, you are now a registered user!')
        save_register(form)
        return redirect(url_for('auth.login'))
    else:
        flash('Error! Form is not validated.')
    return render_template('auth/reg_an.html', title='Register_agency', form=form)

@bp.route('/reg_rl', methods=['GET', 'POST'])
def reg_rl():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Congratulations, you are now a registered user!')
        save_register(form)
        return redirect(url_for('auth.login'))
    else:
        flash('Error! Form is not validated.')
    return render_template('auth/reg_rl.html', title='Register_realter', form=form)

@bp.route('/reg_ow', methods=['GET', 'POST'])
def reg_ow():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Congratulations, you are now a registered user!')
        save_register(form)
        return redirect(url_for('auth.login'))
    else:
        flash('Error! Form is not validated.')
    return render_template('auth/reg_ow.html', title='Register_owner', form=form)

@bp.route('/reg_us', methods=['GET', 'POST'])
def reg_us():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Congratulations, you are now a registered user!')
        save_register(form)
        return redirect(url_for('auth.login'))
    else:
        flash('Error! Form is not validated.')
    return render_template('auth/reg_us.html', title='Register_user', form=form)

def save_register(form):
    user = Users(username=form.username.data, user_type=form.user_type.data, email=form.email.data, phone=form.phone.data, address=form.address.data, about=form.about.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    return


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
    return render_template('auth/edit_profile.html', title='Edit Profile', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password!')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = Users.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

