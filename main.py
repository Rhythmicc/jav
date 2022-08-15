import os
import re
import time

import requests
from QuickStart_Rhy import headers
from QuickProject.Commander import Commander
from QuickStart_Rhy.NetTools.NormalDL import normal_dl
from QuickProject import QproDefaultConsole, QproErrorString, QproInfoString, QproWarnString


app = Commander(True)
img_baseUrl = 'https://www.busjav.fun'
info_baseUrl = 'https://javtxt.com'

nfo_template = """\
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<movie>
  <plot><![CDATA[{plot}]]></plot>
  <outline />
  <lockdata>false</lockdata>
  <dateadded>{date} 00:00</dateadded>
  <title>{title}</title>
  <sorttitle>{designation}</sorttitle>
</movie>\
"""

def _cover(designations: list, set_covername: str = ''):
    """
    下载多个封面

    :param designations: 封面的标识
    """
    failed = []
    for designation in designations:
        try:
            headers['Referer'] = img_baseUrl
            html = requests.get(f'{img_baseUrl}/{designation.upper()}/', headers=headers).text
            img = re.findall('<a.*?bigImage.*?src="(.*?)"', html)
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
        filename = f'{designation}.{suffix}' if not set_covername else f'{set_covername}.{suffix}'
        os.rename(img, filename)
        QproDefaultConsole.print(QproInfoString, f'图片名: {filename}')
        QproDefaultConsole.print('-' * QproDefaultConsole.width)
    if failed:
        QproDefaultConsole.print(QproErrorString, f'失败: {failed}')


def translate(content):
    from QuickStart_Rhy.api import translate as _translate
    content = _translate(content)
    while content.startswith('[ERROR] 请求失败了'):
        content = _translate(content)
        time.sleep(1)
    return content


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


def _info(designation: str):
    """
    查询番号信息

    :param designation: 番号
    """
    raw_info = {}
    raw_info['designation'] = designation
    headers['Referer'] = img_baseUrl
    html = requests.get(f'{img_baseUrl}/{designation.upper()}/', headers=headers).text
    img = re.findall('<a.*?bigImage.*?src="(.*?)".*?title="(.*?)"', html)
    if img:
        img, title = img[0]
        img = img_baseUrl + '/' + img
        raw_info['img'] = img
        raw_info['title'] = translate(title)
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

    html = requests.get(f'{info_baseUrl}/search?type=id&q={designation}/', headers=headers).text
    html = BeautifulSoup(html, 'lxml')
    sub_url = html.find('a', class_='work')['href']
    html = requests.get(f'{info_baseUrl}{sub_url}', headers=headers).text
    content = re.findall('<p>(.*?)</p>', html)[0]
    dl_content = re.findall('<dl>(.*?)</dl>', html, re.S)[0]
    dl_content = re.findall('<dd>(.*?)</dd>.*?<dt>(.*?)</dt>', dl_content, re.S)
    if not content:
        return
    from QuickStart_Rhy import cut_string
    from QuickStart_Rhy.TuiTools.Table import qs_default_table

    table = qs_default_table([{
        'header': '关键词',
        'justify': 'left'
    }, {
        'header': '描述',
        'justify': 'left'
    }], title=raw_info['title'] + '\n')
    
    content = translate(content)
    table.add_row(*['🗒️  简介', ' '.join(cut_string(content, QproDefaultConsole.width - 17))])
    raw_info['plot'] = content
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
        if '时间' in item[0]:
            raw_info['date'] = item[1]
        table.add_row(*item)
    table.show_header = False
    QproDefaultConsole.print(table, justify='center')
    return raw_info


@app.command()
def info(designation: str):
    """
    查询番号信息和链接

    :param designation: 番号
    """
    info = _info(designation)
    from QuickProject import _ask
    if not _ask({
        'type': 'confirm',
        'name': 'confirm',
        'message': '是否下载?',
        'default': True
    }):
        return
    from QuickProject import requirePackage
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
    else:
        QproDefaultConsole.print(QproInfoString, f'链接: {url}')
    
    if not _ask({
        'type': 'confirm',
        'name': 'confirm',
        'message': '是否保存封面并导出nfo文件?',
        'default': True
    }):
        return
    img_filename = normal_dl(info['img'])
    suffix = img_filename.split('.')[-1]
    if not os.path.exists(f'folder.{suffix}'):
        os.rename(img_filename, f'folder.{suffix}')
        img_filename = f'folder.{suffix}'
    QproDefaultConsole.print(QproInfoString, f'封面已保存为 "{img_filename}"')
    info.pop('img')
    with open(f'{designation}.nfo', 'w') as f:
        f.write(nfo_template.format(**info))
    QproDefaultConsole.print(QproInfoString, f'nfo文件已保存为 "{designation}.nfo"')


if __name__ == '__main__':
    app()
