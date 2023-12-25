from .. import *
from .. import _ask

url = "https://javtxt.com/rank"


def get_top():
    """
    获取热门番号

    :return: [{
        "designation": designation,
        "title": title,
        "actress": author,
        "watched": watched,
        "liked": liked,
    }], header, style
    """
    days = _ask(
        {
            "type": "list",
            "name": "days",
            "message": "请选择天数",
            "choices": ["1", "7", "30", "90"],
            "default": "7",
        }
    )
    from QuickStart_Rhy import cut_string
    from .. import requests
    from bs4 import BeautifulSoup

    html_text = requests.get(url + f"/{days}-days").text
    soup = BeautifulSoup(html_text, "html.parser")
    a_s = soup.find_all("a", class_="work")[:15]

    res = []
    for a in a_s:
        designation = a.find("h4", class_="work-id").text.strip()
        title = a.find("h4", class_="work-title").text.strip()
        actress = a.find("span", class_="work-actress")
        if actress:
            actress = actress.text.strip()
            _flag = 1
        else:
            actress = "未知"
            _flag = 0
        _ls = a.find_all("span")
        studio = _ls[_flag + 0].text.strip()
        date = _ls[_flag + 1].text.strip()

        res.append(
            {
                "designation": designation.split()[0],
                "title": " ".join(
                    cut_string(title, int(QproDefaultConsole.width * 0.45))
                ),
                "actress": actress,
                "studio": studio,
                "date": date,
            }
        )
    return (
        res,
        {
            "date": "发行日期",
            "designation": "番号",
            "title": {"header": "标题", "justify": "left"},
            "actress": "演员",
            "studio": "厂牌",
        },
        {
            "date": "{}",
            "designation": "[bold magenta]{}[/]",
            "title": "{}",
            "actress": "[bold yellow]{}[/]",
            "studio": "[bold green]{}[/]",
        },
    )
