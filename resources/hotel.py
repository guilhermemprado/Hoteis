""" Imports """
from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    """ Criando classe Hoteis """
    def get(self):
        """ Seta o valor """
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # Basicamento um select all

class Hotel(Resource):
    """ Criando classe Hotel """
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required= True, help="The fild 'nome' cannot be left blank.")
    atributos.add_argument('estrela', type=float, required=True, help="The filed 'estrelas' cannot be left blank.")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        """ Seta o valor """
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404 # note found

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
    