import os
import re
import pickle
from .sites.javdb import _info
from . import *


ACTOR_TEMPLATE = """\
<name>{name}</name>
<thumb>{photo}</thumb>
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
  <actor>
    {actors}
  </actor>
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
    return suffix in ['.mp4', '.avi', '.mkv', '.wmv', '.mpg', '.mpeg', '.mov', '.rm', '.ram', '.flv', '.swf', '.3gp', '.rmvb']

def get_video_id_info(filename):
    filename = os.path.splitext(filename)[0]
    designation = re.findall(r'([a-zA-Z]{2,5})-?(\d{2,5})', filename.upper())[0]
    return '-'.join(designation), filename

def generate_nfo(force: bool = False):
    if not os.path.exists(config.select('cache_path')) and not os.path.isdir(config.select('cache_path')):
        os.makedirs(config.select('cache_path'))
    QproDefaultStatus('扫描并生成NFO文件').start()
    for root, _, files in os.walk('./'):
        for file in files:
            if is_video_suffix(file):
                QproDefaultStatus('正在处理: [bold magenta]' + file + '[/]')
                designation, filename = get_video_id_info(file)
                nfo_path = os.path.join(root, f'{filename}.nfo')
                if os.path.exists(nfo_path) and not force:
                    continue
                cache_info = os.path.join(config.select('cache_path'), designation)
                if os.path.exists(cache_info):
                    with open(cache_info, 'rb') as f:
                        info = pickle.load(f)
                else:
                    info = _info(designation)
                    if info:
                        with open(cache_info, 'wb') as f:
                            pickle.dump(info, f)
                    else:
                        QproDefaultConsole.print(QproErrorString, f'番号 {designation} 查找失败！')
                        continue
                QproDefaultConsole.print(nfo_path)
                with open(nfo_path, 'w', encoding='utf-8') as f:
                    f.write(TEMPLATE.format(
                        title=info['title'],
                        studio=info['studio'],
                        year=info['date'][:4],
                        outline=info['plot'],
                        length=info['length'],
                        director=info['director'],
                        actors='\n    '.join([ACTOR_TEMPLATE.format(name=i['name'], photo=i['photo']) for i in info['actor']]),
                        tags='\n  '.join([f'<tag>{i}</tag>' for i in info['tag']]),
                        genre='\n  '.join([f'<genre>{i}</genre>' for i in info['tag']]),
                        designation=designation,
                        date=info['date'],
                        cover=info['img'],
                        website=info['url'],
                    ))
    QproDefaultStatus.stop()
