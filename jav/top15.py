from . import *

url = "https://jable.tv/hot/"


def get_top15():
    """
    获取热门番号
    """
    with QproDefaultConsole.status("正在打开浏览器") as st:
        driver = getDriver()
        st.update("正在打开网页")
        driver.get(url)
        st.update("正在解析榜单")
        from selenium.webdriver.common.by import By

        res = []

        infos = driver.find_elements(By.CLASS_NAME, "video-img-box")
        for info in infos:
            _ls = (
                info.find_element(By.CLASS_NAME, "title")
                .find_element(By.TAG_NAME, "a")
                .text.strip()
                .split()
            )
            designation = _ls[0]
            title = _ls[1:-1]
            author = _ls[-1]

            _ls = info.find_element(By.CLASS_NAME, "sub-title").text.strip().split("\n")
            watched = int(_ls[0].replace(" ", ""))
            liked = int(_ls[1].replace(" ", ""))

            res.append(
                {
                    "designation": designation,
                    "title": title,
                    "actress": author,
                    "watched": watched,
                    "liked": liked,
                }
            )
    return sorted(res, key=lambda x: (x["liked"], x["watched"]), reverse=True)[:15]
