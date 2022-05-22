import psycopg2
import functools

from flask import Flask
from flask import Response
from flask import redirect
from flask import request
from flask import render_template
from flask import globals
from flask import url_for
from flask import session

from configuration import CONNECTION_PARAMS

from services.kitchen_service import KitchenService
from services.offer_service import OfferService
from services.officiant_service import OfficiantService
from services.discount_service import DiscountService
from services.client_service import ClientService
from services.dish_list_service import DishListService
from services.product_list_service import ProductListService
from services.product_service import ProductService
from services.dish_service import DishService

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='development',
)

def connect():
    try:
        conn = psycopg2.connect(**CONNECTION_PARAMS)

        cur = conn.cursor()

        print(" * PostgreSQL database version: ", end=' ')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        cur = None

connect()


def login_required(view):
    """Декоратор, который перенаправляет на страницу логина, если пользователь неопределен"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if globals.user is None:
            return redirect(url_for('login'))
        
        return view(**kwargs)
    
    return wrapped_view


@app.before_first_request
def load_user_before_first_request():
    try:
        user_id = session['user_id']

        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            globals.user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}")

    except (Exception) as error:
        print(error)

        globals.user = None

        return redirect(url_for('error', error_text=error))


@app.route('/register', methods=['GET', 'POST'])
def register():
    with psycopg2.connect(**CONNECTION_PARAMS) as conn:
        if request.method == 'POST':
            try:
                json = request.form

                username = json['username']
                password = json['password']
                password_confirmation = json['password_confirmation']

                if password == password_confirmation:
                    cur = conn.cursor()

                    query = f"""INSERT INTO users(username, password, role) VALUES
                                                (\'{username}\', \'{generate_password_hash(password, method='plain', salt_length=8)}\', 'user');"""
                    
                    cur.execute(query)

                    return redirect(url_for('login'))
                else:
                    return redirect(url_for('error', error_text='Пароли не совпадают.'))
            
            except (Exception) as error:
                print(error)

                return redirect(url_for('error', error_text=error))
        
        return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST',])
def login():
    with psycopg2.connect(**CONNECTION_PARAMS) as conn:
        if request.method == 'POST':
            try:
                json = request.form

                username = json['username']
                password = json['password']

                cur = conn.cursor()

                cur.execute(f"SELECT * FROM users WHERE username = \'{username}\'")

                user = cur.fetchone()

                id, login, passw, role = user

                if not check_password_hash(passw, password):
                    raise Exception('Password is not matching')
                
                session.clear()
                session['user_id'] = id

                globals.user = 

                return redirect(url_for('index'))
                
            except (Exception) as error:
                print(f' * {error}')

                return redirect(url_for('error', error_text=error))
        
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('base.html', g=globals, session=session)


@app.route('/error/<error_text>')
def error(error_text):
    return render_template('error.html', error_text=error_text)


@app.route('/api/kitchens', methods=['GET', 'POST', 'DELETE'])
@login_required
def kitchens():
    service = KitchenService()
    if request.method == 'GET':
        return service.get_all_kitchens()
    elif request.method == 'POST':
        return service.create_kitchen()
    elif request.method == 'DELETE':
        return service.delete_kitchen()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')


@app.route('/api/officiants', methods=['GET', 'POST', 'DELETE'])
@login_required
def officiants():
    service = OfficiantService()

    if request.method == 'GET':
        return service.get_all_officiants()
    elif request.method == 'POST':
        return service.create_officiant()
    elif request.method == 'DELETE':
        return service.delete_officiant()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')


@app.route('/api/discounts', methods=['GET', 'POST', 'DELETE'])
@login_required
def discounts():
    service = DiscountService()

    if request.method == 'GET':
        return service.get_all_discounts()
    elif request.method == 'POST':
        return service.create_discount()
    elif request.method == 'DELETE':
        return service.delete_discount()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')


@app.route('/api/clients', methods=['GET', 'POST', 'DELETE'])
@login_required
def clients():
    service = ClientService()

    if request.method == 'GET':
        return service.get_all_clients()
    elif request.method == 'POST':
        return service.create_client()
    elif request.method == 'DELETE':
        return service.delete_client()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')


@app.route('/api/dish_lists', methods=['GET', 'POST', 'DELETE'])
@login_required
def dish_lists():
    service = DishListService()

    if request.method == 'GET':
        return service.get_dish_lists()
    elif request.method == 'POST':
        return service.create_dish_list()
    elif request.method == 'DELETE':
        return service.delete_dish_list()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')


@app.route('/api/dishes', methods=['GET', 'POST', 'DELETE'])
@login_required
def dishes():
    service = DishService()

    if request.method == 'GET':
        return service.get_all_dishes()
    elif request.method == 'POST':
        return service.create_dish()
    elif request.method == 'DELETE':
        return service.delete_dish()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')


@app.route('/api/offers', methods=['GET', 'POST', 'DELETE'])
@login_required
def offers():
    service = OfferService()

    if request.method == 'GET':
        return service.get_all_offers()
    elif request.method == 'POST':
        return service.create_offer()
    elif request.method == 'DELETE':
        return service.delete_offer()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')


@app.route('/api/product_lists', methods=['GET', 'POST', 'DELETE'])
@login_required
def product_lists():
    service = ProductListService()

    if request.method == 'GET':
        return service.get_product_lists()
    elif request.method == 'POST':
        return service.create_product_list()
    elif request.method == 'DELETE':
        return service.delete_product_list()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')


@app.route('/api/products', methods=['GET', 'POST', 'DELETE'])
@login_required
def products():
    service = ProductService()

    if request.method == 'GET':
        return service.get_all_products()
    elif request.method == 'POST':
        return service.create_product()
    elif request.method == 'DELETE':
        return service.delete_product()
    else:
        return Response({ 'ok': False, 'status': 404 }, status=404, mimetype='application/json')