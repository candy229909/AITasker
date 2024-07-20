from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

# 創建 Flask 應用
app = Flask(__name__)

# 設置配置
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversation_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production

# 初始化擴展
db = SQLAlchemy(app)
jwt = JWTManager(app)

# 從你的 Blueprint 模塊中導入並註冊 Blueprint
from your_package.auth.routes import auth_bp
from your_package.conversations.routes import conversations_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(conversations_bp, url_prefix='/conversations')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
