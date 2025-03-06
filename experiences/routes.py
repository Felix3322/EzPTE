# experiences/routes.py
from flask import Blueprint, render_template

experiences蓝图 = Blueprint("experiences蓝图", __name__, template_folder='templates/experiences')

@experiences蓝图.route('/')
def experiences首页():
    return render_template('index.html')  # 对应 templates/experiences/index.html

@experiences蓝图.route('/x1')
def experiencesX1页面():
    return render_template('x1.html')  # 如需更多页面，可按需添加
