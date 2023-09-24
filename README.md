# GZCTF_BOT


一款适用于GZ::CTF平台可控制的QQ播报BOT，由于平台的API调用十分方便，使用BOT的可优化的功能点有很多。GZtime nb.jpg！！！

### 功能🧀

- Blood播报（First Blood、Second Blood、Third Blood）
- 题目上新播报
- 题目提示更新播报
- 赛事公告播报

### 部署过程 🚀

此服务使用 Nonebot2 + go-cqhttp 架构完成搭建，需要一点点python基础。

#### 搭建go-cqhttp 😊

首先前往 [go-cqhttp 下载页面](https://github.com/Mrs4s/go-cqhttp/releases) 下载并安装 **`go-cqhttp`** 最新版本

使用 go-cqhttp 进行初始化，选择如下

![微信截图_20230924124228](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/c4796e35-9592-4481-b1ef-4ad42c59c70e)

初始化后，打开同目录下的 `config.yml` 文件，配置好自己的登录令牌，密码可选择为空，然后使用扫码进行登录

![微信截图_20230924124324](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/375b00a7-78c3-45d3-90a6-d9759793eedc)

同时，在 `config.yml` 文件中找到 `ws-server` 设置项，进行如下设置

![微信截图_20230924124942](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/8a8aa999-845e-4c78-aaf1-dfdd67369ff2)

打开同目录下的 `device.json` 将 **`protocol`** 项更改为2（Android Watch协议）

![微信截图_20230924130854](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/ffce8a38-3bef-4efe-9351-9c12182aa8f3)

最后再次使用 `go-cqhttp` 指令，使用二维码即可登录自己的qq，并实现命令行接收qq信息

也可以直接使用 `go-cqhttp` 提供的API实现消息的发送与接收，详细请前往 [go-cqhttp 官方文档](https://docs.go-cqhttp.org/api/#%E5%9F%BA%E7%A1%80%E4%BC%A0%E8%BE%93)

#### 部署Nonebot2 😁

使用git拉取GZCTF-BOT项目

![微信截图_20230924133655](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/ba18028c-4ddc-47b6-abf2-c9ff10d3cb60)

使用python运行bot.py即可




