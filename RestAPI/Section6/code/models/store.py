from db import db
class StoreModel(db.Model): 
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {'name': self.name, 'items': self.items}
        
    @classmethod
    def find_by_name(cls, name): # class method 
        # SQLAlchemy handle all connection, cursor creation even the queries
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1 
    
    def save_to_db(self): 
        # session là một đối tượng collection chứa các object mà chúng ta sẽ write vô db
        # Mỗi object trong database sẽ có một id, nếu như mà insert trùng id thì add method sẽ update thay vì insert, tiện vl 
        db.session.add(self)  
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()