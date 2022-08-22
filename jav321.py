from . import *

img_baseUrl = 'https://www.jav321.com/video'
source_name = 'jav321'


@cover_func_wrapper
def _cover(designation: str):
    """
    下载多个封面

    :param designations: 番号列表
    :param set_covername: 设置封面图片名称
    """
    # ! 此函数返回番号的封面url即可，如果没有封面则 raise Exception("未找到封面")
    from bs4 import BeautifulSoup
    headers['Referer'] = img_baseUrl

    _ls = designation.lower().split('-')
    html = requests.get(f'{img_baseUrl}/{_ls[0]}{"%05d" % int(_ls[1])}', headers=headers).text
    html = BeautifulSoup(html, 'lxml')
    img = html.find_all('div', class_='col-xs-12 col-md-12')[0].find('img').get('src')
    
    if not img:
        QproDefaultConsole.print(QproErrorString, f'{designation} 未找到!')
        raise Exception("未找到封面")
    if not img.startswith('http') and not img.startswith('//'):
        img = img_baseUrl + img[0]
    if img.startswith('//'):
        img = f'http:{img}'
    return img


@info_func_wrapper
def _info(designation: str) -> dict:
    """
    查询番号信息

    :param designation: 番号
    :return dict: {'img', 'imgs', 'title', 'plot', 'date'}
    """
    # ! 此函数返回 {'img': '', 'imgs': '', 'title': ''}
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
            return
        if img.startswith('//'):
            img = f'http:{img}'
        from QuickStart_Rhy.ImageTools.ImagePreview import image_preview
        image_preview(img, qs_console_status=st)
    return raw_info


def _web(designation: str):
    """
    查询番号网页信息
    
    :param designation: 番号
    """
    from QuickStart_Rhy import open_url
    _ls = designation.lower().split('-')
    open_url([f'{img_baseUrl}/{_ls[0]}{"%05d" % int(_ls[1])}'])
