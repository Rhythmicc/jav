import os
import re

import requests
from QuickStart_Rhy import headers
from QuickProject.Commander import Commander
from QuickStart_Rhy.NetTools.NormalDL import normal_dl
from QuickProject import QproDefaultConsole, QproErrorString, QproInfoString


app = Commander()


@app.command()
def down(designations: list):
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


if __name__ == '__main__':
    app()
