# experiences/routes.py

from flask import Blueprint, render_template

experiences蓝图 = Blueprint("experiences蓝图", __name__, template_folder='templates/experiences')

@experiences蓝图.route('/')
def experiences首页():
    return render_template('experiences/index.html')
