import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class ProductListService():
    def get_product_lists(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM product_list;')
            product_lists = cur.fetchall()

            data = []
            for product_list in product_lists:
                id_dish, product_id, product_count, cooking_type = product_list
                
                data.append({
                    'id_dish': id_dish,
                    'product_id': product_id,
                    'product_count': product_count,
                    'cooking_type': cooking_type
                })

            return { 'data': data }

    def create_product_list(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                query = f"""
                    INSERT INTO product_list(id_dish, product_id, product_count, cooking_type) VALUES
                    ({json['id_dish']}, {json['product_id']}, {json['product_count']}, \'{json['cooking_type']}\')
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

    def delete_product_list(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM product_list WHERE id_dish = {json["id"]}')

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


