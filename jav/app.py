from . import *
from .wish import WishList
from QuickProject.Commander import Commander

app = Commander("jav", True)
wish_list = WishList()

@app.command()
def info(designation: str):
    """
    查询番号信息和链接

    :param designation: 番号
    """
    _flag = requirePackage(
        f".sites.{site}",
        "using_selenium",
    )
    _info = requirePackage(f".sites.{site}", "_info")

    if _flag and not driver:
        driver = getDriver()

    designation = designation.upper()
    QproDefaultConsole.clear()
    info, table = _info(designation, driver=driver) if _flag else _info(designation)
    date = requirePackage("datetime", "datetime").strptime(info["date"], "%Y-%m-%d")
    if not info:
        return
    requirePackage("QuickStart_Rhy.ImageTools.ImagePreview", "image_preview")(
        info["img"]
    )
    QproDefaultConsole.print(table, justify="center")

    from QuickProject import _ask

    if _ask(
        {"type": "confirm", "name": "confirm", "message": f"是否展示样品图片?", "default": True}
    ):
        img_concated = imgsConcat(info["imgs"])
        requirePackage("QuickStart_Rhy.ImageTools.ImagePreview", "image_preview")(
            img_concated
        )
    cur_date = requirePackage("datetime", "datetime").now()
    if cur_date > date and _ask(
        {"type": "confirm", "name": "confirm", "message": "是否下载?"}
    ):
        choices = [
            "{id} | {name} | {meta} | {date}".format(**magnet_info)
            for magnet_info in info["magnets"]
        ]
        initial = True
        if res := _ask(
            {
                "type": "list",
                "message": "请选择下载链接",
                "name": "magnet",
                "choices": choices,
                "default": choices[0] if initial else choices[-1],
            }
        ):
            initial = False
            url = info["magnets"][int(res.split()[0]) - 1]["url"]
            downloader = config.select("downloader")
            if not downloader:
                requirePackage("pyperclip", "copy")(url)
                QproDefaultConsole.print(QproInfoString, "已复制到剪贴板:", url)
            else:
                import time
                from selenium.webdriver.common.by import By
                driver = getLocalDriver()
                driver.get(downloader)
                # wait for page to load
                time.sleep(2)                
                driver.find_element(By.CLASS_NAME, "create__task").click()
                driver.find_element(By.CLASS_NAME, 'el-textarea__inner').send_keys(url)
                driver.find_element(By.CLASS_NAME, "task-parse-btn").click()
                time.sleep(0.5)
                driver.find_element(By.CLASS_NAME, "task-parse-btn").click()

        if designation in wish_list.get_list() and _ask(
            {
                "type": "confirm",
                "message": "是否从心愿单中删除?",
                "default": True,
            }
        ):
            wish_list.remove(designation)
            return False
    return cur_date > date


@app.command()
def web(designation: str):
    """
    通过浏览器获取番号信息

    :param designation: 番号
    """
    _web = requirePackage(f".sites.{site}", "_web")
    _web(designation)


@app.command()
def rank(enable_translate: bool = False):
    """
    查看近期榜单

    :param enable_translate: 是否翻译
    """
    from . import translate, famous_actress
    from .rank import ask_company, get_page
    from QuickStart_Rhy.TuiTools.Table import qs_default_table
    from QuickStart_Rhy import cut_string
    from QuickProject import _ask

    company = ask_company()
    if not company:
        return
    page = 1
    pre_page = 0

    while True:
        if page != pre_page:
            infos = get_page(company, page)
            if not infos:
                return

            if enable_translate:
                with QproDefaultConsole.status("正在翻译标题...") as st:
                    import time

                    for _id, info in enumerate(infos):
                        st.update(f"正在翻译第 {_id + 1}/{len(infos)} 项")
                        info["title"] = translate(info["title"])
                        time.sleep(0.2)

            table = qs_default_table(
                ["排名", "番号", "发布日期", "演员", {"header": "标题", "justify": "left"}],
                title="近期榜单\n",
            )

            for n, info in enumerate(infos):
                table.add_row(
                    f"[bold cyan]{n + 1}[/bold cyan]",
                    f'[bold magenta]{info["designation"]}[/bold magenta]',
                    info["date"][2:],
                    f'[bold yellow]{info["actress"]}[/bold yellow]'
                    if info["actress"] in famous_actress
                    else info["actress"],
                    " ".join(cut_string(info["title"], QproDefaultConsole.width - 55)),
                )
            pre_page = page

        QproDefaultConsole.print(table, justify="center")
        QproDefaultConsole.print("-" * QproDefaultConsole.width)
        index = _ask(
            {
                "type": "input",
                "name": "input",
                "message": f'输入序号查询详细信息 (q 取消{" | p 上一页" if page > 1 else ""} | n 下一页 | r 重新查询)',
                "validate": lambda x: (
                    x.isdigit() and 1 <= int(x) <= len(infos) and int(x) != 0
                )
                or x in ["q", "n", "r"] + (["p"] if page > 1 else []),
            }
        )
        if index == "q":
            break
        elif index == "p":
            page -= 1
            QproDefaultConsole.clear()
        elif index == "n":
            page += 1
            QproDefaultConsole.clear()
        elif index == "r":
            QproDefaultConsole.clear()
            page = 1
            pre_page = 0
            company = ask_company()
        else:
            info = infos[int(index) - 1]
            QproDefaultConsole.print(QproInfoString, info["designation"])
            downloadable = app.real_call("info", info["designation"])
            if (
                not downloadable
                and info["designation"] not in wish_list.get_list()
                and _ask(
                    {
                        "type": "confirm",
                        "name": "confirm",
                        "message": "是否添加至心愿单?",
                        "default": True,
                    }
                )
            ):
                wish_list.add(info)
                QproDefaultConsole.print(QproInfoString, "已添加至心愿单")
            QproDefaultConsole.clear()
    QproDefaultConsole.clear()


