from nonebot import on_command,get_driver,get_bot
from nonebot.adapters.cqhttp import Bot,MessageEvent
from nonebot.rule import to_me,Rule
from .gzctf_rules import checkBeginPoint
from .config import Config

HELP_LIST = Config.parse_obj(get_driver().config).HELP_LIST

rule=to_me() & checkBeginPoint

help=on_command("help",aliases={"帮助手册","帮助"},rule=rule)

@help.handle()
async def help_handle(bot:Bot,event:MessageEvent):
    global HELP_LIST
    strHelp=''.join(HELP_LIST)
    try:
        await help.finish(strHelp)
    except:
        print("可能被封控了，无法发送群消息")