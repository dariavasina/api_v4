from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from api_v4.models.items import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=int, required=True, help='This field cannot be blank!')

    @jwt_required()
    def get(self, name):
        if ItemModel.find_by_name(name):
            return {'item': ItemModel.find_by_name(name)}, 204
        return {'message': "item '{}' does not exist".format(name)}, 404

    @jwt_required()
    def post(self):
        item = Item.parser.parse_args()
        if ItemModel.find_by_name(item['name']):
            return {'message': "item '{}' already exists".format(item['name'])}
        item = ItemModel(**item)
        item.add_item()
        return {'new item': item}, 204

    @jwt_required()
    def put(self):
        new_item = Item.parser.parse_args()
        if ItemModel.find_by_name(new_item['name']):
            item = ItemModel.find_by_name(new_item['name'])
            item.price = new_item['price']
            return {'new_item': item}, 204
        new_item = ItemModel(**new_item)
        new_item.add_item()
        return {'new_item': new_item}, 204

    @jwt_required
    def delete(self):
        item = Item.parser.parse_args()
        if ItemModel.find_by_name(item['name']):
            item = ItemModel.find_by_name(item['name'])
            item.delete_item()
            return {'message': 'item was deleted successully'}, 204
        return {'message': "item '{}' does not exist".format(item)}, 404


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=dict, required=True, action='append', help='This field cannot be blank!')

    @jwt_required()
    def get(self):
        items = ItemModel.query.all()
        return {'items': items}, 204

    @jwt_required()
    def post(self):
        items = ItemList.parser.parse_args()['items']
        invalid_items = []
        if items:
            for item in items:
                item = ItemModel.find_by_name(item['name'])
                if item:
                    invalid_items.append(item)
                item.add_item()
            if invalid_items:
                return {'some items already exist': invalid_items}, 208
            return {'new items': items}, 204

    @jwt_required()
    def delete(self):
        items = ItemList.parser.parse_args()['items']
        invalid_items = []
        if items:
            for item in items:
                item = ItemModel.find_by_name(item['name'])
                if item:
                    item.delete_item()
                invalid_items.append(item)
            if invalid_items:
                return {'some items do not exist': invalid_items}, 404
            return {'message': 'all items deleted successfully'}, 204
