from .. import *

search_url = "https://javdb.com/search?q={designation}&f=all"
img_baseUrl = "https://javdb.com"
source_name = "javdb"
using_selenium = False


def _search(designation: str):
    """
    搜索番号

    :param designation: 番号
    """
    # ! 此函数搜索番号
    res = requests.get(search_url.format(designation=designation))

    if res.status_code != 200:
        raise Exception(f"搜索番号时出错: {res.status_code}")

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(res.text, "html.parser")

    # 搜索结果
    search_results = soup.find_all("div", class_="item")
    if search_results is None:
        raise Exception("未找到番号")
    for item in search_results:
        # 番号
        title_div = item.find("div", class_="video-title")
        strong = title_div.find("strong")
        if strong is None:
            continue
        _designation = strong.text
        if _designation != designation:
            continue
        url = item.find("a").get("href")
        return img_baseUrl + url
    raise Exception("未找到番号")


@cover_func_wrapper
def _cover(designation: str):
    """
    下载多个封面

    :param designations: 番号列表
    :param set_covername: 设置封面图片名称
    """
    # ! 此函数返回番号的封面url即可，如果没有封面则 raise Exception("未找到封面")
    designation = designation.upper()
    url = _search(designation)

    QproDefaultConsole.print(url)

    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f"打开番号网页时出错: {res.status_code}")

    from bs4 import BeautifulSoup

    page = BeautifulSoup(res.text, "html.parser")
    return page.find("img", class_="video-cover").get("src")


@info_func_wrapper
def _info(designation: str):
    """
    查询番号信息

    :param designation: 番号
    :return dict: {'img', 'imgs', 'title', 'plot', 'date'}
    """
    # ! 此函数返回 {'img': '', 'imgs': '', 'title': ''}
    PHOTO_URL = "https://c0.jdbstatic.com/avatars/{prefix}/{actor_id}.jpg"
    designation = designation.upper()
    url = _search(designation)

    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f"打开番号网页时出错: {res.status_code}")

    from bs4 import BeautifulSoup

    page = BeautifulSoup(res.text, "html.parser")

    info = {}
    info["img"] = page.find("img", class_="video-cover").get("src")
    info["title"] = page.find("strong", class_="current-title").text
    info["imgs"] = [i.get("href") for i in page.find_all("a", class_="tile-item")]
    info["imgs"] = [i for i in info["imgs"] if i.startswith("http")]
    
    _info_nav = page.find("nav", class_="movie-panel-info")
    panel_blocks = _info_nav.find_all("div", class_="panel-block")[1:]
    info['date'] = panel_blocks[0].find("span", class_="value").text
    info['length'] = panel_blocks[1].find("span", class_="value").text
    info['director'] = panel_blocks[2].find("span", class_="value").text
    info['studio'] = panel_blocks[3].find("span", class_="value").text
    info['series'] = panel_blocks[4].find("span", class_="value").text
    info['rate'] = re.findall(r'\d+', panel_blocks[5].find("span", class_="value").text)[0]
    info['tag'] = [i.text for i in panel_blocks[6].find_all("a")]
    info['actor'] = []
    for i in panel_blocks[7].find_all("a"):
        href = i.get("href").split('/')[-1]
        info['actor'].append({'name': i.text, 'photo': PHOTO_URL.format(prefix=href[:2].lower(), actor_id=href)})
    
    magnets_content = page.find("div", class_="magnet-links").find_all("div", class_="item")
    info['magnets'] = []
    for _id, i in enumerate(magnets_content):
        info['magnets'].append({
            'id': _id + 1,
            'name': i.find('span', class_="name").text,
            'meta': i.find("span", class_="meta").text,
            'date': i.find("span", class_="time").text,
            'url': i.find("a").get("href")
        })

    info['url'] = url

    return info


def _web(designation: str):
    """
    打开番号网页

    :param designation: 番号
    """
    # ! 此函数打开番号网页
    designation = designation.upper()
    url = _search(designation)

    import webbrowser

    webbrowser.open(url)


if __name__ == "__main__":
    print(_search("SSIS-575"))
