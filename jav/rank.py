from time import time
from . import info_baseUrl

companies = {
    'S1 NO.1 STYLE': f'{info_baseUrl}/studio/763?page=',
    'IDEA POCKET': f'{info_baseUrl}/studio/109?page=',
    'Prestige': f'{info_baseUrl}/studio/671?page=',
    'MOODYZ': f'{info_baseUrl}/studio/294?page=',
}


def ask_company():
    from QuickProject import _ask
    return _ask({
        'type': 'list',
        'name': 'company',
        'message': '请选择公司',
        'choices': list(companies.keys())
    })


def get_page(company: str, page: int):
    from . import requests
    from bs4 import BeautifulSoup

    url = companies[company]
    infos = []
    retry = 3
    
    from . import QproDefaultConsole, QproErrorString

    with QproDefaultConsole.status('正在获取榜单...'):
        while retry:
            r = requests.get(url + f'{page}')
            if r.status_code == 200:
                break
            retry -= 1
            time.sleep(1)
    if r.status_code != 200:
        QproDefaultConsole.print(QproErrorString, '获取榜单失败, 请检查网络连接!')
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    for info in soup.find_all('a', class_='work'):
        designation = info.find('h4', class_='work-id').text.strip()
        title = info.find('h4', class_='work-title').text.strip()
        _ls = info.find_all('span')
        date = _ls[1].text.strip()
        actress = '未知'
        if len(_ls) > 2:
            actress = _ls[2].text.strip()

        infos.append({
            'designation': designation.upper(),
            'title': title,
            'date': date,
            'actress': actress
        })
    return infos
