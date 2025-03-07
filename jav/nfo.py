import os
import re
import pickle
from .sites.javdb import _info
from . import *


ACTOR_TEMPLATE = """\
<actor>
    <name>{name}</name>
    <thumb>{photo}</thumb>
  </actor>
"""

TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8" ?>
<movie>
  <title><![CDATA[{title}]]></title>
  <originaltitle><![CDATA[{title}]]></originaltitle>
  <sorttitle><![CDATA[{title}]]></sorttitle>
  <customrating>JP-18+</customrating>
  <mpaa>JP-18+</mpaa>
  <set></set>
  <studio>{studio}</studio>
  <year>{year}</year>
  <outline><![CDATA[{outline}]]></outline>
  <plot><![CDATA[{outline}]]></plot>
  <runtime>{length}</runtime>
  <director>{director}</director>
  <poster>poster.jpg</poster>  
  {actors}
  <maker>{studio}</maker>
  <label></label>
  {tags}
  {genre}
  <num>{designation}</num>
  <premiered>{date}</premiered>
  <releasedate>{date}</releasedate>
  <release>{date}</release>
  <cover>{cover}</cover>
  <website>{website}</website>
</movie>
"""


def is_video_suffix(filepath):
    suffix = os.path.splitext(filepath)[1]
    return suffix in [
        ".mp4",
        ".avi",
        ".mkv",
        ".wmv",
        ".mpg",
        ".mpeg",
        ".mov",
        ".rm",
        ".ram",
        ".flv",
        ".swf",
        ".3gp",
        ".rmvb",
    ]


def get_video_id_info(filename):
    filename = os.path.splitext(filename)[0]
    designation = re.findall(
        r"([a-zA-Z]{2,5})-?(\d{2,5})", filename.split("@")[-1].upper()
    )[0]
    return "-".join(designation), filename


def get_info(designation):
    cache_info = os.path.join(config.select("cache_path"), designation)
    if os.path.exists(cache_info):
        with open(cache_info, "rb") as f:
            info = pickle.load(f)
    else:
        info, _ = _info(designation)
        if info:
            with open(cache_info, "wb") as f:
                pickle.dump(info, f)
        else:
            QproDefaultConsole.print(QproErrorString, f"番号 {designation} 查找失败！")
            return None
    return info


def ftp_scan(ftp, path):
    for root, _, files in ftp.walk(path):
        for file in files:
            if not is_video_suffix(file):
                continue
            try:
                designation, filename = get_video_id_info(file)
            except:
                QproDefaultConsole.print(QproErrorString, f"文件名格式错误: {file}")
                from . import _ask
                
                if _ask({
                    'type': 'confirm',
                    'message': '是否删除此文件?',
                    'default': True
                }):
                    ftp.remove(os.path.join(root, file))
            yield root, designation, file, filename


def scan_path(movie_path):
    """
    iterate all video files in movie_path
    """
    if ssh := make_ssh_connect(movie_path):
        _, o, e = ssh.exec_command('jav nfo')
        QproDefaultConsole.print(QproInfoString, "刮削任务已提交")
        QproDefaultConsole.print(QproInfoString, o.read().decode("utf-8"))
        return iter(())
    else:
        return ftp_scan(os, movie_path["path"])


def generate_nfo(force: bool = False):
    if not os.path.exists(config.select("cache_path")) and not os.path.isdir(
        config.select("cache_path")
    ):
        os.makedirs(config.select("cache_path"))
    for root, designation, file, filename in scan_path(config.select("movie_path")):
        nfo_path = os.path.join(root, f"{filename}.nfo")
        extrafanart_path = os.path.join(root, "extrafanart")
        poster_path = os.path.join(root, "poster.jpg")

        if not os.path.exists(nfo_path) or force:
            QproDefaultConsole.print(
                QproInfoString, "处理: [bold magenta]" + file + "[/]"
            )
            if not (info := get_info(designation)):
                continue
            with open(nfo_path, "w", encoding="utf-8") as f:
                f.write(
                    TEMPLATE.format(
                        title=info["title"],
                        studio=info["studio"] if "studio" in info else "未知",
                        year=info["date"][:4],
                        outline=info["plot"] if "plot" in info else info["title"],
                        length=info["length"],
                        director=info["director"] if "director" in info else "未知",
                        actors="  ".join(
                            [
                                ACTOR_TEMPLATE.format(name=i["name"], photo=i["photo"])
                                for i in info["actor"]
                            ]
                        ),
                        tags="\n  ".join(
                            [
                                f"<tag>{i.strip()}</tag>"
                                for i in info["tag"].strip().split(",")
                            ]
                        ),
                        genre="\n  ".join(
                            [
                                f"<genre>{i.strip()}</genre>"
                                for i in info["tag"].strip().split(",")
                            ]
                        ),
                        designation=designation,
                        date=info["date"],
                        cover=info["img"],
                        website=info["url"],
                    )
                )

        if (
            (
                not os.path.exists(extrafanart_path)
                and not os.path.isdir(extrafanart_path)
            )
            or not os.path.exists(poster_path)
            or force
        ):
            if not (info := get_info(designation)):
                continue
            if not os.path.exists(extrafanart_path) and not os.path.isdir(extrafanart_path):
                os.mkdir(extrafanart_path)
            from QuickStart_Rhy.NetTools.MultiSingleDL import multi_single_dl

            name_map = {
                info["img"]: os.path.join(root, "poster"),
            }
            name_map.update(
                {
                    i: os.path.join(extrafanart_path, f"extrafanart-{index + 1}")
                    for index, i in enumerate(info["imgs"])
                }
            )
            multi_single_dl([info["img"]] + info["imgs"], name_map=name_map)
