from .. import *
from .. import _ask

url = "https://javdb.com/rankings/movies?p={days}&t=censored"

def get_top(time_during: str = "week"):
    """
    获取热门番号

    :return: [{
        "designation": designation,
        "title": title,
        "score": score,
    }], header, style
    """
    days = _ask(
        {
            "type": "list",
            "name": "days",
            "message": "请选择天数",
            "choices": ["daily", "weekly", "monthly"],
            "default": "weekly",
        }
    )
    from QuickStart_Rhy import cut_string
    from .. import requests
    from bs4 import BeautifulSoup

    html_text = requests.get(url.format(days=days)).text
    soup = BeautifulSoup(html_text, "html.parser")

    res = []
    for div in soup.find_all("div", class_="item")[:30]:
        date = div.find("div", class_="meta").text.strip()
        designation = div.find("strong").text.strip()
        title = div.find("div", class_="video-title").text.strip()
        title = ' '.join(title.split()[1:])
        score = div.find("span", class_="value").text.strip()
        score, watched = re.findall(r"([0-9]*\.?[0-9]+)?分.*?(\d+)人", score)[0]

        res.append(
            {
                "date": date,
                "designation": designation.split()[0],
                "title": " ".join(cut_string(title, int(QproDefaultConsole.width * 0.7))),
                "score": f'[bold cyan]{score}[/]/{watched}'
            }
        )
    
    return res, {
        "date": "发布日期",
        "designation": "番号",
        "title": {"header": "标题", "justify": "left"},
        "score": "评分",
    }, {
        "date": "{}",
        "designation": "[bold magenta]{}[/]",
        "title": "{}",
        "score": "{}"
    }
