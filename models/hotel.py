from sql_alchemy import banco

class HotelModel(banco.Model):
    """ Classe Hotel Modelo"""
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrela = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, hotel_id, nome, estrela, diaria, cidade):
        """ construtor """
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrela = estrela
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        """ construtor para retorna o objeto em formato JSON """
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrela': self.estrela,
            'diaria': self.diaria,
            'cidade': self.cidade
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() # seleciona o hotel referente ao hotel_id informado
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrela, diaria, cidade):
        self.nome = nome
        self.estrela = estrela
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
