from .. import *

source_name = "guru"


@cover_func_wrapper
def _cover(designation: str):
    """
    下载多个封面

    :param designations: 番号列表
    :param set_covername: 设置封面图片名称
    """
    # ! 此函数返回番号的封面url即可，如果没有封面则 raise Exception("未找到封面")
    designation = designation.upper()
    res = requests.get(f"https://jav.guru/?s={designation}")
    if res.status_code != 200:
        raise Exception("未找到封面")
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(res.text, "lxml")
    tabs = soup.find_all("div", class_="inside-article")
    for tab in tabs:
        if designation in tab.find("h2").text:
            img_url = tab.find("img")["src"].split("-")
            return img_url[0] + "." + img_url[1].split(".")[-1]
    raise Exception("未找到封面")


@info_func_wrapper
def _info(designation: str):
    """
    查询番号信息

    :param designation: 番号
    :return dict: {'img', 'imgs', 'title', 'plot', 'date'}
    """
    # ! 此函数返回 {'img': '', 'imgs': '', 'title': ''}
    with QproDefaultConsole.status("查询番号信息") as st:
        designation = designation.upper()
        st.update("查询番号信息")
        res = requests.get(f"https://jav.guru/?s={designation}")
        _res = {}
        if res.status_code != 200:
            return None
        if "Sorry, nothing good matched." in res.text:
            return None
        from bs4 import BeautifulSoup

        st.update("解析番号信息")
        soup = BeautifulSoup(res.text, "lxml")
        tabs = soup.find_all("div", class_="inside-article")
        _tab = None

        for tab in tabs:
            if designation not in tab.find("h2").text:
                continue
            _tab = tab
            break
        if _tab is None:
            return None
        a_href = _tab.find("a")["href"]
        res = requests.get(a_href)
        if res.status_code != 200:
            return None
        soup = BeautifulSoup(res.text, "lxml")
        maintain_content = soup.find("div", class_="inside-article")
        if not maintain_content:
            QproDefaultConsole.print(QproErrorString, "解析失败")
            return None
        _res["title"] = translate(maintain_content.find("h1").text)
        _res["img"] = maintain_content.find("img")["src"]
        _res["imgs"] = [i["src"] for i in maintain_content.find_all("img")[1:]]
        return _res
