# membership.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from functools import wraps

数据库 = SQLAlchemy()
加密器 = Bcrypt()
登录管理 = LoginManager()

# 用户模型，包含会员状态
class 用户表(数据库.Model, UserMixin):
    id = 数据库.Column(数据库.Integer, primary_key=True)
    用户名 = 数据库.Column(数据库.String(20), unique=True, nullable=False)
    密码 = 数据库.Column(数据库.String(60), nullable=False)
    是否会员 = 数据库.Column(数据库.Boolean, default=False)

@登录管理.user_loader
def 加载用户(user_id):
    return 用户表.query.get(int(user_id))

def 创建数据库():
    数据库.create_all()

# 定义用户管理蓝图（登录、注册、登出）
会员蓝图 = Blueprint('会员蓝图', __name__, template_folder='templates/membership')

class 注册表单(FlaskForm):
    用户名 = StringField("用户名", validators=[DataRequired(), Length(min=2, max=20)])
    密码 = PasswordField("密码", validators=[DataRequired(), Length(min=6)])
    确认密码 = PasswordField("确认密码", validators=[DataRequired(), EqualTo('密码', "两次密码不一致")])
    是否会员 = BooleanField("开通会员")  # 简单示例
    提交 = SubmitField("注册")

class 登录表单(FlaskForm):
    用户名 = StringField("用户名", validators=[DataRequired()])
    密码 = PasswordField("密码", validators=[DataRequired()])
    提交 = SubmitField("登录")

@会员蓝图.route('/register', methods=['GET', 'POST'])
def 注册():
    if current_user.is_authenticated:
        return redirect(url_for('首页'))
    form = 注册表单()
    if form.validate_on_submit():
        hash_pwd = 加密器.generate_password_hash(form.密码.data).decode('utf-8')
        新用户 = 用户表(用户名=form.用户名.data, 密码=hash_pwd, 是否会员=form.是否会员.data)
        数据库.session.add(新用户)
        数据库.session.commit()
        flash("注册成功，请登录！", "success")
        return redirect(url_for('会员蓝图.登录'))
    return render_template('register.html', form=form)

@会员蓝图.route('/login', methods=['GET', 'POST'])
def 登录():
    if current_user.is_authenticated:
        return redirect(url_for('首页'))
    form = 登录表单()
    if form.validate_on_submit():
        用户数据 = 用户表.query.filter_by(用户名=form.用户名.data).first()
        if 用户数据 and 加密器.check_password_hash(用户数据.密码, form.密码.data):
            from flask_login import login_user
            login_user(用户数据)
            flash("登录成功！", "success")
            return redirect(url_for('首页'))
        else:
            flash("用户名或密码错误", "danger")
    return render_template('login.html', form=form)

@会员蓝图.route('/logout')
def 登出():
    from flask_login import logout_user
    logout_user()
    flash("您已退出登录", "info")
    return redirect(url_for('首页'))

# 会员专属装饰器：要求已登录且为会员
def 会员专属(功能):
    @wraps(功能)
    def 包装(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('会员蓝图.登录'))
        if not current_user.是否会员:
            abort(403, "对不起，您不是会员，没有权限访问此功能")
        return 功能(*args, **kwargs)
    return 包装
