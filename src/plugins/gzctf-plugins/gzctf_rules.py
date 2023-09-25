import asyncio
from nonebot.rule import Rule
from nonebot.adapters.cqhttp import Event
from nonebot import get_driver

from .config import Config

WHITE_LIST:dict = Config.parse_obj(get_driver().config).BASECONFIG.get("WHITE_LIST")

async def checkIfGroup(event:Event):
    return event.json['message_type'] == "group"

async def checkBeginPoint(event:Event):
    global WHITE_LIST
    if not WHITE_LIST:
        return False
    session=event.get_session_id().split("_")
    [session.insert(0,i) for i in [None,'private']] if session.__len__() == 1 else session
    for user,check in WHITE_LIST.items():
        if session[2] != user:
            continue
        if check['type'] == 'private' and session[0] == 'private': return True
        if check['type'] == 'all' and (session[0] == 'private' or (session[0] == 'group' and (session[1] in check['group']))): return True
        if check['type'] == 'group' and (session[0] == 'group' and (session[1] in check['group'])): return True
    return False
