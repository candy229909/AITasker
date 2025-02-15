# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 19:44:05 2024

@author: g8920
"""

# user_api

from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import  jwt_required 
from flask_sqlalchemy import SQLAlchemy
from models import Customer, Login, Case, Merchant, Tag
from database import db
from flask_jwt_extended import get_jwt_identity


merchant = Blueprint('merchant', __name__)

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
@merchant.route(' ', methods=['GET'])
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
@merchant.route('/get_merchant_info/<int:merchant_id>', methods=['GET'])
# @jwt_required()
def get_merchant_info(merchant_id):
    merchant = Merchant.query.filter_by(id=merchant_id).first()
    if not merchant:
        return jsonify({'message': 'Merchant not found'}), 404
    tag_name = request.args.get('tag_name', "code", type=str)
    # 獲取該 merchant 關聯的 tags
    tags = [tag.name for tag in merchant.tags]
    if tag_name in tags:
        tags.remove(tag_name)
    # 组装返回數據
    merchant_data = {
        'id': merchant.id,
        'name': merchant.name,
        'email': merchant.email,
        'case_experience': merchant.case_experience,
        'temp_experience': merchant.temp_experience,
        'created_at': merchant.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'tags': tags
    }
    
    return jsonify(merchant_data), 200

@merchant.route('/merchants_sorted_experience', methods=['GET'])
def merchants_sorted_experience():
    tag_name = request.args.get('tag_name', "code", type=str)
    page = request.args.get('page', 1, type=int)
    query = Merchant.query.join(Merchant.tags)
    query = query.filter(Tag.name == tag_name)
    query = query.order_by(Merchant.case_experience.desc())

    merchants = query.paginate(page=page, per_page=10, error_out=False)  # 每頁 10 個數據
    
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



