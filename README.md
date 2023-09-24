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

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/c4796e35-9592-4481-b1ef-4ad42c59c70e)

初始化后，打开同目录下的 `config.yml` 文件，配置好自己的登录令牌，密码可选择为空，然后使用扫码进行登录

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/375b00a7-78c3-45d3-90a6-d9759793eedc)

同时，在 `config.yml` 文件中找到 `ws-server` 设置项，进行如下设置

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/8a8aa999-845e-4c78-aaf1-dfdd67369ff2)

打开同目录下的 `device.json` 将 **`protocol`** 项更改为2（Android Watch协议）

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/ffce8a38-3bef-4efe-9351-9c12182aa8f3)

最后再次使用 `go-cqhttp` 指令，使用二维码即可登录自己的qq，并实现命令行接收qq信息

也可以直接使用 `go-cqhttp` 提供的API实现消息的发送与接收，详细请前往 [go-cqhttp 官方文档](https://docs.go-cqhttp.org/api/#%E5%9F%BA%E7%A1%80%E4%BC%A0%E8%BE%93)

#### 部署Nonebot2 😁

使用git拉取GZCTF-BOT项目

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/ba18028c-4ddc-47b6-abf2-c9ff10d3cb60)

设置 GZCTF-BOT/src/plugin/gzctf-plugin/config.py 中的必选项

#### config.py 设置 🔧

- "WHITE_LIST": 规定指令监听消息的来源
  - "key": 可触发指令的用户的账号
  - "value"
    - "type": "private", "group", "all"
      - "private": 表示监听单个用户，设置此项则后续 `group` 项无效
      - "group": 该类型表示监听群组消息， 设置此项则必须设置后续的 `group` 项来指明被监听群的群号
      - "all": 该类型表示既监听私人信息又监听群组消息，设置此项则必须设置后续的 `group` 项
      - "注": 所监听的私人用户账号是上面所设置 "key" 字段
    - "group": 列表，其中添加被监听群的群号，需使用字符串格式 
``` python
# WHITE_LIST 标准示例
"WHITE_LIST" : {
            "1234567890": {"type": "all","group":['518041028']},
            "2236548876": {"type": "private"}
        }
```

- "ENDPOINT": 用来指明消息接收方
  - "group_id": 列表，指明接收群群号
  - "user_id": 列表，指明接收用户的账号

``` python
# ENDPOINT 标准示例
"ENDPOINT" : {
            'group_id': [518041028],
            'user_id': [1234567890]
        }
```

- "BC_FRESH_TIME": 播报刷新频率，可空，默认20秒一次

- "GAME_ID": GZCTF比赛id，可以从比赛URL中获得

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/bb5bfe8d-5248-46d7-a7ed-a30acb7839bb)

- "BC_MESSAGE_TEMPLATE": 播报消息模板
  - "{type}": 表示消息种类
  - "{time}": 表示消息发生时间
  - "{content}": 表示消息内容
  - "注": 可从 [CQ码](https://docs.go-cqhttp.org/cqcode/#%E8%BD%AC%E4%B9%89) 获取表情字符使用说明

``` python
# BC_MESSAGE_TEMPLATE 标准示例
"BC_MESSAGE_TEMPLATE": """\
{type} {time}
{content}"""
```

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/d1a6a7c1-3ac5-492c-9386-a5fb7688b95d)

- "GZCTF_USER": GZCTF平台管理员账户

- "GZCTF_USER_PASS": GZCTF平台管理员密码

- "HEADERS": 可从登录页面进行登录抓包获取

- "BASEURL": gzctf平台地址，例：https://www.gzctf.com/


