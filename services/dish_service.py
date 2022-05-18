import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class DishService():
    def get_all_dishes(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM dish;')
            dishes = cur.fetchall()

            data = []
            for dish in dishes:
                print(dish)
                id, dish_name, kitchen_id, cost = dish
                
                data.append({
                    'id': id,
                    'dish_name': dish_name,
                    'kitchen_id': kitchen_id,
                    'cost': cost,
                })

            return { 'data': data }

    def create_dish(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                query = f"""
                    INSERT INTO dish(dish_name, kitchen_id, cost) VALUES
                    (\'{json['dish_name']}\', \'{json['kitchen_id']}\', \'{json['cost']}\')
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

    def delete_dish(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM dish WHERE dish_id = {json["id"]}')

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


