from flask import Flask, request
from security import authenticate, identity
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
import sqlite3 

# pip install Flask_RESTFul
# pip install Flask_JWT

app = Flask(__name__)
app.secret_key = 'duypk'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create a new endpoint /auth
# jwt get our username and password, and send it to authenticate function, find correct user object and compare password that we received
# /auth endpoint will return JWT token if password is matched

# We can send jwt token to the next request we make, when we send jwt token, jwt will call identity function
# It will use JWT token to get the user id that means the user was authenticated, JWT token is valid 

items = []

class Item(Resource):
    @jwt_required() # must authenticate before call get method, when test api, modify content-type in header tab to application/json
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None) 
        return {'item': item}, 200 if item else 404
    
    @jwt_required()
    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None): 
            return {'message': "An item with name '{}' already exists".format(name)}, 400 # 400 mean bad request

        request_data = request.get_json() # modify content-type in header tab in postman to application/json 
        new_item = {
            'name': name,
            'price': request_data['price']
        }
        items.append(new_item)
        return new_item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {'message': "Item deleted"}

    def put(self, name): 
        parser = reqparse.RequestParser() # Tao object de su dung 
        # chi chap nhan mot argument la price, chi chap nhan thay doi nhung tham so lien quan, de nguoi dung khong thay thay doi nhung thong tin quan trong 
        parser.add_argument('price', 
            type=float, 
            required=True, 
            help="This field can't not be blank"
        )

        # data_request = request.get_json()
        data_request = parser.parse_args() 
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item is None: 
            item = {
                'name': name, 
                'price': data_request['price']
            }
            items.append(item)
        else:
            item.update(data_request)
        return item

pass

class ItemList(Resource):
    def get(self):
        return {'item': items}

# pip install Flask-JWT for authentication 

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000,debug=True) # Debug de show error message 
