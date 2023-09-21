from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    """
    WHITE_LIST:
        "user_id" : {"type": "all/private/group","group":["group1_id","group2_id"]}
        注: type 拥有三种类型，分别为'all'、'private'、'group'。
            group项需在'all'与'group'类型时设置
        all: 接收私人信息以及群组消息,需设置group。
        private: 仅接收私人消息。
        group: 仅接收群组消息,需设置group。
    ENDPOINT: 端点 -> 控制机器人会将消息发送到哪里。
        "group_id": 群号
        "user_id": 用户号

        -------------ENDPOINT_SAMPLE-------------
        "ENDPOINT" : {
            'group_id': [518041028],
            'user_id': [1234567890]
        }
        会将消息发送至518041028群以及1234567890好友

        ------------WHITE_LIST_SAMPLE------------
        "WHITE_LIST" : {
            "1234567890": {"type": "all","group":['518041028']},
            "2236548876": {"type": "private"}
        }
        对于 “1234567890” 用户
        接收私人消息指令，接收用户在 “518041028” 群中的消息指令
        对于 “2236548876” 用户
        仅接收私人消息指令
    """
    # ---------------------- plugin_config ----------------------------

    baseConfig={
        # WHITE_LIST Must Be Set, Which Definds The Origin Of The Request
        # The id in the group must exist in the form of a string
        "WHITE_LIST" : { # Set Your List
            
        },
        # ENDPOINT Must Be Set, Which Definds The Response Goes Where
        "ENDPOINT" : { # Set Your Point
            
        },
        # BC_FRESH_TIME Is Optional, Default 20
        "BC_FRESH_TIME" : 20,
        # GAME_ID Is Optional, Default 1
        "GAME_ID" : 8,
        "BC_MESSAGE_TEMPLATE": "",
        # GZCTF Admin Username, Must Be Set
        "GZCTF_USER": "",
        # GZCTF Admin Password, Must Be Set
        "GZCTF_USER_PASS": "",
        # The Headers Of Post Request In Login View, Must Be Set
        "HEADERS":{},
        # The Base Url Of Your Gzctf Platform, Like "https://192.168.0.1/", Must Be Set
        "BASEURL": ""
    }

    TYPE_LIST = {
        "Normal" : "【公告更新】",
        "FirstBlood" : "---> 【一血】 <---",
        "SecondBlood" : "---> 【二血】 <---",
        "ThirdBlood" : "---> 【三血】 <---",
        "NewHint" : "【提示更新】",
        "NewChallenge" : "【上题目啦】"
    }

    HELP_LIST = [
        "help alias:帮助、帮助手册\n\
 - 查看指令手册\n",
        "open alias:打开播报\n\
 - 打开播报\n",
        "close alias:关闭播报\n\
 - 关闭播报\n"
 ]