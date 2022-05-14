import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class OfficiantService():
    def get_all_officiants(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM officiant;')
            officiants = cur.fetchall()

            data = []
            for officiant in officiants:
                id, name, hiring_date, level, phone_number, birthdate = officiant
                
                data.append({
                    'id': id,
                    'officiant_name': name,
                    'hiring_date': hiring_date,
                    'level': level,
                    'phone_number': phone_number,
                    'birthdate': birthdate
                })

            return { 'data': data }

    def create_officiant(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                query = f"""
                    INSERT INTO officiant(name, hiring_date, level, phone_number, birthdate) VALUES
                    (\'{json['officiant_name']}\', \'{json['hiring_date']}\', \'{json['level']}\', \'{json['phone_number']}\', \'{json['birthdate']}\')
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

    def delete_officiant(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM officiant WHERE officiant_id = {json["id"]}')

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


