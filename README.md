# Jav Cover Downloader | JAV 封面下载

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
```

## 使用

- 如果未注册为全局命令，则在本项目文件夹下执行:
  
  ```sh
  qrun down -designations <多个番号...>
  ```

- 如果已经注册为全局命令，则在任意位置:

  ```sh
  javCoverDL down -designations <多个番号...>
  ```
