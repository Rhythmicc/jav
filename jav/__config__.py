import os
import json
from QuickProject import user_root, _ask, QproDefaultStatus

config_path = os.path.join(user_root, ".jav", "config.json")


problems = {
    "terminal_font_size": {
        "type": "input",
        "message": "请输入终端字体大小(默认为 16):",
        "default": "16",
    },
    "wish_list_path": {
        "type": "input",
        "message": "请输入心愿单路径(默认为 ~/.jav/wish_list.json):",
        "default": os.path.join(user_root, ".jav", "wish_list.json"),
    },
    "disable_translate": {
        "type": "confirm",
        "message": "是否禁用翻译(默认为否):",
        "default": False,
    },
    "remote_url": {"type": "input", "message": "请输入远程浏览器URL (无则跳过):"},
    "remote_proxy": {"type": "input", "message": "请输入代理地址 (无则跳过):"},
    "cache_path": {'type': 'input', 'message': '请输入缓存路径(默认为 ~/.jav/cache):', 'default': os.path.join(user_root, '.jav', 'cache')},
}


def init_config():
    """
    初始化配置
    """
    if not os.path.exists(os.path.join(user_root, ".jav")) or not os.path.isdir(
        os.path.join(user_root, ".jav")
    ):
        os.mkdir(os.path.join(user_root, ".jav"))

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "famous_actress": [
                    "三上悠亜",
                    "河北彩花",
                    "桃乃木かな",
                    "miru",
                    "相沢みなみ",
                    "涼森れむ",
                    "野々浦暖",
                    "明里つむぎ",
                    "葵つかさ",
                    "深田えいみ",
                    "七沢みあ",
                    "香水じゅん",
                    "天使もえ",
                    "青空ひかり",
                ],
                "wish_list_path": _ask(problems["wish_list_path"]),
                "disable_translate": _ask(problems["disable_translate"]),
                "remote_url": _ask(problems["remote_url"]),
                "cache_path": os.path.join(user_root, ".jav", "cache"),
            },
            f,
            ensure_ascii=False,
            indent=4,
        )


class JavConfig:
    def __init__(self) -> None:
        if not os.path.exists(config_path):
            init_config()
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def select(self, key):
        if key not in self.config:
            if key in problems:
                self.update(key, _ask(problems[key]))

        return self.config.get(key, None)

    def update(self, key, value):
        self.config[key] = value
        with open(config_path, "w") as f:
            json.dump(self.config, f)
