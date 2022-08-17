# Jav Utils | JAV 工具箱

## 安装

### 安装依赖

```sh
pip3 install -r requirements.txt
```

### [将此项目注册为全局命令](https://rhythmlian.cn/2020/02/14/QuickProject/#%E5%B0%86Commander%E5%BA%94%E7%94%A8%E6%B3%A8%E5%86%8C%E4%B8%BA%E5%85%A8%E5%B1%80%E5%91%BD%E4%BB%A4)

```sh
Qpro register-global # 注册全局命令
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

`info`命令保存的图像文件默认为`folder.<suffix>`，nfo文件默认为`<番号>.nfo`

## Demo

1. `jav info SSIS-464`

   ![](https://cos.rhythmlian.cn/ImgBed/6aca0d8eff3d737190c22a5cf4fd5bfa.png)

   图片是后期人工打码，实际使用中可看清。

   nfo 文件内容:

   ![](https://cos.rhythmlian.cn/ImgBed/8666a497a636036147f586dddf25d5cf.png)

2. [点此预览视频](https://cos.rhythmlian.cn/ImgBed/dfec21722022947a677ead76b6979d40.mp4)

## 注意事项

1. 本项目中的翻译引擎依赖于[QuickStart_Rhy](https://github.com/Rhythmicc/qs)中配置的默认翻译引擎，初次使用`qs`会自动引导配置；如果你不想使用`qs`，可以自行修改main.py中的translate函数。
2. 终端内图片预览只支持系统配合[iTerm2](https://iterm2.com/)使用。
3. **请勿在墙内宣传本项目!**
