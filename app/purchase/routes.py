# -*- coding: utf-8 -*-
from app.purchase import bp
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)
from sqlalchemy import text
from flask_login import login_required, current_user
from app.models import Purchase, db
from .forms import PurchaseSearchForm, PurchaseCreateForm

fields_condition = {'type': 'type={}', 'rooms': 'rooms={}', 'nfloor': 'nfloor={}', 'living_area_from': 'living_area>={}', 'living_area_to': 'living_area<={}', 'user_type': "users.id=hse.owner AND users.user_type='{}'", 'price_from': 'price>={}', 'price_to': 'price<={}', 'prepay_from': 'prepay>={}', 'prepay_to': 'prepay<={}', 'rental_period': 'rental_period={}', 'address': "address='{}'", 'actual_date_from': "actual_date>='{}'", 'actual_date_to': "actual_date<='{}'",}
# def log_error(*args, **kwargs):
#     current_app.logger.error(*args, **kwargs)


@bp.route('/', methods=['GET'])
@bp.route('/index/', methods=['GET', 'POST'])
def index(object_list=None):
    form = PurchaseSearchForm()
    houses = None
    if request.method == 'POST':
        # and form.validate_on_submit():
        filter_list = []
        for  par in form.data:
            if par == 'submit' or par == 'csrf_token':
                continue
            if form.data[par] is not None and form.data[par]:
                if isinstance(form.data[par], dict):
                    par_str = ''
                    for key, value in form.data[par].items():
                        if value:
                            if par_str != '':
                                par_str += ' OR '
                            par_str += par + '=' + key[1:]
                    if par_str != '':
                        filter_list.append('(' + par_str + ')')
                else:
                    filter_list.append(fields_condition[par].replace('{}',str(form.data[par])))
        filters = ''
        if len(filter_list) > 1:
            filters = ' AND '.join(filter_list)
        elif len(filter_list) > 0:
            filters = filter_list[0]
        print('*****', filters)
        
        houses = object_list
        houses = db.session.execute(text('select * from house, users where ' + filters))
        # db.session.commit()
        if houses is None:
            flash('По вашему запросу ничего не найдено. Попробуйте изменить условия поиска.')
            return redirect(url_for(pch.index))
        
    return render_template('purchase/index.html', object_list=houses, form=form)


@bp.route('/insert/', methods=['GET', 'POST'])
def insert():
    form = PurchaseCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        fd = form.data
        del fd['submit']
        del fd['csrf_token']
        print('*****', form.data)
        house = House(**fd)
        db.session.add(house)
        db.session.commit()
        flash('Запись была успешно добавлена!', 'success')
        return redirect(url_for('pch.index'))
    return render_template('purchase/insert.html', form=form)

@bp.route('/buy/')
@login_required
def buy():
    page = request.args.get('page', 1, type=int)
    buys = current_user.buy_offers().paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('pch.buy', page=buys.next_num) if buys.has_next else None
    prev_url = url_for('pch.buy', page=buys.prev_num) if buys.has_prev else None
    return render_template('user.html', title='Rent Offers', user=current_user, posts=buys.items, next_url=next_url, prev_url=prev_url)
    #######################
