import os
import json
from QuickProject import user_root, _ask

config_path = os.path.join(user_root, ".jav", "config.json")

problems = {
    "site": {
        "type": "list",
        "name": "list",
        "message": "请选择一个默认数据源",
        "choices": ["busjav", "jav321", "guru"],
        "default": "busjav",
    },
    "terminal_font_size": {
        "type": "input",
        "name": "terminal_font_size",
        "message": "请输入终端字体大小(默认为 16):",
        "default": "16",
    },
    "wish_list_path": {
        "type": "input",
        "name": "wish_list_path",
        "message": "请输入心愿单路径(默认为 ~/.jav/wish_list.json):",
        "default": os.path.join(user_root, ".jav", "wish_list.json"),
    },
    "disable_translate": {
        "type": "confirm",
        "name": "disable_translate",
        "message": "是否禁用翻译(默认为否):",
        "default": False,
    },
}


def ask_sites(site: str):
    return _ask(
        {
            "type": "list",
            "name": "list",
            "message": f"请为 '{site}' 选择一个数据源",
            "choices": ["busjav", "jav321", "guru"],
            "default": "busjav",
        }
    )


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
                "site": _ask(problems["site"]),
                "sites": {
                    "S1 NO.1 STYLE": ask_sites("S1 NO.1 STYLE"),
                    "Prestige": ask_sites("Prestige"),
                    "SOD Create": ask_sites("SOD Create"),
                    "Faleno": ask_sites("Faleno"),
                    "MOODYZ": ask_sites("MOODYZ"),
                    "IDEA POCKET": ask_sites("IDEA POCKET"),
                },
                "terminal_font_size": _ask(problems["terminal_font_size"]),
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
                ],
                "wish_list_path": _ask(problems["wish_list_path"]),
                "disable_translate": _ask(problems["disable_translate"]),
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
            elif key == "sites":
                self.update(
                    key,
                    {
                        "S1 NO.1 STYLE": ask_sites("S1 NO.1 STYLE"),
                        "Prestige": ask_sites("Prestige"),
                        "SOD Create": ask_sites("SOD Create"),
                        "Faleno": ask_sites("Faleno"),
                        "MOODYZ": ask_sites("MOODYZ"),
                        "IDEA POCKET": ask_sites("IDEA POCKET"),
                    },
                )

        return self.config.get(key, None)

    def update(self, key, value):
        self.config[key] = value
        with open(config_path, "w") as f:
            json.dump(self.config, f)
