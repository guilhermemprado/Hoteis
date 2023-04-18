""" Imports """
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
import sqlite3

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrela_min', type=float)
path_params.add_argument('estrela_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
            'hotel_id': linha[0] ,
            'nome': linha[1],
            'estrela': linha[2],
            'diaria': linha[3],
            'cidade': linha[4]
            })

        return {'hoteis': hoteis} # SELECT * FROM hoteis

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    atributos.add_argument('estrela')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')
    
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):
        """ Seta o valor """
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel '{}' already exists.". format(hotel_id)}, 400 # Código 400 - requisiçao errada

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados) # Utilizando o **kwargs
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal Server error
        return hotel.json()

    def put(self, hotel_id):
        """ Seta o valor """
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados) # Utilizando o **kwargs
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 # Código 200 - tudo certo
        hotel = HotelModel(hotel_id, **dados) # Utilizando o **kwargs
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal Server error
        return hotel.json(), 201 # Código 201 - criar

    def delete(self, hotel_id):
        """ Seta o valor """
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500 # Internal Server error
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel deleted.'}, 404
    