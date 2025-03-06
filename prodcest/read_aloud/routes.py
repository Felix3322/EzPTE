# prodcest/read_aloud/routes.py

from flask import Blueprint, render_template, jsonify, abort, send_file
from flask_login import login_required
from membership import 会员专属
import os

朗读蓝图 = Blueprint("朗读蓝图", __name__, template_folder='templates/prodcest/read_aloud')

# 假定资源路径(中文)
资源目录 = os.path.join("resources", "prodcest", "read_aloud")
音频目录 = os.path.join(资源目录, "audio")
文本目录 = os.path.join(资源目录, "text", "zh")

@朗读蓝图.route('/')
@login_required
@会员专属
def 朗读首页():
    return render_template('index.html')

@朗读蓝图.route('/list', methods=['GET'])
@login_required
@会员专属
def 获取朗读列表():
    文件列表 = []
    for 文件名 in os.listdir(文本目录):
        if 文件名.endswith('.txt'):
            名字 = 文件名[:-4]
            try:
                文件编号 = int(名字)
                文件列表.append(文件编号)
            except ValueError:
                pass
    文件列表.sort()
    返回数据 = []
    for 编号 in 文件列表:
        返回数据.append({
            "编号": str(编号),
            "text_api": f"/prodcest/read-aloud/text/{编号}",
            "audio_api": f"/prodcest/read-aloud/audio/{编号}"
        })
    return jsonify(返回数据)

@朗读蓝图.route('/text/<int:file_id>', methods=['GET'])
@login_required
@会员专属
def 获取文本(file_id):
    文件路径 = os.path.join(文本目录, f"{file_id}.txt")
    if not os.path.exists(文件路径):
        abort(404, "文本不存在")
    with open(文件路径, 'r', encoding='utf-8') as f:
        内容 = f.read().strip()
    return jsonify({"编号": file_id, "text": 内容})

@朗读蓝图.route('/audio/<int:file_id>', methods=['GET'])
@login_required
@会员专属
def 获取音频(file_id):
    文件路径 = os.path.join(音频目录, f"{file_id}.mp3")
    if not os.path.exists(文件路径):
        abort(404, "音频不存在")
    return send_file(文件路径, mimetype='audio/mpeg')
