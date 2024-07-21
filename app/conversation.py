

import enum

from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import  jwt_required, get_jwt_identity
from database import Customer, Conversation, Merchant

chat = Blueprint('chat', __name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # 使用 SQLite 数据库，文件名为 app.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 獲取對話的路由
@chat.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    user_id = get_jwt_identity()
    customer = Customer.query.get(user_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    
    conversations = Conversation.query.filter_by(customer_id=customer.id).all()
    conversations_data = [
        {
            'id': conv.id,
            'content': conv.content,
            'created_at': conv.created_at,
            'updated_at': conv.updated_at,
            'case': conv.case_id,
            'merchants': [merchant.id for merchant in conv.merchants]
        }
        for conv in conversations
    ]
    
    return jsonify(conversations_data), 200

# 新增對話的路由
@chat.route('/conversations', methods=['POST'])
@jwt_required()
def create_conversation():
    user_id = get_jwt_identity()
    customer = Customer.query.get(user_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    
    content = request.json.get('content')
    case_id = request.json.get('case_id')
    merchant_ids = request.json.get('merchant_ids', [])
    
    if not content:
        return jsonify({'message': 'Content is required'}), 400
    
    new_conversation = Conversation(customer_id=customer.id, content=content, case_id=case_id)
    db.session.add(new_conversation)
    db.session.commit()
    
    for merchant_id in merchant_ids:
        merchant = Merchant.query.get(merchant_id)
        if merchant:
            new_conversation.merchants.append(merchant)
    
    db.session.commit()
    
    return jsonify({'message': 'Conversation created successfully'}), 201

# 通過案件查詢對話紀錄的路由
@chat.route('/conversations/case/<int:case_id>', methods=['GET'])
@jwt_required()
def get_conversations_by_case(case_id):
    conversations = Conversation.query.filter_by(case_id=case_id).all()
    if not conversations:
        return jsonify({'message': 'No conversations found for this case'}), 404
    
    conversations_data = [
        {
            'id': conv.id,
            'content': conv.content,
            'created_at': conv.created_at,
            'updated_at': conv.updated_at,
            'customer': conv.customer_id,
            'merchants': [merchant.id for merchant in conv.merchants]
        }
        for conv in conversations
    ]
    
    return jsonify(conversations_data), 200

# 通過商家查詢對話紀錄的路由
@chat.route('/conversations/merchant/<int:merchant_id>', methods=['GET'])
@jwt_required()
def get_conversations_by_merchant(merchant_id):
    conversations = Conversation.query.join(Conversation.merchants).filter(Conversation.merchants.c.merchant_id == merchant_id).all()
    if not conversations:
        return jsonify({'message': 'No conversations found for this merchant'}), 404
    
    conversations_data = [
        {
            'id': conv.id,
            'content': conv.content,
            'created_at': conv.created_at,
            'updated_at': conv.updated_at,
            'customer': conv.customer_id,
            'case': conv.case_id,
            'merchants': [merchant.id for merchant in conv.merchants]
        }
        for conv in conversations
    ]
    
    return jsonify(conversations_data), 200

# 通過顧客查詢對話紀錄的路由
@chat.route('/conversations/customer/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_conversations_by_customer(customer_id):
    conversations = Conversation.query.filter_by(customer_id=customer_id).all()
    if not conversations:
        return jsonify({'message': 'No conversations found for this customer'}), 404
    
    conversations_data = [
        {
            'id': conv.id,
            'content': conv.content,
            'created_at': conv.created_at,
            'updated_at': conv.updated_at,
            'case': conv.case_id,
            'merchants': [merchant.id for merchant in conv.merchants]
        }
        for conv in conversations
    ]
    
    return jsonify(conversations_data), 200