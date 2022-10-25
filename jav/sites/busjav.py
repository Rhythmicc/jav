from .. import *

img_baseUrl = "https://www.busjav.fun"
source_name = "busjav"


@cover_func_wrapper
def _cover(designation: str):
    """
    下载多个封面

    :param designations: 番号列表
    :param set_covername: 设置封面图片名称
    """
    # ! 此函数返回番号的封面url即可，如果没有封面则 raise Exception("未找到封面")
    headers["Referer"] = img_baseUrl
    html = requests.get(f"{img_baseUrl}/{designation.upper()}/", headers=headers).text
    img = re.findall('<a.*?bigImage.*?src="(.*?)"', html)
    if img:
        img = img_baseUrl + img[0]
    else:
        QproDefaultConsole.print(QproErrorString, f"{designation} 未找到!")
        raise Exception("未找到封面")
    if img == "${element.cover}":
        QproDefaultConsole.print(QproErrorString, f"{designation} 未找到!")
        raise Exception("未找到封面")
    if img.startswith("//"):
        img = f"http:{img}"
    return img


@info_func_wrapper
def _info(designation: str):
    """
    查询番号信息

    :param designation: 番号
    :return dict: {'img', 'imgs', 'title', 'plot', 'date'}
    """
    # ! 此函数返回 {'img': '', 'imgs': '', 'title': ''}
    with QproDefaultConsole.status("查询番号信息") as st:
        raw_info = {}
        raw_info["designation"] = designation
        headers["Referer"] = img_baseUrl
        html = requests.get(
            f"{img_baseUrl}/{designation.upper()}/", headers=headers
        ).text
        st.update("解析番号图片信息")
        img = re.findall('<a.*?bigImage.*?src="(.*?)".*?title="(.*?)"', html)
        imgs = re.findall('<a.*?sample-box.*?href="(.*?)"', html)
        if img == "${element.cover}":
            return None
        if img.startswith("//"):
            img = f"http:{img}"
        if img:
            img, title = img[0]
            img = img_baseUrl + img
            raw_info["img"] = img
            raw_info["imgs"] = [
                img_baseUrl + i if not i.startswith("http") else i for i in imgs if i
            ]
            raw_info["imgs"] = [i.strip() for i in raw_info["imgs"]]
            st.update("翻译标题")
            raw_info["title"] = translate(title)
        else:
            return
    return raw_info


def _web(designation: str):
    """
    查询番号网页信息

    :param designation: 番号
    """
    from QuickStart_Rhy import open_url

    open_url([f"{img_baseUrl}/{designation.upper()}/"])
