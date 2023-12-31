from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    # ---------------------- plugin_config ----------------------------
    # Get Sample From https://github.com/Birkenwald-Sec/GZCTF-QQBOT
    BASECONFIG={
        # WHITE_LIST Must Be Set, Which Definds The Origin Of The Request
        # The id in the group must exist in the form of a string
        "WHITE_LIST" : { # Set Your List
            
        },
        # ENDPOINT Must Be Set, Which Definds The Response Goes Where
        "ENDPOINT" : { # Set Your Point
            
        },
        # BASEURL Must Be Set, The Base Url Of Your Gzctf Platform, Like "https://192.168.0.1/"
        "BASEURL": "",
        # BC_FRESH_TIME Is Optional, Default 20
        "BC_FRESH_TIME" : 20,
        # GAMEMONITORED Is Optional, Default [], Which Represents Monitoring Of All Games Which Is Opening
        "GAMEMONITORED" : [],
        # BC_MESSAGE_TEMPLATE Is Optional, Default "类型：{type} 于 {game_title}\n内容： {content}\n时间： {month}-{day} {time}"
        "BC_MESSAGE_TEMPLATE": "",
        # GZCTF Admin Username, Optional
        "GZCTF_USER": "",
        # GZCTF Admin Password, Optional
        "GZCTF_USER_PASS": "",
        # TYPE_LIST Is Optional, Which Defined Title Of Type
        "TYPE_LIST": {
            
        }
    }