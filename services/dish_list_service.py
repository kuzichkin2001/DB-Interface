import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class DishListService():
    def get_dish_lists(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM dish_list;')
            dish_lists = cur.fetchall()

            data = []
            for dish_list in dish_lists:
                offer_id, dish_id = dish_list
                
                data.append({
                    'offer_id': offer_id,
                    'dish_id': dish_id
                })

            return { 'data': data }

    def create_dish_list(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                query = f"""
                    INSERT INTO dish_list(offer_id, dish_id) VALUES
                    (\'{json['offer_id']}\', \'{json['dish_id']}\')
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

    def delete_dish_list(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM dish_list WHERE dish_id = {json["dish_id"]}')

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


