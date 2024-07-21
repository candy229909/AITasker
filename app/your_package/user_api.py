# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 19:44:05 2024

@author: g8920
"""

from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import  jwt_required 
from flask_sqlalchemy import SQLAlchemy
from database import Customer, Login, Task
from flask_jwt_extended import get_jwt_identity


user = Blueprint('user', __name__)

app = Flask(__name__)
db = SQLAlchemy(app)

# 新增帳號的路由
@user.route('/register', methods=['POST'])
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

# 将任务加进购物车
@user.route('/add_to_cart/<task_id>', methods=['POST'])
@jwt_required()
def add_to_cart(task_id):
    current_user = get_jwt_identity()  # 获取当前用户的 ID
    customer = Customer.query.filter_by(id=current_user).first()
    if not customer:
        return jsonify({'message': 'User not found'}), 404

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    # 添加任务到用户购物车
    # 这里假设您已经定义了 Customer 模型中存储购物车的字段，例如 cart
    # 可以使用列表或其他数据结构来存储任务 ID
    customer.cases.append(task_id)  # 添加任务 ID 到购物车
    db.session.commit()
    return jsonify({'message': 'Task added to cart successfully'}), 201






