# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 19:44:05 2024

@author: g8920
"""

# user_api

from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import  jwt_required 
from flask_sqlalchemy import SQLAlchemy
from models import Customer, Login, Case, Merchant
from database import db
from flask_jwt_extended import get_jwt_identity


customer = Blueprint('customer', __name__)

# 新增帳號的路由
@customer.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if not all([name, email, username, password]):
        return jsonify({'message': 'Missing fields'}), 400
    if Customer.query.filter_by(email=email).first() or Login.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    new_customer = Customer(name=name, email=email)
    db.session.add(new_customer)
    db.session.commit()
    new_login = Login(username=username, password=password, customer=new_customer)
    db.session.add(new_login)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201


# 將任務加進購物車
@customer.route('/add_to_cart/<case_id>', methods=['POST'])
@jwt_required()
def add_to_cart(case_id):
    current_user = get_jwt_identity()  # 獲取當前用戶的 ID
    customer = Customer.query.filter_by(id=current_user).first()
    if not customer:
        return jsonify({'message': 'User not found'}), 404

    case = Case.query.get(case_id)
    if not case:
        return jsonify({'message': 'Case not found'}), 404

    # 添加任務到用戶購物車
    # 這裡假設您已經定義了 Customer 模型中儲存購物車的字段，例如 cart
    # 可以使用列表或其他數據結構來儲存 任務 ID
    customer.cases.append(case_id)  # 添加任務 ID 到購物車
    db.session.commit()
    return jsonify({'message': 'Task added to cart successfully'}), 201


if __name__ == '__main__':
    pass



