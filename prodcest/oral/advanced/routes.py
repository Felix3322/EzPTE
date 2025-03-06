# PTE/prodcest/oral/advanced/routes.py
from flask import Blueprint, render_template
from flask_login import login_required
from membership import 会员专属

# 定义口语高级蓝图，模板目录为 templates/prodcest/oral/advanced
高级口语蓝图 = Blueprint("高级口语蓝图", __name__, template_folder='templates/prodcest/oral/advanced')

@高级口语蓝图.route('/')
@login_required
@会员专属
def 高级口语首页():
    # 返回口语高级功能的模板（例如 templates/prodcest/oral/advanced/index.html）
    return render_template('index.html')
