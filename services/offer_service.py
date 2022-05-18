import psycopg2

from flask import Response, request
from configuration import CONNECTION_PARAMS


class OfferService():
    def get_all_offers(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            cur = conn.cursor()

            cur.execute('SELECT * FROM offer;')
            offers = cur.fetchall()

            data = []
            for offer in offers:
                id, offer_time, price, officiant_id, client_id = offer
                
                data.append({
                    'id': id,
                    'offer_time': offer_time,
                    'price': price,
                    'officiant_id': officiant_id,
                    'client_id': client_id
                })

            return { 'data': data }

    def create_offer(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                query = f"""
                    INSERT INTO offer(offer_time, price, officiant_id, client_id) VALUES
                    (\'{json['offer_time']}\', {json['price']}, {json['officiant_id']}, {json['client_id']});
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

    def delete_offer(self):
        with psycopg2.connect(**CONNECTION_PARAMS) as conn:
            json = request.json

            try:
                cur = conn.cursor()
                cur.execute(f'DELETE FROM offer WHERE offer_id = {json["id"]}')

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


