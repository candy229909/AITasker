# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 20:14:38 2024

@author: g8920
"""

# case_api

from flask import Blueprint, request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import  jwt_required
from models import Case, Customer, CaseStatus, Tag
from database import db

case = Blueprint('case', __name__)


@case.route('/cases_sorted_new', methods=['GET'])
def cases_sorted_new():
    page = request.args.get('page', 1, type=int)  # 默认页码为 1
    status = request.args.get('status', 'wait', type=str)
    tag_name = request.args.get('tag_name', 'code', type=str)
    
    query = Case.query.join(Case.tags).filter(Tag.name == tag_name)
    if status:
        query = query.filter(Case.status == status)
    query = query.order_by(Case.created_at.desc())
    
    cases = query.paginate(page, per_page=10, error_out=False)  # 每頁 10 個數據
    case_list = []
    for case in cases.items:
        case_list.append({
            'id': case.id,
            'case_number': case.case_number,
            'budget': case.budget,
            'price': case.price,
            'status': case.status,
            'created_at': case.created_at.isoformat(),  # 將日期時間轉換為 ISO 格式
            # ... 添加其他需要的字段 ...
        })

    return jsonify({
        'cases': case_list,
        'has_next': cases.has_next,  # 是否有下一頁
        'has_prev': cases.has_prev   # 是否有上一頁
    })

    
@case.route('/cases_sorted_high_price', methods=['GET'])
def cases_sorted_high_price():
    page = request.args.get('page', 1, type=int) # 默认页码为 1
    status = request.args.get('status', 'find', type=str)
    tag_name = request.args.get('tag_name', 'code', type=str)
    
    query = Case.query.join(Case.tags).filter(Tag.name == tag_name)
    if status:
        query = query.filter(Case.status == status)
    query = query.order_by(Case.price.desc())
    
    cases = query.paginate(page, per_page=10, error_out=False)  # 每頁 10 個數據
    cases_list = []
    for case in cases:
        cases_list.append({
            'id': case.id,
            'case_number': case.case_number,
            'budget': case.budget,
            'price': case.price,
            'status': case.status,
            'created_at': case.created_at.isoformat(),  # 將日期時間轉換為 ISO 格式
        })
    return jsonify({
        'cases': cases_list,
        'has_next': cases.has_next,  # 是否有下一頁
        'has_prev': cases.has_prev   # 是否有上一頁
    })

@case.route('/cases_sorted_low_price', methods=['GET'])
def cases_sorted_low_price():
    page = request.args.get('page', 1, type=int) # 默認頁碼為 1
    tag_name = request.json.get('tag_name', "code", type=str)
    status = request.args.get('status', 'find', type=str)
    
    query = Case.query.join(Case.tags).filter(Tag.name == tag_name)
    if status:
        query = query.filter(Case.status == status)    
    query = query.order_by(Case.price.asc())
    cases = query.paginate(page, per_page=10, error_out=False)  # 每頁 10 個數據

    cases_list = []
    for case in cases:
        cases_list.append({
            'id': case.id,
            'case_number': case.case_number,
            'budget': case.budget,
            'price': case.price,
            'status': case.status,
            'created_at': case.created_at.isoformat(),  # 將日期時間轉換為 ISO 格式
        })
    return jsonify({
        'cases': cases_list,
        'has_next': cases.has_next,  # 是否有下一頁
        'has_prev': cases.has_prev   # 是否有上一頁
    })
    
# 新增任務
@jwt_required()
@case.route('/add_case', methods=['POST'])
def add_case():
    data = request.get_json()
    case_number = data.get('case_number')
    budget = data.get('budget')
    price = data.get('price')
    status = data.get('status')
    
    if not all([case_number, budget, price, status]):
        return jsonify({'message': 'Missing fields'}), 400
    
    # 驗證 case_number 是否存在
    case = Case.query.filter_by(case_number=case_number).first()
    if case:
        return jsonify({'message': 'Invalid case number'}), 400
    new_case = Case(case_number=case_number, budget=budget, price=price, status=status)
    new_case.status = CaseStatus.wait
    db.session.add(new_case)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201


# 刪除任務
@case.route('/delete_case/<case_id>', methods=['DELETE'])
@jwt_required()
def delete_case(case_id):
    case = Customer.query.get(case_id)
    if not case:
        return jsonify({'message': 'Case not found'}), 404
    db.session.delete(case)
    db.session.commit()
    return jsonify({'message': 'Case deleted successfully'}), 200



