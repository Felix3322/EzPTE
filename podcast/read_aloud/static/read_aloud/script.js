document.addEventListener("DOMContentLoaded", function () {
    const 音频播放器 = document.getElementById("音频播放器");
    const 上一条 = document.getElementById("上一条");
    const 下一条 = document.getElementById("下一条");
    const 中文文本 = document.getElementById("中文文本");
    const 英文文本 = document.getElementById("英文文本");
    const 音频列表 = document.getElementById("音频列表");

    let 资源 = [];
    let 当前索引 = 0;

    fetch("/podcast/read-aloud/资源")
        .then(response => response.json())
        .then(data => {
            资源 = data;
            加载音频列表();
        });

    function 加载音频列表() {
        音频列表.innerHTML = "";
        资源.forEach((项, 索引) => {
            let li = document.createElement("li");
            li.textContent = `音频 ${项.编号}`;
            li.dataset.index = 索引;
            li.addEventListener("click", () => 播放音频(索引));
            音频列表.appendChild(li);
        });
    }

    function 播放音频(索引) {
        if (索引 < 0 || 索引 >= 资源.length) return;
        当前索引 = 索引;
        let 项 = 资源[当前索引];
        音频播放器.src = 项.音频地址;
        音频播放器.play();
    }

    下一条.addEventListener("click", function () {
        播放音频(当前索引 + 1);
    });

    上一条.addEventListener("click", function () {
        播放音频(当前索引 - 1);
    });
});
