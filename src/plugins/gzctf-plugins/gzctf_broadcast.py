from nonebot import on_command,get_driver,get_bot
from nonebot import require
from nonebot.rule import Rule,to_me
# from nonebot_plugin_apscheduler import scheduler
he = require("nonebot_plugin_apscheduler").scheduler
from .gzctf_tools import getNowNoticeList, parseTime, sendMessageTo,getGameMonitored, getNoticeById, getContestInfo
from .gzctf_rules import checkBeginPoint
from .config import Config

CONFIG = Config.parse_obj(get_driver().config)
BASECONFIG = CONFIG.BASECONFIG
SEND_ENABLED = False
NOWCONTESTINFO=getContestInfo()
GAMEMONITORED=getGameMonitored()
NOWNOTICELIST=getNowNoticeList(GAMEMONITORED)
ENDPOINT=BASECONFIG.get('ENDPOINT')
BC_FRESH_TIME = 20 if not BASECONFIG.get("BC_FRESH_TIME") else BASECONFIG.get("BC_FRESH_TIME")
BC_MESSAGE_TEMPLATE=BASECONFIG.get("BC_MESSAGE_TEMPLATE") if BASECONFIG.get("BC_MESSAGE_TEMPLATE")\
      else """类型：{type} 于 {game_title}\n内容： {content}\n时间： {month}-{day} {time}"""
try:
    TYPE_LIST = BASECONFIG["TYPE_LIST"]
except:
    TYPE_LIST = {
        "Normal" : "【公告更新】",
        "FirstBlood" : "-> 【一血】",
        "SecondBlood" : "-> 【二血】",
        "ThirdBlood" : "-> 【三血】",
        "NewHint" : "【提示更新】",
        "NewChallenge" : "【上题目啦】"
    }

rule=to_me() & checkBeginPoint

#! open 指令路由
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

#! close 指令路由
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

#! 查看当前所播报的比赛信息
check=on_command("check",aliases={"比赛信息,比赛"},rule=rule)
@check.handle()
async def check_handle(bot,event):
    global GAMEMONITORED
    GAMEMONITORED=getGameMonitored()
    status = "开" if SEND_ENABLED else "关"
    msg=f"处于监听中的比赛有(状态：{status}):\n"
    for gameInfo in GAMEMONITORED:
        gameTimeStart = parseTime(gameInfo['start'])
        gameTimeEnd = parseTime(gameInfo['end'])
        msg+=f"\t赛事名称: {gameInfo['title']}\n\t\t开始时间: {gameTimeStart[1]}-{gameTimeStart[2]} {gameTimeStart[3]}:{gameTimeStart[4]}:{gameTimeStart[5]}\
            \n\t\t结束时间: {gameTimeEnd[1]}-{gameTimeEnd[2]} {gameTimeEnd[3]}:{gameTimeEnd[4]}:{gameTimeEnd[5]}\n"
        
    try:
        await bot.send(event,msg)
    except:
        return

#! 定时任务，受控于SEND_ENABLED
@he.scheduled_job("interval", seconds=BC_FRESH_TIME)
async def drink_tea():
    global SEND_ENABLED, BC_MESSAGE_TEMPLATE, NOWNOTICELIST, GAMEMONITORED, NOWCONTESTINFO
    bot=get_bot()
    #! 播报
    if SEND_ENABLED:
        #! 检测比赛是否有变动，有则更改GAMEMONITORED
        tmpContestInfo=getContestInfo()
        if tmpContestInfo != NOWCONTESTINFO:
            GAMEMONITORED=getGameMonitored()
        #! 循环获取多个监听比赛的信息并进行处理
        for gameInfo in GAMEMONITORED:
            if (tmpnoticelist:=getNoticeById(f"{gameInfo['id']}")) != NOWNOTICELIST[f"{gameInfo['id']}"]:
                tmpList=[]
                for single_info in tmpnoticelist:
                    if single_info not in NOWNOTICELIST[f"{gameInfo['id']}"]:
                        tmpList.append([single_info['id'],single_info])
                tmpList.sort()
                for idInfoSet in tmpList:
                    single_info = idInfoSet[1]
                    megTime=parseTime(single_info['time'])
                    msgType=TYPE_LIST[single_info['type']] if TYPE_LIST.get(single_info['type']) else single_info['type']
                    msgContent=single_info['content']
                    msg:str=BC_MESSAGE_TEMPLATE.lstrip(' ').rstrip(' ')
                    msg=msg.format(year=megTime[0],month=megTime[1],day=megTime[2],hour=megTime[3],minute=megTime[4],\
                                secode=megTime[5],type=msgType,content=msgContent,game_title=gameInfo['title'],game_id=gameInfo['id'],\
                                time=f"{megTime[3]}:{megTime[4]}:{megTime[5]}")
                    for key,ids in ENDPOINT.items():
                        for id in ids:
                            await sendMessageTo(bot, key, id, msg)
                NOWNOTICELIST[f"{gameInfo['id']}"]=tmpnoticelist