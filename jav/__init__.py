import os
import re

import requests
from QuickStart_Rhy import headers
from QuickStart_Rhy import requirePackage
from QuickProject import QproDefaultConsole, QproErrorString, QproInfoString, QproWarnString

famous_actress = {
    '三上悠亜',
    "河北彩花",
    "桃乃木かな",
    'miru',
    '相沢みなみ',
    '涼森れむ',
    '野々浦暖',
    '明里つむぎ',
    '葵つかさ',
    '深田えいみ',
    '七沢みあ'
}

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


def translate(content):
    import time
    from QuickStart_Rhy.api import translate as _translate
    
    raw = content
    try:
        content = _translate(content)
        while content.startswith('[ERROR] 请求失败了'):
            content = _translate(content)
            time.sleep(1)
    except Exception as e:
        QproDefaultConsole.print(QproErrorString, '翻译失败: {}'.format(repr(e)))
        content = raw
    return content


def imgsConcat(imgs_url: list):
    """
    合并图片
    """
    def is_wide():
        width = QproDefaultConsole.width
        height = QproDefaultConsole.height
        rate = width / height
        return rate > 2

    from io import BytesIO
    from QuickStart_Rhy.NetTools.MultiSingleDL import multi_single_dl_content_ls
    
    Image = requirePackage('PIL', 'Image', 'Pillow')
    try:
        imgs = [Image.open(BytesIO(i)) for i in multi_single_dl_content_ls(imgs_url, referer=imgs_url[0].split('/')[2]) if i]
    except:
        QproDefaultConsole.print(QproErrorString, '样品图获取失败!')
        return

    wide = is_wide()
    heights_len = 4 if wide else 3
    with QproDefaultConsole.status('拼接图片中') as st:
        one_width = QproDefaultConsole.width // heights_len * 16
        imgs = [i.resize((one_width, int(one_width * i.size[1] / i.size[0]))) for i in imgs]
        imgs = sorted(imgs, key=lambda i: -i.size[0] * i.size[1])
        heights = [0] * heights_len
        for i in imgs:
            heights[heights.index(min(heights))] += i.size[1]
        if wide:
            st.update('嗅探最佳拼接方式')
            while max(heights) > one_width * heights_len:
                heights_len += 1
                heights = [0] * heights_len
                one_width = QproDefaultConsole.width // heights_len * 16
                for i in imgs:
                    heights[heights.index(min(heights))] += i.size[1]
        result = Image.new('RGBA', (one_width * heights_len, max(heights)))
        heights = [0] * heights_len
        for i in imgs:
            min_height_index = heights.index(min(heights))
            result.paste(i, (one_width * min_height_index, heights[min_height_index]))
            heights[min_height_index] += i.size[1]
    return result


def cover_func_wrapper(func):
    """
    封面图片获取函数装饰器

    :param func: lambda description: img_url
    """
    def wrapper(designations: list, set_covername: str = '', **kwargs):
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
                    img = normal_dl(img)
                    suffix = img.split('.')[-1]
                    filename = f'{designation}.{suffix}' if not set_covername else f'{set_covername}.{suffix}'
                    os.rename(img, filename)
                    QproDefaultConsole.print(QproInfoString, f'图片名: {filename}')
                    QproDefaultConsole.print('-' * QproDefaultConsole.width)
                except Exception as e:
                    failed.append(designation)
            if failed:
                QproDefaultConsole.print(QproErrorString, '封面图获取失败: {}'.format(failed))
        except Exception as e:
            QproDefaultConsole.print(QproErrorString, '出现错误: {}'.format(e))
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
                QproDefaultConsole.print(QproErrorString, '番号信息获取失败: {}'.format(designation))
                return
            with QproDefaultConsole.status('查询番号信息') as st:
                from bs4 import BeautifulSoup
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
                
                st.update('翻译番号信息')
                content = translate(content)
                st.update('准备展示')
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
        except Exception as e:
            QproDefaultConsole.print(QproErrorString, '出现错误: {}'.format(e))
    return wrapper
