import os
import re

import requests
from QuickStart_Rhy import headers
from QuickStart_Rhy import requirePackage
from QuickStart_Rhy.NetTools.NormalDL import normal_dl
from QuickProject import QproDefaultConsole, QproErrorString, QproInfoString, QproWarnString

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
    
    content = _translate(content)
    while content.startswith('[ERROR] 请求失败了'):
        content = _translate(content)
        time.sleep(1)
    return content


def imgsConcat(imgs_url: list):
    """
    合并图片
    """
    def is_wide():
        width = QproDefaultConsole.width
        height = QproDefaultConsole.height
        rate = width / height
        return rate > 2.5

    from io import BytesIO
    from QuickStart_Rhy.NetTools.MultiSingleDL import multi_single_dl_content_ls
    
    Image = requirePackage('PIL', 'Image', 'Pillow')
    try:
        imgs = [Image.open(BytesIO(i)) for i in multi_single_dl_content_ls(imgs_url, referer=imgs_url[0].split('/')[2])]
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