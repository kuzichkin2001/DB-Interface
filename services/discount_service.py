import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class DiscountService():
    def get_all_discounts(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM discount;')
            discounts = cur.fetchall()

            data = []
            for discount in discounts:
                id, start_date, end_date = discount
                
                data.append({
                    'id': id,
                    'start_date': start_date,
                    'end_date': end_date
                })

            return { 'data': data }

    def create_discount(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                query = f"""
                    INSERT INTO discount(start_date, end_date) VALUES
                    (\'{json['start_date']}\', \'{json['end_date']}\')
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

    def delete_discount(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM kitchen WHERE discount_id = {json["id"]}')
                cur.execute(f'DELETE FROM discount WHERE discount_id = {json["id"]}')

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


