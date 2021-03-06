from db import db
class ItemModel(db.Model): 
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_json(self):
        return {'name': self.name, 'price': self.price}
        
    @classmethod
    def find_by_name(cls, name): # class method 
        # SQLAlchemy handle all connections, cursor creation even the queries
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1 
    
    def save_to_db(self): 
        # session là một đối tượng collection chứa các object mà chúng ta sẽ write vô db
        # Mỗi object trong database sẽ có một id, nếu như mà insert trùng id thì add method sẽ update thay vì insert, tiện vl 
        db.session.add(self)  
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()