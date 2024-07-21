from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from models import Login
from models import Customer
from database import db

auth = Blueprint('auth', __name__)

jwt = JWTManager()

# 新增帳號的路由
@auth.route('/register', methods=['POST'])
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

# 用戶登錄生成 JWT 的路由
@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    login = Login.query.filter_by(username=username).first()
    if login and login.password == password:
        access_token = create_access_token(identity=login.id)
        return jsonify({'token': access_token})
    return jsonify({'message': 'Invalid credentials'}), 401