@app.command()
def wish():
    """
    心愿单
    """
    from QuickStart_Rhy.TuiTools.Table import qs_default_table
    from QuickStart_Rhy import cut_string
    from QuickProject import _ask

    while True:
        _ls = wish_list.get_list()
        _ls_values = list(_ls.values())

        table = qs_default_table(
            ["排名", "番号", "发布日期", "演员", {"header": "标题", "justify": "left"}],
            title="心愿单\n",
        )

        for n, info in enumerate(_ls_values):
            table.add_row(
                f"[bold cyan]{n + 1}[/bold cyan]",
                f'[bold magenta]{info["designation"]}[/bold magenta]',
                info["date"][2:],
                f'[bold yellow]{info["actress"]}[/bold yellow]',
                " ".join(cut_string(info["title"], QproDefaultConsole.width - 55)),
            )
        QproDefaultConsole.print(table, justify="center")
        QproDefaultConsole.print("-" * QproDefaultConsole.width)
        index = _ask(
            {
                "type": "input",
                "name": "input",
                "message": "输入序号查询详细信息 (q 退出)",
                "validate": lambda x: (
                    x.isdigit() and 1 <= int(x) <= len(_ls_values) and int(x) != 0
                )
                or x in ["q"],
            }
        )
        if index == "q":
            break
        else:
            info = _ls_values[int(index) - 1]
            app.real_call("info", info["designation"])
            QproDefaultConsole.clear()


@app.command()
def top():
    """
    查看近期榜单
    """
    from . import _ask
    from .top_k import top_k
    from QuickStart_Rhy.TuiTools.Table import qs_default_table

    infos, header, style = top_k()
    closeDriver()
    if not infos:
        return
    table = qs_default_table(["序号"] + [header[i] for i in header], title="热门榜单\n")

    for n, info in enumerate(infos):
        line = [f"[bold cyan]{n + 1}[/bold cyan]"]
        for item in header:
            line.append(style[item].format(info[item]))
        table.add_row(*line)

    while True:
        QproDefaultConsole.print(table, justify="center")
        QproDefaultConsole.print("-" * QproDefaultConsole.width)
        index = _ask(
            {
                "type": "input",
                "message": "输入序号查询详细信息 (q 退出)",
                "validate": lambda x: (
                    x.isdigit() and 1 <= int(x) <= len(infos) and int(x) != 0
                )
                or x in ["q"],
            }
        )
        if index == "q":
            break
        else:
            info = infos[int(index) - 1]
            app.real_call("info", info["designation"])
            QproDefaultConsole.clear()


@app.command()
def nfo(force: bool = False):
    """
    找到目录下所有视频文件并生成nfo

    :param force: 是否强制更新
    """
    from .nfo import generate_nfo

    generate_nfo(force)


@app.command()
def update():
    """
    更新jav工具
    """
    from QuickProject import user_pip

    with QproDefaultConsole.status("正在更新..."):
        external_exec(
            f"{user_pip} install git+https://github.com/Rhythmicc/jav.git -U", True
        )
    QproDefaultConsole.print(QproInfoString, "更新完成")


def main():
    try:
        app()
        # QproDefaultConsole.clear()
    except:
        QproDefaultConsole.print_exception()
        closeDriver()
    finally:
        closeDriver()
    wish_list.store()


if __name__ == "__main__":
    main()
