from .. import *
from .. import _ask

root_url = "https://javtxt.com"
url = f"{root_url}/rank"


def last_year():
    from datetime import datetime
    return f"/{datetime.now().year - 1}"


def parse_cn_title_and_abstract(url):
    from .. import requests
    from bs4 import BeautifulSoup

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")

    title = soup.find("h2", class_="text-zh").text.strip()
    info = soup.find("div", class_="text-zh")
    abstract = info.find("p").text.strip()

    return title, abstract


def parse_cn_title(url):
    from .. import requests
    from bs4 import BeautifulSoup

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    title = soup.find("h2", class_="text-zh").text.strip()

    return title

def parallel_parse_title(a_s):
    from QuickStart_Rhy.TuiTools.Bar import NormalProgressBar
    from concurrent.futures import ThreadPoolExecutor 

    progress, task_id = NormalProgressBar("正在获取中文标题", len(a_s))
    progress.start()

    def parse_title(a):
        title = parse_cn_title(f'{root_url}/{a["href"]}')
        progress.advance(task_id)
        return title

    res_ls = None
    with ThreadPoolExecutor() as executor:
        res_ls = list(executor.map(parse_title, a_s))
    progress.stop()
    return res_ls

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
            "choices": ["1", "7", "30", "90", "Year"],
            "default": "7",
        }
    )
    from QuickStart_Rhy import wrap_text_preserve_links
    from .. import requests
    from bs4 import BeautifulSoup

    html_text = requests.get(url + (f"/{days}-days" if days != 'Year' else last_year())).text
    soup = BeautifulSoup(html_text, "html.parser")
    a_s = soup.find_all("a", class_="work")[:15]
    titles = parallel_parse_title(a_s)

    res = []
    with QproDefaultStatus("正在获取热门番号"):
        total = len(a_s)
        for _id, a in enumerate(a_s):
            designation = a.find("h4", class_="work-id").text.strip().split()[0]
            QproDefaultStatus(f"[{_id + 1}/{total}] 正在获取: " + designation)
            # title = parse_cn_title(f'{root_url}/{a["href"]}')
            title = titles[_id]
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
                    "designation": designation,
                    "title": wrap_text_preserve_links(title, int(QproDefaultConsole.width * 0.3)),
                    "actress": actress,
                    "studio": studio,
                    "date": date if is_before_today(date[1:].strip()) else f"[red]{date}[/]",
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
