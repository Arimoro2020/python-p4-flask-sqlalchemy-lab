from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Zookeeper(db.Model):
    __tablename__ = 'zookeepers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birthday = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime, server_default= db.func.now())
    end_date = db.Column(db.DateTime, onupdate=db.func.now())
    zookeeper_animals= db.relationship('Animal', back_populates='zookeeper')
    enclosures= association_proxy('zookeeper_animals', 'enclosure')

class Enclosure(db.Model):
    __tablename__ = 'enclosures'

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean, default=False)
    enclosure_animals = db.relationship('Animal', back_populates='enclosure')
    zookeepers = association_proxy('enclosure_animals', 'zookeeper')

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)  
    species = db.Column(db.String)
    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))
    enclosure = db.relationship('Enclosure', back_populates='enclosure_animals')
    zookeeper = db.relationship('Zookeeper', back_populates='zookeeper_animals')