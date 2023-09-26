from nonebot import on_command, get_driver, get_bot
# from nonebot.adapters.cqhttp import Bot,MessageEvent
from nonebot.rule import to_me,Rule
from .gzctf_rules import checkBeginPoint
from .config import Config

HELP_LIST = "指令示例：@Bot /open\n\
\t/open => '打开/打开播报'\n\t <---- 打开赛事播报功能 ---->\n\
\t/close => '关闭/关闭播报'\n\t <---- 关闭赛事播报功能 ---->\n\
\t/check => '查看/查看赛事'\n\t <---- 检测监控赛事状态 ---->\n\
\t/help => '帮助/帮助手册'\n\t <---- 查看指令手册 ---->\n\
注：群聊使用指令需艾特机器人后加指令才可\n"



rule=to_me() & checkBeginPoint

help=on_command("help",aliases={"帮助手册","帮助"},rule=rule)

@help.handle()
async def help_handle(bot,event):
    global HELP_LIST
    # strHelp=''.join(HELP_LIST)
    try:
        await help.finish(HELP_LIST)
    except:
        print("可能被封控了，无法发送群消息")