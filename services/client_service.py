# something went wrong

import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class ClientService():
    def get_all_clients(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM client;')
            clients = cur.fetchall()

            data = []
            for client in clients:
                id, name, birthdate, phone_number, discount_id = client
                
                data.append({
                    'id': id,
                    'name': name,
                    'birthdate': birthdate,
                    'phone_number': phone_number,
                    'discount_id': discount_id
                })

            return { 'data': data }

    def create_client(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                query = f"""
                    INSERT INTO client(name, birthdate, phone_number, discount_id) VALUES
                    (\'{json['name']}\', \'{json['birthdate']}\', \'{json['phone_number']}\', \'{json['discount_id']}\')
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

    def delete_client(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM client WHERE client_id = {json["id"]}')

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


