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
cd ~/.fig/user/autocomplete
Qpro gen-fig-script
```

## 调用方式

- 如果未注册为全局命令，则在本项目文件夹下执行:
  
  ```sh
  qrun cover -designations <多个番号...>
  ```

- 如果已经注册为全局命令，则在任意位置:

  ```sh
  jav cover -designations <多个番号...>
  ```

## 支持的子命令

| 子命令 | 调用方式                             | 描述                                         |
| ------ | ------------------------------------ | -------------------------------------------- |
| cover  | jav cover -designations <多个番号..> | 下载多个番号的封面图片                       |
| info   | jav info <番号>                      | 查询番号信息                                 |
| dl     | jav dl <番号>                        | 查询番号信息、获取复制下载链接并打开迅雷下载 |

## Demo

1. `jav dl SSIS-406`

   ![](https://cos.rhythmlian.cn/ImgBed/14676959edb211a0441bef3ae8593e65.png)

   图片左侧是后期人工打码，实际使用中可看清。

## 注意事项

1. 本项目中的翻译引擎依赖于[QuickStart_Rhy](https://github.com/Rhythmicc/qs)中配置的默认翻译引擎，初次使用`qs`会自动引导配置。
2. 终端内图片预览只支持系统配合[iTerm2](https://iterm2.com/)使用。