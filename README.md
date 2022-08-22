# Jav Utils | JAV 工具箱

## 注意事项

1. 本项目中的翻译引擎依赖于[QuickStart_Rhy](https://github.com/Rhythmicc/qs)中配置的默认翻译引擎，初次使用`qs`会自动引导配置；如果你不想使用`qs`，可以自行修改main.py中的translate函数。
2. 终端内图片预览只支持系统配合[iTerm2](https://iterm2.com/)使用。
3. **请勿在墙内宣传本项目!**

## 安装

### 安装依赖

```sh
pip3 install -r requirements.txt
```

### 在`app.py`中设置数据源

默认使用`jav321`作为数据源，因此文件前两行是`from .source.jav321 ...`，如需切换成`busjav`则将`jav321`替换为`busjav`即可 (注意前面的`.source`不要删掉了)。

### [将此项目注册为全局命令](https://rhythmlian.cn/2020/02/14/QuickProject/#%E5%B0%86Commander%E5%BA%94%E7%94%A8%E6%B3%A8%E5%86%8C%E4%B8%BA%E5%85%A8%E5%B1%80%E5%91%BD%E4%BB%A4)

```sh
Qpro register-global # 注册全局命令，第一次注册请点击上方链接查阅文档
cd /usr/local/share/zsh/site-functions
Qpro gen-zsh-comp # 生成zsh自动补全脚本
# 以下操作仅支持Mac，并且需要配置fig: https://fig.io/
cd ~/.fig/autocomplete # 如果这个路径不存在则尝试下一条
# cd ~/.fig/user/autocomplete
Qpro gen-fig-script
```

## 调用方式

- 如果未注册为全局命令，则在本项目文件夹下执行:
  
  ```sh
  qrun cover
  ```

- 如果已经注册为全局命令，则在任意位置:

  ```sh
  jav cover
  ```

## 支持的子命令

| 子命令 | 调用方式                             | 描述                                         |
| ------ | ------------------------------------ | -------------------------------------------- |
| cover | jav cover | 遍历目录下的番号视频并为其自动下载封面 |
| info   | jav info <番号> | 查询番号信息+获取下载链接+保存视频信息 |
| web | jav web <番号> | 从浏览器查询番号信息 |

`info`命令保存的图像文件默认为`folder.<suffix>`，nfo文件默认为`<番号>.nfo`

## Demo

1. [点此预览视频](https://cos.rhythmlian.cn/ImgBed/dfec21722022947a677ead76b6979d40.mp4)
2. `jav info SSIS-464`

   nfo 文件内容:

   ![](https://cos.rhythmlian.cn/ImgBed/8666a497a636036147f586dddf25d5cf.png)

## 开发者

1. 为了开发Qpro Commander应用，你需要创建一个文件夹比如`$HOME/QproCommanderAPP`，并为`$PYTHONPATH`环境变量增加一条该文件夹的路径信息。
2. 增加其他自定义刮削方式，在`source`文件夹下新建一个`<站点名>.py`，结构如下:
  ```py
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
      # ! 此函数返回 {'img': '', 'imgs': '', 'title': ''}
  ```
