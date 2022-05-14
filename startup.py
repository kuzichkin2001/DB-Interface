import psycopg2

from flask import Flask, Response, request
from configuration import CONNECTION_PARAMS
from services.kitchen_service import KitchenService
from services.officiant_service import OfficiantService
from services.discount_service import DiscountService


app = Flask(__name__)

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


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/api/kitchens', methods=['GET', 'POST', 'DELETE'])
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
