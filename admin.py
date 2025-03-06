# admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from membership import 数据库, 用户表
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from flask import abort
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates/admin')

def 管理员专属(功能):
    @wraps(功能)
    def 包装(*args, **kwargs):
        if not current_user.is_authenticated or current_user.用户名 != 'admin':
            flash("您没有权限访问后台管理。", "danger")
            return redirect(url_for('首页'))
        return 功能(*args, **kwargs)
    return 包装

@admin_bp.route('/')
@login_required
@管理员专属
def admin_index():
    用户列表 = 用户表.query.all()
    return render_template('admin/index.html', 用户列表=用户列表)

@admin_bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
@管理员专属
def update_user(user_id):
    用户 = 用户表.query.get(user_id)
    if not 用户:
        flash("用户不存在", "danger")
        return redirect(url_for('admin_bp.admin_index'))
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        if new_password:
            用户.密码 = generate_password_hash(new_password)
            数据库.session.commit()
            flash("密码更新成功", "success")
            return redirect(url_for('admin_bp.admin_index'))
    return render_template('admin/update.html', 用户=用户)
