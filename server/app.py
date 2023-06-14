#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    q = Animal.query.filter(Animal.id == id).first()

    if not q:
        response_body = '<h1>404 animal not found</h1>'
        response = make_response(response_body, 404)
        return response
    else:
        response_body = f'<ul>Name: {q.name}</ul>\n'
        response_body += f'<ul>Species: {q.species}</ul>\n'

        
    q_zookeepers = Zookeeper.query.filter(Zookeeper.id ==q.zookeeper_id).all()



    if not q_zookeepers:
        response_body += '<h1>404 No zookeeper found</h1>'
        response = make_response(response_body, 404)

    else:
        for qz in range(len(q_zookeepers)):
             response_body += f'<ul>Zookeeper: {q_zookeepers[qz].name}</ul>'

    
          
    q_enclosures = Enclosure.query.filter(Enclosure.id == q.enclosure_id).all()



    if not q_enclosures:
        response_body += '<h1>404 No enclosure found</h1>'
        response = make_response(response_body, 404)

    else:
        for qe in range(len(q_enclosures)):
             response_body += f'<ul>Enclosure: {q_enclosures[qe].environment}</ul>'
        

    return make_response(response_body, 200)

    
    

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    q = Zookeeper.query.filter(Zookeeper.id == id).first()
    if not q:
        response_body = '<h1>404 zookeeper not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    Name = q.name
    Birthday = q.birthday

    response_body = f'<ul>Name: {Name}</ul>\n'
    response_body += f'<ul>Birthday: {Birthday}</ul>\n'
    
    q_animals = Animal.query.filter(Animal.zookeeper_id ==id).all()



    if not q_animals:
        response_body += '<h1>404 No animal found</h1>'
        response = make_response(response_body, 404)

    else:
        for q in range(len(q_animals)):
             response_body += f'<ul>Animal: {q_animals[q].name}</ul>'
        

    return make_response(response_body, 200)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):

    q = Enclosure.query.filter(Enclosure.id == id).first()

    if not q:
        response_body = '<h1>404 enclosure not found</h1>'
        response = make_response(response_body, 404)
        return response
   
   
    response_body = f'<ul>Environment: {q.environment}</ul>\n'
    response_body += f'<ul>Open to visitors: {q.open_to_visitors}</ul>\n'

    q_animals = Animal.query.filter(Animal.enclosure_id == id).all()



    if not q_animals:
        response_body += '<h1>404 No animal found</h1>'
        response = make_response(response_body, 404)

    else:
        for qa in range(len(q_animals)):
             response_body += f'<ul>Animal: {q_animals[qa].name}</ul>'


    return make_response(response_body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
