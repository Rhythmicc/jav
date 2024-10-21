# Jav Utils | JAV 工具箱

## 注意事项

1. 翻译引擎
   1. 默认依赖于[QuickStart_Rhy](https://github.com/Rhythmicc/qs)（简称 qs）中配置的默认翻译引擎，初次使用`qs`会自动引导配置，支持AI翻译、[DeepLX](https://github.com/OwO-Network/DeepLX)（免费的 DeepL）等；
   2. 如果不想使用`qs`，可以自行修改 main.py 中的 translate 函数。
2. 终端内图片预览只支持  系统配合[iTerm2](https://iterm2.com/)使用。
3. **请勿在墙内宣传本项目!**

## 安装

```sh
pip3 install git+https://github.com/Rhythmicc/jav.git -U
```

支持迅雷下载：

1. 先在服务器上跑个迅雷的 Docker
   ```yaml
   services:
     xunlei:
       image: cnk3x/xunlei:latest
       privileged: true
       container_name: xunlei
       hostname: mynas
       network_mode: bridge
       ports:
         - <port>:2345
       volumes:
         - ./data:/xunlei/data
         - /path/to/download:/xunlei/downloads
         - ./root:/xunlei/downloads/ROOT
       restart: unless-stopped
   ```
2. 然后在`~/.jav/config.json`中增加配置
   ```json
   {
     "downloader": "xunlei url"
   }
   ```

## 支持的子命令

| 子命令 | 调用方式          | 描述                           |
| ------ | ----------------- | ------------------------------ |
| info   | `jav info <番号>` | 查询番号信息+迅雷下载/存心愿单 |
| web    | `jav web <番号>`  | 从浏览器查询番号信息           |
| rank   | `jav rank`        | 查询片商的近期榜单             |
| wish   | `jav wish`        | 心愿单查看                     |
| nfo    | `jav nfo`         | 刮削媒体库所有视频             |
| update | `jav update`      | 更新 jav                       |

初次运行`jav`会自动引导相关配置。

## Demo

1. [点此预览视频](https://cos.rhythmlian.cn/ImgBed/dfec21722022947a677ead76b6979d40.mp4)
2. `jav info SSIS-464` 查询番号信息+获取下载链接
3. 通过`jav rank`查看片商近期榜单，可在预览后选择将其添加至心愿单；（心愿单中的内容仅会在选择下载后提示删除）。
4. 使用`jav nfo`扫描所有视频文件，自动刮削生成 nfo 文件，并下载封面图片（poster.jpg）和花絮图片（extrafanart/extrafanart-\<id>.jpg）。

## 开发者

1. fork 本项目。

2. 增加其他自定义刮削方式，在`site`文件夹下新建一个`<站点名>.py`，结构如下:

   ```python
   from .. import *
   
   source_name = '' # 站点名


   @cover_func_wrapper
   def _cover(designation: str):
       """
       下载多个封面

       :param designations: 番号列表
       :param set_covername: 设置封面图片名称
       """
       # ! 此函数返回番号的封面url即可，如果没有封面则 raise Exception("未找到封面")

   @info_func_wrapper
   def _info(designation: str) -> dict:
       """
       查询番号信息

       :param designation: 番号
       :return dict: {'img', 'imgs', 'title', 'plot', 'date'}
       """
       # ! 此函数返回 {
       # !    'img': '封面',
       # !    'imgs': ['花絮'],
       # !    'title': ''，
       # !    'length': '时长（分钟）',
       # !    'director': '导演',
       # !    'studio': '片商',
       # !    'rate': '评分',
       # !    'tag': '分类',
       # !    'actor': [{'name': '', 'photo': '头像链接'}],
       # !    'magnets': [{'id': '1~n', 'name': '文件名', 'meta': '空间', 'date': '发布日期', 'url': '磁力链'}]
       # ! }，（'plot' 和 'date' 会自动生成。）
   ```

3. 自行安装测试：`pip3 install git+https://<你的仓库地址>/jav.git -U`。
4. 测试通过后提交 PR。
