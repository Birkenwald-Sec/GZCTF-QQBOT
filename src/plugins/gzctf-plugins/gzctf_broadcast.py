from nonebot import on_command,get_driver,get_bot
from nonebot import require
from nonebot.rule import Rule,to_me
# from nonebot_plugin_apscheduler import scheduler
he = require("nonebot_plugin_apscheduler").scheduler
from .gzctf_tools import getNotice, parseTime, getChallenges
from .gzctf_rules import checkBeginPoint
from .config import Config

config = Config.parse_obj(get_driver().config)
baseConfig = config.baseConfig

SEND_ENABLED = False
BC_FRESH_TIME = 20 if not baseConfig.get("BC_FRESH_TIME") else baseConfig.get("BC_FRESH_TIME")
try:
    TYPE_LIST = config.TYPE_LIST
except:
    TYPE_LIST = {}
ENDPOINT=baseConfig.get('ENDPOINT')
NowNoticeList=getNotice()
NowChallengeList=getChallenges()

rule=to_me() & checkBeginPoint

# open 指令路由
open=on_command("open",aliases={"打开播报"},rule=rule)
@open.handle()
async def open_handle(bot,event):
    global SEND_ENABLED
    try:
        if not SEND_ENABLED:
            SEND_ENABLED = True
            await bot.send(event,"播报已经开启")
        else:
            await bot.send(event,"播报本来就开启着呢")
    except:
        print("可能被封控了，无法发送群消息")

# close 指令路由
clsoe=on_command("close",aliases={"关闭播报"},rule=rule)
@clsoe.handle()
async def close_handle(bot,event):
    global SEND_ENABLED
    try:
        if not SEND_ENABLED:
            await bot.send(event,"播报本来就关闭着呢")
        else:
            SEND_ENABLED = False
            await bot.send(event,"播报已经关闭")
    except:
        print("可能被封控了，无法发送群消息")

# 定时任务，受控于SEND_ENABLED
@he.scheduled_job("interval", seconds=BC_FRESH_TIME)
async def drink_tea():
    global SEND_ENABLED, NowNoticeList, NowChallengeList
    bot=get_bot()
    # 更新挑战
    tmpchallengelist = getChallenges()
    # 播报
    if SEND_ENABLED and (tmpnoticelist:=getNotice()) != NowNoticeList:
        tmpList=[]
        for single_info in tmpnoticelist:
            if single_info not in NowNoticeList:
                tmpList.append([single_info['id'],single_info])
        tmpList.sort()
        for idInfoSet in tmpList:
            single_info = idInfoSet[1]
            print(single_info)
            megTime=parseTime(single_info['time'])
            msgType=TYPE_LIST[single_info['type']] if TYPE_LIST.get(single_info['type']) else single_info['type']
            msgContent=single_info['content']
            msg:str=baseConfig['BC_MESSAGE_TEMPLATE'].lstrip(" ").rstrip(' ')
            msg=msg.format(time=megTime,type=msgType,content=msgContent)
            for key,ids in ENDPOINT.items():
                for id in ids:
                    try:
                        if key == "user_id" or key == "user":
                            await bot.call_api('send_msg',user_id=id,message=msg)
                        elif key == "group_id" or key == "group":
                            await bot.call_api('send_msg',group_id=id,message=msg)
                    except:
                        print("可能被封控了，无法发送群消息")
        NowNoticeList=tmpnoticelist