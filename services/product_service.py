import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class ProductService():
    def get_all_products(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM product;')
            products = cur.fetchall()

            data = []
            for product in products:
                id, product_name, exp_time, arrivement_date, cost, supplier = product
                
                data.append({
                    'id': id,
                    'product_name': product_name,
                    'exp_time': exp_time,
                    'arrivement_date': arrivement_date,
                    'cost': cost,
                    'supplier': supplier
                })

            return { 'data': data }

    def create_product(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                query = f"""
                    INSERT INTO product(product_name, exp_time, arrivement_date, cost, supplier) VALUES
                    (\'{json['product_name']}\', {json['exp_time']}, \'{json['arrivement_date']}\', {json['cost']}, \'{json['supplier']}\');
                """
                cur.execute(query)

                response = {
                    'ok': True,
                    'status': 200
                }

                return Response(response, status=200, mimetype='application/json');
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

                response = {
                    'ok': False,
                    'status': 400
                }

                return Response(response, status=400, mimetype='application/json')

    def delete_product(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM product WHERE id_product = {json["id"]}')

                response = {
                    'ok': True,
                    'status': 200
                }

                return Response(response, status=200, mimetype='application/json')
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

                response = {
                    'ok': False,
                    'status': 400
                }

                return Response(response, status=400, mimetype='application/json')


