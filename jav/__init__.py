import os
import re
import sys

import requests
from QuickStart_Rhy.NetTools import headers
from QuickProject import (
    _ask,
    QproDefaultConsole,
    QproInfoString,
    QproErrorString,
    user_lang,
    user_pip,
    external_exec,
    QproDefaultStatus
)

from .__config__ import JavConfig

config = JavConfig()
site = "javdb"
disable_translate = config.select("disable_translate")
famous_actress = config.select("famous_actress")
terminal_font_size = int(config.select("terminal_font_size"))

info_baseUrl = "https://javtxt.com"

def requirePackage(
    pname: str,
    module: str = "",
    real_name: str = "",
    not_exit: bool = True,
    not_ask: bool = False,
    set_pip: str = user_pip,
):
    """
    获取本机上的python第三方库，如没有则询问安装

    :param not_ask: 不询问，无依赖项则报错
    :param set_pip: 设置pip路径
    :param pname: 库名
    :param module: 待引入的模块名，可缺省
    :param real_name: 用于 pip3 install 的名字
    :param not_exit: 安装后不退出
    :return: 库或模块的地址
    """
    try:
        exec(f"from {pname} import {module}" if module else f"import {pname}")
    except (ModuleNotFoundError, ImportError):
        if not_ask:
            return None
        if _ask(
            {
                "type": "confirm",
                "name": "install",
                "message": f"""jav require {pname + (' -> ' + module if module else '')}, confirm to install?
  Qs 依赖 {pname + (' -> ' + module if module else '')}, 是否确认安装?""",
                "default": True,
            }
        ):
            with QproDefaultConsole.status(
                "Installing..." if user_lang != "zh" else "正在安装..."
            ):
                external_exec(
                    f"{set_pip} install {pname if not real_name else real_name} -U",
                    True,
                )
            if not_exit:
                exec(f"from {pname} import {module}" if module else f"import {pname}")
            else:
                QproDefaultConsole.print(
                    QproInfoString, f'just run again: "{" ".join(sys.argv)}"'
                )
                exit(0)
        else:
            exit(-1)
    finally:
        return eval(f"{module if module else pname}")


def translate(content):
    if disable_translate:
        return content

    from QuickStart_Rhy.apiTools import translate as _translate

    raw = content
    try:
        content = _translate(content)
    except Exception as e:
        QproDefaultConsole.print(QproErrorString, "翻译失败: {}".format(repr(e)))
        content = raw
    return content


def imgsConcat(imgs_url: list):
    """
    合并图片
    """
    from QuickStart_Rhy.ImageTools.ImageTools import imgsConcat as _imgsConcat
    from QuickStart_Rhy.NetTools.MultiSingleDL import multi_single_dl_content_ls

    try:
        imgs = [
            i
            for i in multi_single_dl_content_ls(
                imgs_url, referer=imgs_url[0].split("/")[2]
            )
            if i
        ]
    except:
        QproDefaultConsole.print(QproErrorString, "样品图获取失败!")
        return

    return _imgsConcat(imgs)


def cover_func_wrapper(func):
    """
    封面图片获取函数装饰器

    :param func: lambda description: img_url
    """

    def wrapper(designations: list, set_covername: str = "", **kwargs):
        """
        封面图片获取函数装饰器

        :param designations: 番号列表
        :param set_covername: 设置封面图片名称
        """
        try:
            from QuickStart_Rhy.NetTools.NormalDL import normal_dl

            failed = []
            for designation in designations:
                try:
                    img = func(designation, **kwargs)
                    from .sites import get_fileinfo, backup_img

                    if not get_fileinfo(img)[0]:
                        img = backup_img(designation)
                    img = normal_dl(img)
                    suffix = img.split(".")[-1]
                    filename = (
                        f"{designation}.{suffix}"
                        if not set_covername
                        else f"{set_covername}.{suffix}"
                    )
                    os.rename(img, filename)
                    QproDefaultConsole.print(QproInfoString, f"图片名: {filename}")
                    QproDefaultConsole.print("-" * QproDefaultConsole.width)
                except Exception as e:
                    failed.append(designation)
            if failed:
                QproDefaultConsole.print(QproErrorString, "封面图获取失败: {}".format(failed))
        except Exception as e:
            QproDefaultConsole.print(QproErrorString, "出现错误: {}".format(e))

    return wrapper


def info_func_wrapper(func):
    """
    番号信息获取函数装饰器

    :param func: lambda designation: {'img': '', 'imgs': '', 'title': ''}
    """

    def wrapper(designation: str, **kwargs):
        """
        番号信息获取函数装饰器

        :param designations: 番号列表
        """
        try:
            raw_info = func(designation, **kwargs)
            if not raw_info:
                QproDefaultConsole.print(
                    QproErrorString, "番号信息获取失败: {}, 启用备用封面获取器。".format(designation)
                )
                from .sites import backup_img

                raw_info = {
                    "img": backup_img(designation),
                    "imgs": [],
                    "title": designation,
                }
            with QproDefaultConsole.status("查询番号信息") as st:
                from bs4 import BeautifulSoup

                html = requests.get(
                    f"{info_baseUrl}/search?type=id&q={designation}/", headers=headers
                ).text
                html = BeautifulSoup(html, "html.parser")
                sub_url = html.find("a", class_="work")["href"]
                html = requests.get(f"{info_baseUrl}{sub_url}", headers=headers).text
                content = re.findall("<p>(.*?)</p>", html)[0]
                dl_content = re.findall("<dl>(.*?)</dl>", html, re.S)[0]
                dl_content = re.findall(
                    "<dd>(.*?)</dd>.*?<dt>(.*?)</dt>", dl_content, re.S
                )
                if not content:
                    return
                from QuickStart_Rhy import cut_string
                from QuickStart_Rhy.TuiTools.Table import qs_default_table

                table = qs_default_table(
                    [
                        {"header": "关键词", "justify": "left"},
                        {"header": "描述", "justify": "left"},
                    ],
                    title=raw_info["title"] + "\n",
                )

                st.update("准备展示")
                table.add_row(
                    "🗒️  简介",
                    " ".join(cut_string(content, QproDefaultConsole.width - 17)),
                )
                raw_info["plot"] = content
                for item in dl_content:
                    if "番号" in item[0] or "厂牌" in item[0]:
                        continue
                    item = list(item)
                    if item[0][1] != " " and "导演" not in item[0]:
                        item[0] = item[0][0] + " " + item[0][1:]
                    if "<a" in item[1]:
                        item[1] = " ".join(re.findall("<a.*?>(.*?)</a>", item[1]))
                    if "导演" in item[0]:
                        item[1] = "  " + item[1]
                    if "时间" in item[0]:
                        raw_info["date"] = item[1]
                    table.add_row(*item)
                table.show_header = False
            return raw_info, table
        except Exception as e:
            QproDefaultConsole.print(QproErrorString, "出现错误: {}".format(e))
            return raw_info, None

    return wrapper


_driver = None


def getLocalDriver():
    global _driver

    if _driver is None:
        from selenium import webdriver

        # options = webdriver.ChromeOptions()
        # options.add_argument("headless")

        _driver = webdriver.Chrome()
    return _driver


def getRemoteDriver():
    global _driver

    if _driver is None:
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server={}".format(config.select("remote_proxy")))

        _driver = webdriver.Remote(
            command_executor=config.select("remote_url"),
            options=options,
        )
    return _driver


def getDriver():
    if config.select("remote_url"):
        return getRemoteDriver()
    else:
        return getLocalDriver()


def closeDriver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver.quit()
        _driver = None
