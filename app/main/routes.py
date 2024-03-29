# -*- coding: utf-8 -*-
from flask import render_template
# from flask import flash, redirect, url_for, current_app
# from app import db
from app.main import bp
# from app.forms import LoginForm, EditProfileForm, RegistrationForm
# from app.forms import PostForm
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from app.models import Users, House, Purchase
from flask import request
from werkzeug.urls import url_parse
# from datetime import datetime
# from app.email import send_password_reset_email


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index/', methods=['GET', 'POST'])
# @login_required
def index():
    '''
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    '''
    return render_template('index.html')
        # , title='Home Page' , form=form, next_url=next_url 
        # , prev_url=prev_url, posts=posts.items)

@bp.route('/user')
@login_required
def user():

    # page = request.args.get('page', 1, type=int)
    if current_user:
        print('*****last_seen ', current_user.last_seen.strftime('%d.%m.%Y %H:%M:%S'))
    
    return render_template('user.html', title='Profile', user=current_user)

'''
@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))

@bp.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], max_per_page=10, error_out=False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('explore.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
'''
