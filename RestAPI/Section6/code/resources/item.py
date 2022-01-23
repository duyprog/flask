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
            return item, 200
        return {'message': 'Item not found'}, 404 


    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item is already exists !'}

        data = Item.parser.parse_args()
        
        item = {'name': name, 'price': data['price']}
        ItemModel.insert(item)
        return item

    @jwt_required()    
    def put(self, name): 
        data = Item.parser.parse_args() 
         
        updated_item = {'name': name, 'price': data['price']}
        item = ItemModel.find_by_name(name)

        if item is None: 
            try: 
                ItemModel.insert(updated_item)
            except:
                return {'message': 'An error occurred inserting the item'}
        else: 
            try: 
                ItemModel.update(updated_item)
            except: 
                return {'message': 'An error occurred inserting the item'} 
        return updated_item


    @jwt_required()
    def delete(self, name):
        if ItemModel.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor() 

            query = 'DELETE FROM items WHERE name=?'
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()

            return {'message': 'Item deleted'}, 200

        return {'message': 'Item not found'}, 404

    

pass

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor() 
        items = [] 

        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        for row in result: 
            items.append({'name': row[0], 'price': row[1]})

        connection.commit() 
        connection.close()

        return {'items': items}, 200