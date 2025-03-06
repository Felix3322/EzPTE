from flask import Flask, render_template
from podcast.read_aloud.routes import 朗读蓝图

应用 = Flask(__name__)

# 注册蓝图
应用.register_blueprint(朗读蓝图, url_prefix="/podcast/read-aloud")


@应用.route("/")
def 主页():
    return render_template("layout.html", 内容模板="read_aloud/content.html")


if __name__ == "__main__":
    应用.run(host="0.0.0.0", port=5000, debug=True)
