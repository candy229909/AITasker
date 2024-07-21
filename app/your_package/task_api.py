# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 20:14:38 2024

@author: g8920
"""



from flask import Blueprint, request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import  jwt_required
from database import Case, Customer

app = Flask(__name__)
db = SQLAlchemy(app)
task = Blueprint('task', __name__)

# 定義購物車
cart = {}

# 新增任務
@jwt_required()
@task.route('/add_task', methods=['POST'])
def add_task():
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
    new_task = Customer(case_number=case_number, budget=budget, price=price, status=status)
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201


# 刪除任務
@task.route('/delete_task/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Customer.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200
