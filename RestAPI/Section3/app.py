from flask import Flask, jsonify, request

# This __name__ variable will give each file a unique name
app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'item': [
            {
                'name': 'My Item',
                'price': 100
            }
        ]
    }
]

# POST - used to receive data
# GET - used to send data back only and both of them is see under server perspective

# POST /store data: {name:}


# By default, @app.route will use GET method
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'item': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
# <string:name> is a special Flask syntax, when we create our method, our method can have a param which is name


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store not found'})

# GET /stores


@app.route('/stores')
def get_stores():
    return jsonify({'store': stores})

# POST /store/<string:name>/item {name, price}


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    new_item = {
        'name': request_data['name'],
        'price': request_data['price']
    }
    for store in stores:
        if store['name'] == name:
            store['item'].append(new_item)
    return jsonify(new_item)


# GET /store/<string:name>/item


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'item': store['item']})
    return jsonify({'message': 'Item not found'})


app.run(port=6969)
