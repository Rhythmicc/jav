from .. import *

img_baseUrl = "https://javgg.net/jav/"
source_name = "javgg"
using_selenium = True


@cover_func_wrapper
def _cover(designation: str, driver=None):
    """
    下载多个封面

    :param designations: 番号列表
    :param set_covername: 设置封面图片名称
    """
    # ! 此函数返回番号的封面url即可，如果没有封面则 raise Exception("未找到封面")
    remote_url = config.select("remote_url")

    if not remote_url:
        raise Exception("未设置远程地址")

    driver_flag = True if driver else False

    from selenium import webdriver
    from selenium.webdriver.common.by import By

    if not driver_flag:
        from selenium import webdriver

        driver = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=webdriver.DesiredCapabilities.CHROME,
        )
    driver.get(f"{img_baseUrl}{designation.upper()}/")
    img = driver.find_element(By.CLASS_NAME, "cover").get_attribute("src")
    if not driver_flag:
        driver.quit()
    return img


@info_func_wrapper
def _info(designation: str, driver=None):
    """
    查询番号信息

    :param designation: 番号
    :return dict: {'img', 'imgs', 'title', 'plot', 'date'}
    """
    # ! 此函数返回 {'img': '', 'imgs': '', 'title': ''}
    remote_url = config.select("remote_url")

    if not remote_url:
        raise Exception("未设置远程地址")

    from selenium.webdriver.common.by import By

    driver_flag = True if driver else False

    with QproDefaultConsole.status("正在打开远程浏览器") as st:
        raw_info = {}
        if not driver_flag:
            from selenium import webdriver

            driver = webdriver.Remote(
                command_executor=remote_url,
                desired_capabilities=webdriver.DesiredCapabilities.CHROME,
            )
        st.update("正在打开网页")
        driver.get(f"{img_baseUrl}{designation.lower()}/")
        st.update("正在获取信息")
        raw_info["img"] = driver.find_element(By.CLASS_NAME, "cover").get_attribute(
            "src"
        )
        info = driver.find_element(By.ID, "cover")
        raw_info["imgs"] = [
            i.get_attribute("href") for i in info.find_elements(By.TAG_NAME, "a")
        ]
        raw_info["title"] = info.text.splitlines()[0]

        if not driver_flag:
            driver.quit()
        return raw_info


def _web(designation: str):
    """
    查询番号网页信息

    :param designation: 番号
    """
    from QuickStart_Rhy import open_url

    open_url([f"{img_baseUrl}/{designation.lower()}/"])
