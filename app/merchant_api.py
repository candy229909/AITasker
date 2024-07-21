# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 19:44:05 2024

@author: g8920
"""

# user_api

from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import  jwt_required 
from flask_sqlalchemy import SQLAlchemy
from database import Customer, Login, Case, Merchant, Tag
from flask_jwt_extended import get_jwt_identity


merchant = Blueprint('merchant', __name__)

app = Flask(__name__)
db = SQLAlchemy(app)

# 新增帳號的路由
@merchant.route('/add_merchant', methods=['POST'])
def add_merchant():
    name = request.json.get('name')
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if not all([name, email, username, password]):
        return jsonify({'message': 'Missing fields'}), 400
    if Merchant.query.filter_by(email=email).first() or Login.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    new_customer = Merchant(name=name, email=email)
    db.session.add(new_customer)
    db.session.commit()
    new_login = Login(username=username, password=password, customer=new_customer)
    db.session.add(new_login)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@merchant.route('/case_experence_add', methods=['POST'])
def case_experence_add():
    user_id = request.json.get('user_id')
    merchant = Merchant.query.get(user_id)
    if merchant:
        now_experience = merchant.case_experience
        merchant.case_experience = now_experience + 1
        db.session.commit()
        return jsonify({'message': 'Case experience updated successfully'}), 200
    else:
        return jsonify({'message': 'Merchant not found'}), 404
    

# 取得所有merchants的部分資料
@merchant.route('/merchants', methods=['GET'])
def get_merchants():
    merchants = Merchant.query.all()
    merchants_list = []
    for merchant in merchants:
        merchants_list.append({
            'id': merchant.id,
            'name': merchant.name
        })
    return jsonify(merchants_list)

# 取得單一merchant的詳細資料
@merchant.route('/get_merchant/<int:merchant_id>', methods=['GET'])
def get_merchant(merchant_id):
    merchant = Case.query.get_or_404(merchant_id)
    return jsonify({
        'id': merchant.id,
        'name': merchant.name,
    })


@merchant.route('/merchants_sorted_experience', methods=['GET'])
def merchants_sorted_experience():
    tag_name = request.json.get('tag_name', "code", type=str)
    page = request.json.get('page', 1, type=int)
    query = Merchant.query.join(Merchant.tags)
    query = query.filter(Tag.name == tag_name)
    query = query.order_by(Merchant.case_experience.desc())

    merchants = query.paginate(page, per_page=10, error_out=False)  # 每頁 10 個數據
    
    merchants_list = []
    for merchant in merchants:
        merchants_list.append({
            'id': merchant.id,
            'name': merchant.name,
            'case_experience': merchant.case_experience  # 添加经验值字段
        })
    return jsonify(merchants_list)


if __name__ == '__main__':
    pass



