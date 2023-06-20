# -*- coding: utf-8 -*-
from app.house import bp
from flask import (
    # Blueprint,
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
from app.models import House, db
from .forms import HouseSearchForm, HouseCreateForm

fields_condition = {'type': 'type={}', 'rooms': 'rooms={}', 'nfloor': 'nfloor={}', 'living_area_from': 'living_area>={}', 'living_area_to': 'living_area<={}', 'user_type': "users.id=hse.holder AND users.user_type='{}'", 'price_from': 'price>={}', 'price_to': 'price<={}', 'prepay_from': 'prepay>={}', 'prepay_to': 'prepay<={}', 'rental_period': 'rental_period={}', 'address': "address='{}'", 'actual_date_from': "actual_date>='{}'", 'actual_date_to': "actual_date<='{}'",}


@bp.route('/', methods=['GET'])
@bp.route('/index/', methods=['GET', 'POST'])
def index(object_list=None):
    form = HouseSearchForm()
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
        print('*****filters =', filters)
        houses = db.session.execute(text('select * from house, users where ' + filters)).all()
        if houses is None:
            flash('По вашему запросу ничего не найдено. Попробуйте изменить условия поиска.')
            return redirect(url_for(hse.index))

        print('##### house/index = houses[] = ', *houses)
    return render_template('house/index.html', object_list=houses, form=form)


@bp.route('/insert/', methods=['GET', 'POST'])
def insert():
    form = HouseCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        fd = form.data
        del fd['submit']
        del fd['csrf_token']
        print('****', form.data)
        house = House(**fd)
        db.session.add(house)
        db.session.commit()
        flash('Запись была успешно добавлена!', 'success')
        return redirect(url_for('hse.insert'))
    return render_template('house/insert.html', form=form)

@bp.route('/rent/')
@login_required
def rent():
    page = request.args.get('page', 1, type=int)
    rents = current_user.rent_offers().paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('hse.rent', page=rents.next_num) if rents.has_next else None
    prev_url = url_for('hse.rent', page=rents.prev_num) if rents.has_prev else None
    return render_template('user.html', title='Rent Offers', user=current_user, posts=rents.items, next_url=next_url, prev_url=prev_url)
