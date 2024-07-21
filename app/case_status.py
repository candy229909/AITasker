# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 20:14:38 2024

@author: g8920
"""
# task_status
from flask import Blueprint, request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import  jwt_required
from database import Case, Customer, CaseStatus

app = Flask(__name__)
db = SQLAlchemy(app)
case_status = Blueprint('case_status', __name__)

@case_status.route('/wait', methods=['GET'])
def wait():
    case_id = request.args.get('case_id')

    # 使用查询构建器来查询数据库
    case = Case.query.get(case_id)
    if not case:
        return jsonify({'message': 'Case not found'}), 404

    case.status = CaseStatus.wait
    db.session.commit()
    
    return jsonify({'message': 'Case status updated to wait', 'case_id': case.id}), 200

@case_status.route('/find', methods=['GET'])
def find():
    case_id = request.args.get('case_id')

    # 使用查询构建器来查询数据库
    case = Case.query.get(case_id)
    if not case:
        return jsonify({'message': 'Case not found'}), 404

    case.status = CaseStatus.find
    db.session.commit()
    
    return jsonify({'message': 'Case status updated to find', 'case_id': case.id}), 200

@case_status.route('/pend', methods=['GET'])
def pend():
    case_id = request.args.get('case_id')
    
    # 使用查询构建器来查询数据库
    case = Case.query.get(case_id)
    if not case:
        return jsonify({'message': 'Case not found'}), 404

    case.status = CaseStatus.pend
    db.session.commit()
    
    return jsonify({'message': 'Case status updated to pend', 'case_id': case.id}), 200

@case_status.route('/close', methods=['GET'])
def close():
    case_id = request.args.get('case_id')

    # 使用查询构建器来查询数据库
    case = Case.query.get(case_id)
    if not case:
        return jsonify({'message': 'Case not found'}), 404
    
    case.status = CaseStatus.close
    db.session.commit()
    
    return jsonify({'message': 'Case status updated to close', 'case_id': case.id}), 200