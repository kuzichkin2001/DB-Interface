import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class KitchenService():
    def get_all_kitchens(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM kitchen;')
            kitchens = cur.fetchall()

            data = []
            for kitchen in kitchens:
                id, name = kitchen
                
                data.append({
                    'id': id,
                    'kitchen_name': name
                })

            return { 'data': data }

    def create_kitchen(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'INSERT INTO kitchen(kitchen_name) VALUES (\'{json["name"]}\');')

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

    def delete_kitchen(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM kitchen WHERE kitchen_id = {json["id"]}')

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


