# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 导入用户管理模块（包含登录/注册及会员判断）
from membership import 数据库, 加密器, 登录管理, 创建数据库, 会员专属, 会员蓝图
# 导入 prodcest 模块及其子功能蓝图
from prodcest.routes import prodcest蓝图
# 导入 experiences 模块蓝图
from experiences.routes import experiences蓝图

def 创建应用():
    应用 = Flask(__name__)
    应用.config['SECRET_KEY'] = '你的密钥_请修改'
    应用.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    应用.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    数据库.init_app(应用)
    加密器.init_app(应用)
    登录管理.init_app(应用)
    登录管理.login_view = '会员蓝图.登录'  # 未登录时重定向至登录页面

    with 应用.app_context():
        创建数据库()

    # 注册用户管理蓝图（登录、注册）
    应用.register_blueprint(会员蓝图, url_prefix='/member')
    # 注册 experiences 模块（公开页面）
    应用.register_blueprint(experiences蓝图, url_prefix='/experiences')
    # 注册 prodcest 模块（会员功能，多级路由）
    应用.register_blueprint(prodcest蓝图, url_prefix='/prodcest')

    @应用.route('/')
    def 首页():
        return render_template('index.html')

    return 应用

if __name__ == '__main__':
    应用实例 = 创建应用()
    应用实例.run(host='0.0.0.0', port=5000, debug=True)
