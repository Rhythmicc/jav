import os
import re
import sys

import requests
from QuickStart_Rhy import headers
from QuickProject.Commander import Commander
from QuickStart_Rhy.NetTools.NormalDL import normal_dl
from QuickProject import QproDefaultConsole, QproErrorString, QproInfoString


app = Commander()


@app.command()
def cover(designations: list):
    """
    下载多个封面

    :param designations: 封面的标识
    """
    failed = []
    for designation in designations:
        try:
            html = requests.get(f'https://www5.javmost.com/search/{designation}/', headers=headers).text
            img = re.findall('<img.*?card-img-top.*?data-src="(.*?)"', html)
            if img:
                img = img[0]
            else:
                QproDefaultConsole.print(QproErrorString, f'{designation} 未找到!')
                failed.append(designation)
                continue
            if img == '${element.cover}':
                QproDefaultConsole.print(QproErrorString, f'{designation} 未找到!')
                failed.append(designation)
                continue
            if img.startswith('//'):
                img = f'http:{img}'
            img = normal_dl(img)
        except:
            QproDefaultConsole.print(QproErrorString, f'{designation} 下载失败!')
            failed.append(designation)
            continue
        suffix = img.split('.')[-1]
        os.rename(img, f'{designation}.{suffix}')
        QproDefaultConsole.print(QproInfoString, f'图片名: {designation}.{suffix}')
        QproDefaultConsole.print('-' * QproDefaultConsole.width)
    if failed:
        QproDefaultConsole.print(QproErrorString, f'失败: {failed}')


@app.command()
def info(designation: str):
    """
    查询番号信息

    :param designation: 番号
    """
    html = requests.get(f'https://www5.javmost.com/search/{designation}/', headers=headers).text
    img = re.findall('<img.*?card-img-top.*?data-src="(.*?)"', html)
    if img:
        img = img[0]
    else:
        QproDefaultConsole.print(QproErrorString, f'{designation} 未找到!')
        return
    if img == '${element.cover}':
        QproDefaultConsole.print(QproErrorString, f'{designation} 未找到!')
        return
    if img.startswith('//'):
        img = f'http:{img}'
    from QuickStart_Rhy.ImageTools.ImagePreview import image_preview
    from bs4 import BeautifulSoup

    image_preview(img)

    info_rt_url = 'https://javtxt.com'
    html = requests.get(f'{info_rt_url}/search?type=id&q={designation}/', headers=headers).text
    html = BeautifulSoup(html, 'lxml')
    sub_url = html.find('a', class_='work')['href']
    html = requests.get(f'{info_rt_url}{sub_url}', headers=headers).text
    content = re.findall('<p>(.*?)</p>', html)[0]
    dl_content = re.findall('<dl>(.*?)</dl>', html, re.S)[0]
    dl_content = re.findall('<dd>(.*?)</dd>.*?<dt>(.*?)</dt>', dl_content, re.S)
    if content:
        from QuickStart_Rhy import cut_string
        from QuickStart_Rhy.api import translate
        from QuickStart_Rhy.TuiTools.Table import qs_default_table

        table = qs_default_table([{
            'header': '关键词',
            'justify': 'left'
        }, {
            'header': '描述',
            'justify': 'left'
        }])
        table.add_row(*['🗒️  简介', ' '.join(cut_string(translate(content), QproDefaultConsole.width - 17))])
        for item in dl_content:
            if '番号' in item[0] or '厂牌' in item[0]:
                continue
            item = list(item)
            if item[0][1] != ' ' and '导演' not in item[0]:
                item[0] = item[0][0] + ' ' + item[0][1:]
            if '<a' in item[1]:
                item[1] = ' '.join(re.findall('<a.*?>(.*?)</a>', item[1]))
            if '导演' in item[0]:
                item[1] = '  ' + item[1]
            table.add_row(*item)
        table.show_header = False
        QproDefaultConsole.print(table, justify='center')


@app.command()
def dl(designation: str):
    """
    查询番号信息和链接

    :param designation: 番号
    """
    app.real_call('info', designation)
    from QuickProject import _ask, requirePackage
    from QuickStart_Rhy import system
    from QuickStart_Rhy.API.SimpleAPI import Designation2magnet

    searcher = Designation2magnet(designation)
    infos = searcher.search_designation()
    choices = [f'[{n + 1}] ' + i[1] + ': ' + i[-1] for n, i in enumerate(infos)]
    url = searcher.get_magnet(
        infos[
            choices.index(_ask({
                'type': 'list',
                'message': 'Select | 选择',
                'name': 'sub-url',
                'choices': choices
            }))
        ][0]
    )

    copy = requirePackage('pyperclip', 'copy', not_ask=True)
    if copy:
        copy(url)
        QproDefaultConsole.print(QproInfoString, '链接已复制!')
        if (system.startswith('darwin') or system.startswith('win')) and _ask({
            'name': 'openInThunder',
            'type': 'confirm',
            'message': 'Open in Thunder? | 打开迅雷?',
            'default': True
        }):
            import os
            if system.startswith('darwin'):
                os.system('open -a Thunder.app')
            elif system.startswith('win'):
                os.system('start /b /min "Thunder"')
    else:
        QproDefaultConsole.print(QproInfoString, f'链接: {url}')


if __name__ == '__main__':
    app()
