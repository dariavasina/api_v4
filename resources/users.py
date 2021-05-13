from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from api_v4.models.users import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="this field cannot be blank!")
    parser.add_argument('password', type=str, required=True, help="this field cannot be blank!")

    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return {'user': user}, 204
        return {'message': "user '{}' does not exist".format(user)}, 404

    def post(self):
        user = UserRegister.parser.parse_args()
        if UserModel.find_by_username(user['username']):
            return {'message': "user '{}' already exists".format(user['username'])}, 208
        user = UserModel(**user)
        user.add_user()
        return {'new user': user}, 204

    @jwt_required
    def put(self):
        new_user = UserRegister.parser.parse_args()
        if UserModel.find_by_username(new_user['username']):
            user = UserModel.query.filter_by(username=new_user['username'])
            user.password = new_user['password']
        else:
            new_user = UserModel(**new_user)
            new_user.add_user()
        return {'new user': new_user}, 204

    @jwt_required()
    def delete(self):
        user = UserRegister.parser.parse_args()
        if UserModel.find_by_username(user['username']):
            user = UserModel.query.filter_by(username=user['username'])
            user.delete_user()
            return {'message': "user '{}' was deleted successfully".format(user)}, 204
        return {'message': "user '{}' does not exist".format(user)}, 404
