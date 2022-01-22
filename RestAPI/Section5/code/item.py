import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):

    parser = reqparse.RequestParser() 
    parser.add_argument('price', 
        type=float, 
        required=True,
        help="This field cannot be bank !"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row: 
            return {'item': {'name': row[0], 'price': row[1]}}
    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'],item['price']))

        connection.commit() 
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item['price'], item['name']))
        
        connection.commit() 
        connection.close()
        pass   

    @jwt_required() # must authenticate before call get method, when test api, modify content-type in header tab to application/json
    def get(self, name):
        item = self.find_by_name(name)

        if item: 
            return item, 200
        return {'message': 'Item not found'}, 404 


    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': 'Item is already exists !'}

        data = Item.parser.parse_args()
        
        item = {'name': name, 'price': data['price']}
        self.insert(item)
        return item

    @jwt_required()    
    def put(self, name): 
        data = Item.parser.parse_args() 
         
        updated_item = {'name': name, 'price': data['price']}
        item = self.find_by_name(name)

        if item is None: 
            try: 
                self.insert(updated_item)
            except:
                return {'message': 'An error occurred inserting the item'}
        else: 
            try: 
                self.update(updated_item)
            except: 
                return {'message': 'An error occurred inserting the item'} 
        return updated_item


    @jwt_required()
    def delete(self, name):
        if self.find_by_name(name):
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