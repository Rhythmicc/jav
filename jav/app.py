from .source.busjav import *
from .source.busjav import _cover, _info, _web

from QuickProject.Commander import Commander
app = Commander(True)


@app.command()
def cover():
    """
    下载所有的封面
    """
    import os
    
    for rt, _, files in os.walk('.'):
        for file in files:
            suffix = file.split('.')[-1]
            if suffix not in ['mp4', 'mkv']:
                continue
            if os.path.exists(os.path.join(rt, 'folder.jpg')) or os.path.exists(os.path.join(rt, 'folder.png')) or os.path.exists(os.path.join(rt, 'folder.jpeg')):
                continue
            designation = file.split('.')[0]
            QproDefaultConsole.print(QproInfoString, os.path.join(rt, file))
            _cover([designation], set_covername=os.path.join(rt, 'folder'))


@app.command()
def info(designation: str):
    """
    查询番号信息和链接

    :param designation: 番号
    """
    designation = designation.upper()
    info = _info(designation)
    if not info:
        return
    from QuickProject import _ask
    if _ask({
        'type': 'confirm',
        'name': 'confirm',
        'message': f'是否展示样品图片?',
        'default': True
    }):
        from QuickStart_Rhy.ImageTools.ImagePreview import image_preview
        img_concated = imgsConcat(info['imgs'])
        image_preview(img_concated)
        if _ask({
            'type': 'confirm',
            'name': 'confirm',
            'message': f'是否保存样品图片?',
            'default': False
        }):
            img_concated.save(f'{designation}_samples.png')
            QproDefaultConsole.print(QproInfoString, f'已保存为: "{designation}_samples.png"')
    if _ask({
        'type': 'confirm',
        'name': 'confirm',
        'message': '是否下载?',
        'default': True
    }):    
        if _ask({
            'type': 'list',
            'name': 'list',
            'message': '请选择下载方式',
            'choices': ['[1] jav 内置', f'[2] 在 {source_name} 自行提取']
        }) == '[1] jav 内置':
            from QuickStart_Rhy.API.SimpleAPI import Designation2magnet

            searcher = Designation2magnet(designation)
            infos = searcher.search_designation()
            choices = [f'[{n + 1}] ' + i[1] + ': ' + i[-1] for n, i in enumerate(infos)] + ['[-1] 取消']
            ch_index = _ask({
                'type': 'list',
                'message': 'Select | 选择',
                'name': 'sub-url',
                'choices': choices
            })
            if ch_index.startswith('[-1]'):
                return
            url = searcher.get_magnet(
                infos[
                    choices.index(ch_index)
                ][0]
            )

            copy = requirePackage('pyperclip', 'copy', not_ask=True)
            if copy:
                copy(url)
                QproDefaultConsole.print(QproInfoString, '链接已复制!')
            else:
                QproDefaultConsole.print(QproInfoString, f'链接: {url}')
        else:
            app.real_call('web', designation)
    
    if _ask({
        'type': 'confirm',
        'name': 'confirm',
        'message': '是否保存封面并导出nfo文件?',
        'default': False
    }):
        img_filename = normal_dl(info['img'])
        suffix = img_filename.split('.')[-1]
        if not os.path.exists(f'folder.{suffix}'):
            os.rename(img_filename, f'folder.{suffix}')
            img_filename = f'folder.{suffix}'
        QproDefaultConsole.print(QproInfoString, f'封面已保存为 "{img_filename}"')
        if 'img' in info:
            info.pop('img')
        if 'imgs' in info:
            info.pop('imgs')
        with open(f'{designation}.nfo', 'w') as f:
            f.write(nfo_template.format(**info))
        QproDefaultConsole.print(QproInfoString, f'nfo文件已保存为 "{designation}.nfo"')


@app.command()
def web(designation: str):
    """
    通过浏览器获取番号信息

    :param designation: 番号
    """
    _web(designation)


@app.command()
def rank(enable_translate: bool = False):
    """
    查看近期榜单

    :param enable_translate: 是否翻译
    """
    from . import translate, famous_actress
    from QuickProject import _ask
    from .rank import ask_company, get_page
    from QuickStart_Rhy.TuiTools.Table import qs_default_table
    from QuickStart_Rhy import cut_string

    company = ask_company()
    if not company:
        return
    page = 1
    pre_page = 0

    while True:
        if page != pre_page:
            infos = get_page(company, page)

            if enable_translate:
                with QproDefaultConsole.status('正在翻译标题...') as st:
                    import time
                    for _id, info in enumerate(infos):
                        st.update(f'正在翻译第 {_id + 1}/{len(infos)} 项')
                        info['title'] = translate(info['title'])
                        time.sleep(0.2)
            
            table = qs_default_table(['排名', '番号', '发布日期', '演员', {'header': '标题', 'justify': 'left'}], title='近期榜单\n')

            for n, info in enumerate(infos):
                table.add_row(
                    f'[bold cyan]{n + 1}[/bold cyan]', 
                    f'[bold magenta]{info["designation"]}[/bold magenta]', 
                    info['date'][2:],
                    f'[bold yellow]{info["actress"]}[/bold yellow]' if info['actress'] in famous_actress else info["actress"],
                    ' '.join(cut_string(info['title'], QproDefaultConsole.width - 55))
                )
            pre_page = page
        
        QproDefaultConsole.print(table, justify='center')
        QproDefaultConsole.print('-' * QproDefaultConsole.width)
        index = _ask({
            'type': 'input',
            'name': 'input',
            'message': '输入序号查询详细信息(q 取消 | p 上一页 | n 下一页 | r 重新查询)',
            'validate': lambda x: (x.isdigit() and 1 <= int(x) <= len(infos) and int(x) != 0) or x in ['q', 'p', 'n', 'r']
        })
        if index == 'q':
            break
        elif index == 'p':
            if page > 1:
                page -= 1
                QproDefaultConsole.clear()
            else:
                QproDefaultConsole.print(QproInfoString, '已经是第一页了')
        elif index == 'n':
            page += 1
            QproDefaultConsole.clear()
        elif index == 'r':
            QproDefaultConsole.clear()
            page = 1
            pre_page = 0
            company = ask_company()
        else:
            info = infos[int(index) - 1]
            QproDefaultConsole.print(QproInfoString, info["designation"])
            app.real_call('info', info['designation'])
            QproDefaultConsole.clear()


def main():
    app()


if __name__ == "__main__":
    main()
