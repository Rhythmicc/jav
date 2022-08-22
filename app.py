from .jav321 import *
from .jav321 import _cover, _info, _web

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
            'default': True
        }):
            img_concated.save(f'{designation}_samples.png')
            QproDefaultConsole.print(QproInfoString, f'已保存为: "{designation}_samples.png"')
    if not _ask({
        'type': 'confirm',
        'name': 'confirm',
        'message': '是否下载?',
        'default': True
    }):
        return
    if _ask({
        'type': 'list',
        'name': 'list',
        'message': '请选择下载方式',
        'choices': ['[1] jav 内置', '[2] 在 jav321 自行提取']
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
    """
    _web(designation)


def main():
    app()


if __name__ == "__main__":
    main()