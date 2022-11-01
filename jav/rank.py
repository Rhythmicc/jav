import time
from . import info_baseUrl, translate

companies = {
    "S1 NO.1 STYLE": f"{info_baseUrl}/studio/763?page=",
    "Prestige": f"{info_baseUrl}/studio/671?page=",
    "SOD Create": f"{info_baseUrl}/studio/1334?page=",
    "Faleno": f"{info_baseUrl}/studio/4411?page=",
    "MOODYZ": f"{info_baseUrl}/studio/294?page=",
    "IDEA POCKET": f"{info_baseUrl}/studio/109?page=",
}


def ask_company():
    from QuickProject import _ask

    return _ask(
        {
            "type": "list",
            "name": "company",
            "message": "请选择公司",
            "choices": list(companies.keys()),
        }
    )


def get_page(company: str, page: int):
    from . import requests
    from bs4 import BeautifulSoup

    url = companies[company]
    infos = []
    retry = 3

    from . import QproDefaultConsole, QproErrorString
    from QuickProject import QproWarnString

    with QproDefaultConsole.status("正在获取榜单..."):
        while retry:
            try:
                r = requests.get(url + f"{page}")
                if r.status_code == 200:
                    break
            except:
                QproDefaultConsole.print(QproWarnString, "获取失败，正在重试...")
            finally:
                retry -= 1
                time.sleep(1)
    if r.status_code != 200:
        QproDefaultConsole.print(QproErrorString, "获取榜单失败, 请检查网络连接!")
        return None
    soup = BeautifulSoup(r.text, "html.parser")

    from QuickStart_Rhy.TuiTools.Bar import NormalProgressBar

    ls = soup.find_all("a", class_="work")
    progress, task_id = NormalProgressBar("解析与翻译", len(ls))
    progress.start()
    progress.start_task(task_id)

    for info in ls:
        designation = info.find("h4", class_="work-id").text.strip()
        title = info.find("h4", class_="work-title").text.strip()
        _ls = info.find_all("span")
        date = _ls[1].text.strip()
        actress = "未知"
        if len(_ls) > 2:
            actress = _ls[2].text.strip()

        infos.append(
            {
                "designation": designation.upper(),
                "title": translate(title),
                "date": date,
                "actress": actress,
            }
        )
        time.sleep(0.2)
        progress.advance(task_id)
    progress.stop_task(task_id)
    progress.stop()

    QproDefaultConsole.clear()

    return infos
