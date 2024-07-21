# main
import os
from flask_cors import CORS
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from sqlalchemy.orm import validates
from models import Login
from blueprints import register_blueprints

# 創建 Flask 應用
app = Flask(__name__)

# 設置配置
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # 使用 SQLite 数据库，文件名为 app.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production

# 初始化擴展
jwt = JWTManager(app)
CORS(app)

# 保護的路由範例，只能在驗證 JWT 後訪問
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    login = Login.query.get(user_id)
    return jsonify({'message': f'Hello, {login.customer.name}'})

register_blueprints(app)


if __name__ == '__main__':
    app.run(debug=True)
    