from QuickStart_Rhy.NetTools import get_fileinfo


def backup_img(designation: str):
    """
    备份的封面获取方式

    :param designation: 番号
    :return: 封面url
    """
    if get_fileinfo(f"https://img2.javmost.cx/file_image/{designation.upper()}.jpg")[0]:
        return f"https://img2.javmost.cx/file_image/{designation.upper()}.jpg"
    elif get_fileinfo(
        f"https://img2.javmost.cx/file_image/{designation.upper()}-Uncensored-Leak.jpg"
    )[0]:
        return f"https://img2.javmost.cx/file_image/{designation.upper()}-Uncensored-Leak.jpg"
    return ""
