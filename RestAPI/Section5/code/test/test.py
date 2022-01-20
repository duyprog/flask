from flask import Flask
from flask_restful import Resource, Api 
# Resource la may cai ma API co the return hoac create, vi du nhu student, product,...
# Resource luon luon map vo table cua database 
# Api giup chung ta co the de dang add resource, get post delete

app = Flask(__name__)
api = Api(app)

# Moi resource la mot class 

class Student(Resource): 
    def get(self, name):
        return {'student': name}

# Resource co the duoc access thong qua API - add_resource. 
api.add_resource(Student, '/student/<string:name>') # http://localhost:5000/duy 
app.run(port=5000)