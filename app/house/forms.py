from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, RadioField, FormField, DecimalField, DateField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

# rooms_str = ('1', '2', '3', '4', '5 и больше', )

class RoomsValue(FlaskForm):
    r1 = BooleanField(label=u'1', default=False)
    r2 = BooleanField(label=u'2', default=False)
    r3 = BooleanField(label=u'3', default=False)
    r4 = BooleanField(label=u'4', default=False)
    r5 = BooleanField(label=u'5 и больше', default=False)

class FloorsValue(FlaskForm):
    f1 = BooleanField(label=u'не первый', default=True)
    f2 = BooleanField(label=u'не последний', default=False)
    f3 = BooleanField(label=u'первый/последний', default=False)
    f4 = BooleanField(label=u'не имеет значения', default=False)

class PeriodValue(FlaskForm):
    p1 = BooleanField(label=u'посуточно', default=False)
    p2 = BooleanField(label=u'помесячно', default=True)
    p3 = BooleanField(label=u'больше года', default=False)

class HouseSearchForm(FlaskForm):
    type = RadioField(
        'Тип жилья', 
        [DataRequired()],
        choices=[('1', 'квартира'), ('2', 'комната'), ('3', 'дом'), ('4', 'гараж'), ('5', 'офис'), ('6', 'участок')],
        coerce=int,
    )

    rooms = FormField(RoomsValue, separator=' ', label='Количество комнат')

    nfloor = FormField(FloorsValue, separator=' ', label='Этаж')
    
    '''
    nfloor = SelectField(
        u'Этаж',
        choices=[(1, 'не первый'), (2, 'не последний'), (4, 'первый/последний'), (8, 'не имеет значения')],
        coerce=int,
        default=8,
    )
    '''
    living_area_from = DecimalField (
        u'Жилая площадь от: ',
        # [validators.required(), validators.length(max=10)],
        # coerce=float,
        default=0.0,
    )
    
    living_area_to = DecimalField (
        u'Жилая площадь до: ',
        # [validators.required(), validators.length(max=10)],
        # coerce=float,
    )
    
    user_type = RadioField(
        u'Арендодатель или представитель: ',
        [DataRequired()],
        choices=[('1', 'владелец жилья'), ('2', 'риэлтер'), ('3', 'агентство'),],
        default='1'
    )
    
    price_from = DecimalField (
        u'Цена за период от: ',
        # [validators.required(), validators.length(max=10)],
        # coerce=float,
        default=0.0,
    )
    
    price_to = DecimalField (
        u'Цена за период до: ',
        # [validators.required(), validators.length(max=10)],
        # coerce=float,
    )
    
    prepay_from = DecimalField (
        u'Предоплата от: ',
        # [validators.required(), validators.length(max=10)],
        # coerce=float,
        default=0.0,
    )
    
    prepay_to = DecimalField (
        u'Предоплата до: ',
        # [validators.required(), validators.length(max=10)],
        # coerce=float,
    )
    
    rental_period = FormField(PeriodValue, separator=' ', label='Период аренды')
    
    '''
    rental_period = SelectField(
        u'Срок аренды: ',
        choices=[('1', 'посуточно'), ('2', 'помесячно'), ('4', 'больше года')],
        coerce=int,
        default='2',
    )
    
    
    address = TextAreaField(
        u'Адрес: ',
        # [validators.optional(), validators.length(max=256)],
    )
    '''
    actual_date_from = DateField(
        u'Дата публикации от: ', 
        format='%Y-%m-%d',
    )
    
    actual_date_to = DateField(
        u'Дата публикации до: ', 
        format='%Y-%m-%d',
    )
    
    submit = SubmitField('Выбрать')


class HouseCreateForm(FlaskForm):
    type = IntegerField(
        'Тип жилья: ',
        [
            DataRequired(message="This field is required")
        ],
        description='1 - квартира, 2 - комната, 3 - служебное помещение'
    )
    rooms = IntegerField(
        'Количество комнат: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Количество комнат'
    )
    living_area = IntegerField(
        'Жилая площадь: ',
        [
            DataRequired(message="This field is required")
        ],
        description='Жилая площадь'
    )
    kitchen_area = IntegerField(
        'Площадь кухни: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Площадь кухни'
    )
    nfloor = IntegerField(
        'Этаж: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Этаж'
    )
    floors = IntegerField(
        'Этажей в доме: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Этажей в доме'
    )
    price = FloatField(
        'Арендная плата за единицу времени сдачи: ',
        [
            DataRequired(message="This field is required")
        ],
        description='Арендная плата (см. Период сдачи)'
    )
    prepay = FloatField(
        'Предоплата: ',
        [
            DataRequired(message="This field is required")
        ],
        description='Предоплата'
    )
    insurance = IntegerField(
        'Страховка: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Страховка'
    )
    rental_period = IntegerField(
        'Период сдачи: ',
        [
            DataRequired(message="This field is required")
        ],
        description='1 - помесячно, 2 - на длительный срок, 3 - посуточно'
    )
    contract_type = IntegerField(
        'Тип договора: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Тип договора'
    )
    client_commission = IntegerField(
        'Комиссия клиента: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Комиссия клиента'
    )
    agents = BooleanField(
        'Агент: ',
        [
            # DataRequired(message="This field is required")
        ],
        description=''
    )
    agents_commission = IntegerField(
        'Комиссия агента %: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Комиссия агентам %'
    )
    address = TextAreaField(
        'Адрес: ',
        [
            DataRequired(message="This field is required")
        ],
        description='Адрес'
    )
    insurance = IntegerField(
        'Страховка: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Страховка'
    )
    metro = IntegerField(
        'Станция метро (если есть): ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Станция метро ID'
    )
    metro_dist = IntegerField(
        'Время до станции метро (см. следующий пункт): ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Время до станции метро'
    )
    walk = BooleanField(
        'Пешком (да/нет): ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Пешком'
    )
    railway_dist = IntegerField(
        'Расстояние до ж/д станции: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Расстояние до ж/д станции'
    )
    kitchen_furn = BooleanField(
        'Наличие кухонной мебели: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Наличие кухонной мебели'
    )
    room_furn = BooleanField(
        'Наличие мебели: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Наличие мебели'
    )
    refrigerator = BooleanField(
        'Холодильник: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Холодильник'
    )
    tv = BooleanField(
        'Телевизор: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Телевизор'
    )
    washing_automat = BooleanField(
        'Стиральная машина-автомат: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Стиральная машина-автомат'
    )
    dishwasher = BooleanField(
        'Посудомоечная машина: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Посудомоечная машина'
    )
    internet = BooleanField(
        'Интернет: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Интернет'
    )
    balcony = BooleanField(
        'Балкон: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Балкон'
    )
    windows = IntegerField(
        'Количество окон: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Количество око'
    )
    bathrooms = IntegerField(
        'Количество ванных комнат: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Количество ванных комнат'
    )
    bath = BooleanField(
        'Ванна: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Ванна'
    )
    shower_cab = BooleanField(
        'Душевая кабина: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Душевая кабина'
    )
    parking = BooleanField(
        'Парковка: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='Парковка'
    )
    repair_need = IntegerField(
        'Требуется ремонт: ',
        [
            # DataRequired(message="This field is required")
        ],
        description='0 - нет, 1 - косметический, 2 капитальный'
    )
    submit = SubmitField('Сохранить')
    