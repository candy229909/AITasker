# main
import os
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import validates
from sqlalchemy import Enum
from database import Login
from conversation import chat
from customer_api import customer
from merchant_api import merchant
from case_api import case
from case_status import case_status

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # 使用 SQLite 数据库，文件名为 app.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
db = SQLAlchemy(app)
jwt = JWTManager(app)

# 用戶登錄生成 JWT 的路由
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    login = Login.query.filter_by(username=username).first()
    if login and login.password == password:
        access_token = create_access_token(identity=login.id)
        return jsonify({'token': access_token})
    return jsonify({'message': 'Invalid credentials'}), 401

# 保護的路由範例，只能在驗證 JWT 後訪問
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    login = Login.query.get(user_id)
    return jsonify({'message': f'Hello, {login.customer.name}'})


app.register_blueprint(chat)
app.register_blueprint(customer)
app.register_blueprint(merchant)
app.register_blueprint(case)
app.register_blueprint(case_status)

with app.app_context():
    db.create_all()  # 在应用上下文内创建数据库表


if __name__ == '__main__':
    app.run(debug=True)
    