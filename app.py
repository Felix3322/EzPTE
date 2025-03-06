# app.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 用户管理（登录、注册）
from membership import 数据库, 加密器, 登录管理, 创建数据库, 会员蓝图
# 后台（可选）
from admin import admin_bp
# 公开页面（可选）
from experiences.routes import experiences蓝图
# Prodcest 主路由（包含朗读子功能）
from prodcest.routes import prodcest蓝图

def 创建应用():
    应用 = Flask(__name__)
    应用.config['SECRET_KEY'] = 'admin123'
    应用.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    应用.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化
    数据库.init_app(应用)
    加密器.init_app(应用)
    登录管理.init_app(应用)
    登录管理.login_view = '会员蓝图.登录'

    with 应用.app_context():
        创建数据库()

    # 注册蓝图
    应用.register_blueprint(会员蓝图, url_prefix='/member')
    应用.register_blueprint(admin_bp, url_prefix='/admin')
    应用.register_blueprint(experiences蓝图, url_prefix='/experiences')
    应用.register_blueprint(prodcest蓝图, url_prefix='/prodcest')

    @应用.route('/')
    def 首页():
        return render_template('index.html')

    return 应用

if __name__ == '__main__':
    app = 创建应用()
    app.run(host='0.0.0.0', port=5000, debug=True)
