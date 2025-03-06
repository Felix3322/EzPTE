from flask import Blueprint, render_template, jsonify, send_from_directory
import os

朗读蓝图 = Blueprint("朗读", __name__, template_folder="templates", static_folder="static")

资源目录 = "资源"
中文文本目录 = os.path.join(资源目录, "文字资源/podcast/read-aloud/中文")
英文文本目录 = os.path.join(资源目录, "文字资源/podcast/read-aloud/英文")
音频目录 = os.path.join(资源目录, "音频资源/podcast/read-aloud")


def 获取资源列表():
    文件列表 = sorted(os.listdir(中文文本目录))
    资源 = []
    for 文件 in 文件列表:
        if 文件.endswith(".txt"):
            文件编号 = 文件.replace(".txt", "")
            资源.append({
                "编号": 文件编号,
                "中文文本": f"/podcast/read-aloud/文本/{文件编号}",
                "英文文本": f"/podcast/read-aloud/文本/{文件编号}",
                "音频地址": f"/podcast/read-aloud/音频/{文件编号}"
            })
    return 资源


@朗读蓝图.route("/", methods=["GET"])
def 主页():
    return render_template("layout.html", 内容模板="read_aloud/content.html")


@朗读蓝图.route("/资源", methods=["GET"])
def 获取资源():
    return jsonify(获取资源列表())


@朗读蓝图.route("/文本/<file_id>", methods=["GET"])
def 获取文本(file_id):
    中文路径 = os.path.join(中文文本目录, f"{file_id}.txt")
    英文路径 = os.path.join(英文文本目录, f"{file_id}.txt")

    if not os.path.exists(中文路径) or not os.path.exists(英文路径):
        return jsonify({"错误": "文件未找到"}), 404

    with open(中文路径, "r", encoding="utf-8") as 中文文件:
        中文内容 = 中文文件.read()

    with open(英文路径, "r", encoding="utf-8") as 英文文件:
        英文内容 = 英文文件.read()

    return jsonify({"编号": file_id, "中文": 中文内容, "英文": 英文内容})



@朗读蓝图.route("/音频/<file_id>", methods=["GET"])
def 获取音频(file_id):
    文件路径 = f"{file_id}.mp3"
    if not os.path.exists(os.path.join(音频目录, 文件路径)):
        return jsonify({"错误": "音频文件未找到"}), 404
    return send_from_directory(音频目录, 文件路径)
