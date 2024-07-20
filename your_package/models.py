from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import enum

db = SQLAlchemy()

class CaseStatus(enum.Enum):
    wait = 'wait'
    find = 'find'
    pend = 'pend'
    close = 'close'

# 定義多對多關係表
case_tags = db.Table('case_tags',
                     db.Column('case_id', db.Integer, db.ForeignKey('cases.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )

conversation_merchants = db.Table('conversation_merchants',
                                  db.Column('conversation_id', db.Integer, db.ForeignKey('conversations.id')),
                                  db.Column('merchant_id', db.Integer, db.ForeignKey('merchants.id'))
                                  )

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    conversations = db.relationship('Conversation', back_populates='customer')
    cases = db.relationship('Case', back_populates='customer')
    logins = db.relationship('Login', back_populates='customer')

class Merchant(db.Model):
    __tablename__ = 'merchants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cases = db.relationship('Case', back_populates='merchant')
    conversations = db.relationship('Conversation', secondary=conversation_merchants, back_populates='merchants')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cases = db.relationship('Case', secondary=case_tags, back_populates='tags')

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String, unique=True, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=True)
    status = db.Column(Enum(CaseStatus), nullable=False, default=CaseStatus.wait)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id'))
    contractor_id = db.Column(db.Integer, db.ForeignKey('merchants.id'))
    customer = db.relationship('Customer', back_populates='cases')
    merchant = db.relationship('Merchant', back_populates='cases', foreign_keys=[merchant_id])
    contractor = db.relationship('Merchant', foreign_keys=[contractor_id])
    tags = db.relationship('Tag', secondary=case_tags, back_populates='cases')
    conversations = db.relationship('Conversation', back_populates='case')

class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    customer = db.relationship('Customer', back_populates='conversations')
    merchants = db.relationship('Merchant', secondary=conversation_merchants, back_populates='conversations')
    case = db.relationship('Case', back_populates='conversations', foreign_keys=[case_id])

class Login(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customer', back_populates='logins')
