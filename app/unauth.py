from flask import Blueprint
from flask import request, jsonify
from database import Case, Merchant # 假設您有 `Product` 和 `Category` 模型
unauth = Blueprint('unauth', __name__)


@unauth.route('/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    case = Case.query.get_or_404(case_id)
    return jsonify({
        'id': case.id,
        'name': case.name,
        'price': case.price,
        'category_id': case.category_id,
        'category_name': case.category.name
    })


@unauth.route('/cases', methods=['GET'])
def get_cases_sorted_high_price():
    cases = Case.query.all()
    cases = Case.query.order_by(Case.price.desc()).all()
    cases_list = []
    for case in cases:
        cases_list.append({
            'id': case.id,
            'name': case.name,
            'price': case.price,
        })
    
    return jsonify(cases_list), 200

@unauth.route('/cases', methods=['GET'])
def get_cases_sorted_low_price():
    cases = Case.query.order_by(Case.price.asc()).all()
    cases_list = []
    for case in cases:
        cases_list.append({
            'id': case.id,
            'name': case.name,
            'price': case.price,
        })

@unauth.route('/merchants', methods=['GET'])
def get_merchants():
    merchants = Merchant.query.all()
    category_list = []
    for category in merchants:
        category_list.append({
            'id': category.id,
            'name': category.name
        })
    return jsonify(category_list)

