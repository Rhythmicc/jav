from . import *

img_baseUrl = 'https://www.jav321.com/video'
info_baseUrl = 'https://javtxt.com'
source_name = 'jav321'


def _cover(designations: list, set_covername: str = ''):
    """
    下载多个封面

    :param designations: 封面的标识
    """
    from bs4 import BeautifulSoup
    failed = []
    for designation in designations:
        try:
            headers['Referer'] = img_baseUrl
            _ls = designation.lower().split('-')
            html = requests.get(f'{img_baseUrl}/{_ls[0]}{"%05d" % int(_ls[1])}', headers=headers).text
            html = BeautifulSoup(html, 'lxml')
            img = html.find_all('div', class_='col-xs-12 col-md-12')[0].find('img').get('src')
            if not img:
                QproDefaultConsole.print(QproErrorString, f'{designation} 未找到!')
                failed.append(designation)
                continue
            if not img.startswith('http') and not img.startswith('//'):
                img = img_baseUrl + img[0]
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


def _info(designation: str):
    """
    查询番号信息

    :param designation: 番号
    """
    from bs4 import BeautifulSoup

    with QproDefaultConsole.status('查询番号图片信息') as st:
        raw_info = {}
        raw_info['designation'] = designation
        _ls = designation.lower().split('-')
        html = requests.get(f'{img_baseUrl}/{_ls[0]}{"%05d" % int(_ls[1])}', headers=headers).text
        html = BeautifulSoup(html, 'html.parser')
        st.update('解析番号图片信息')
        divs = html.find_all('div', class_='col-xs-12 col-md-12')
        if not divs:
            QproDefaultConsole.print(divs)
            return None
        img = divs[0].find('img').get('src')
        imgs = [div.find('img').get('src') for div in divs[1:-1]]
        if img:
            title = html.find('h3').text
            raw_info['img'] = img
            raw_info['imgs'] = imgs
            st.update('翻译标题')
            raw_info['title'] = translate(title)
        else:
            QproDefaultConsole.print(QproErrorString, f'{designation} 未找到!')
            return
        if img.startswith('//'):
            img = f'http:{img}'
        from QuickStart_Rhy.ImageTools.ImagePreview import image_preview
        image_preview(img, qs_console_status=st)

    with QproDefaultConsole.status('查询番号信息') as st:
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

