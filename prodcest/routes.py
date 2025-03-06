# prodcest/routes.py

from flask import Blueprint, render_template
from flask_login import login_required
from membership import 会员专属

# 导入子功能(朗读)
from prodcest.read_aloud.routes import 朗读蓝图

prodcest蓝图 = Blueprint("prodcest蓝图", __name__, template_folder='templates/prodcest')

# 注册朗读子蓝图 => /prodcest/read-aloud/
prodcest蓝图.register_blueprint(朗读蓝图, url_prefix='/read-aloud')

@prodcest蓝图.route('/')
@login_required
@会员专属
def prodcest首页():
    return render_template('prodcest/index.html')
