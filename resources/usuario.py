""" Imports """
from flask_restful import Resource, reqparse
from models.usuario import UserModel

class User(Resource):
    """ /usuarios/{user_id}"""

    def get(self, user_id):
        """ Seta o valor """
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404 # note found

    def delete(self, user_id):
        """ Seta o valor """
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User deleted.'}, 404
    
class UserRegister(Resource):
    """ /cadastro """
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="The filed 'login' cannot be left blank.")
        atributos.add_argument('senha', type=str, required=True, help="The filed 'senha' cannot be left blank.")
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User cread successfully!'}, 201 # Created
