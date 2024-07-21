import enum
# from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

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

merchant_tags = db.Table('merchant_tags',
                     db.Column('cmerchant_id', db.Integer, db.ForeignKey('merchants.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )

conversation_merchants = db.Table('conversation_merchants',
                                  db.Column('conversation_id', db.Integer, db.ForeignKey('conversations.id')),
                                  db.Column('merchant_id', db.Integer, db.ForeignKey('merchants.id'))
                                  )

# 定義顧客模型
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

# 定義商家模型
class Merchant(db.Model):
    __tablename__ = 'merchants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    case_experience = db.Column(db.Integer, default=0)
    temp_experience = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cases = db.relationship('Case', back_populates='merchant')
    conversations = db.relationship('Conversation', secondary=conversation_merchants, back_populates='merchants')
    tags = db.relationship('Tag', secondary=merchant_tags, back_populates='merchants')
    
# 定義標籤模型
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cases = db.relationship('Case', secondary=case_tags, back_populates='tags')

# 定義案件模型
class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String, unique=True, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=True)
    status = db.Column(db.String, nullable=False, default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id'))
    contractor_id = db.Column(db.Integer, db.ForeignKey('merchants.id'))
    customer = db.relationship('Customer', back_populates='cases')
    merchant = db.relationship('Merchant', back_populates='cases', foreign_keys=[merchant_id])
    contractor = db.relationship('Merchant', foreign_keys=[contractor_id])
    tags = db.relationship('Tag', secondary=case_tags, back_populates='cases')

# 定義對話模型
class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    customer = db.relationship('Customer', back_populates='conversations')
    merchants = db.relationship('Merchant', secondary=conversation_merchants, back_populates='conversations')

# 定義登入資料模型
class Login(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customer', back_populates='logins')

