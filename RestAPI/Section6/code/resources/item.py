import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser() 
    parser.add_argument('price', 
        type=float, 
        required=True,
        help="This field cannot be bank !"
    )

    @jwt_required() # must authenticate before call get method, when test api, modify content-type in header tab to application/json
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item: 
            return item.to_json(), 200
        return {'message': 'Item not found'}, 404 


    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item is already exists !'}, 400

        data = Item.parser.parse_args()
        
        item = ItemModel(name, data['price'])
        
        try: 
            item.save_to_db() 
        except: 
            return {'message': 'An error occured inserting item'}
        
        return item.to_json()

    @jwt_required()    
    def put(self, name): 
        data = Item.parser.parse_args() 
         
        item = ItemModel.find_by_name(name) 

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.to_json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item: 
            item.delete_from_db()
            return {'message': 'Item deleted'}
        else:
            return {'message': 'Item not found'}, 404
pass


class ItemList(Resource):
    def get(self):
        # return {'items': list(map(lambda item: item.to_json(), ItemModel.query.all()))}, 200
        return {'items': [item.to_json() for item in ItemModel.query.all()]}, 200