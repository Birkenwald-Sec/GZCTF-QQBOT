import requests
import json
import pytz
from datetime import datetime
from nonebot import get_driver
from nonebot.adapters import Bot
from .config import Config

CONFIG=Config.parse_obj(get_driver().config)
BASECONFIG = CONFIG.BASECONFIG
BASEURL=BASECONFIG['BASEURL'].rstrip('/')
HEADERS={"Content-Type": "application/json"}
LOGINDATA="{"+f'"userName": "{BASECONFIG["GZCTF_USER"]}", "password": "{BASECONFIG["GZCTF_USER_PASS"]}"'+"}"
WEBSESSION=requests.session()
UTC_TIMEZONE = pytz.timezone('UTC')
UTC_PLUS_8_TIMEZONE = pytz.timezone('Asia/Shanghai')

def getContestInfo():
    """
        *** 获取 gzctf 所有比赛详细信息 ***
    """
    global WEBSESSION, HEADERS
    API_CONTEST_URL = BASEURL+f'/api/game/'
    try:
        res = WEBSESSION.get(API_CONTEST_URL, headers=HEADERS)
    except:
        return []
    contestInfo = json.loads(res.text)
    return contestInfo

def checkConfig(config: dict):
    """
        *** 判断 BASECONFIG 是否成立 ***
    """
    return True if config.get("WHITE_LIST") and config.get("ENDPOINT") else False

def parseTime(strTime):
    """
        *** 解析通过 gzctf 平台获取的时间串 ***
    """
    global UTC_TIMEZONE, UTC_PLUS_8_TIMEZONE
    date=datetime.fromisoformat(strTime[:19])
    parsed_date_utc = UTC_TIMEZONE.localize(date)
    date=parsed_date_utc.astimezone(UTC_PLUS_8_TIMEZONE)
    # date=datetime.now()
    year=date.year
    month = ('0'+str(date.month)) if date.month < 10 else str(date.month)
    day = ('0'+str(date.day)) if date.day < 10 else str(date.day)
    hour = ('0'+str(date.hour)) if date.hour < 10 else str(date.hour)
    minute = ('0'+str(date.minute)) if date.minute < 10 else str(date.minute)
    second = ('0'+str(date.second)) if date.second < 10 else str(date.second)
    nowTime=(year,month,day,hour,minute,second)
    return nowTime

def getLogin():
    """
        *** 使用gzctf暴露的api进行登录 ***
    """
    global LOGINDATA, HEADERS, WEBSESSION, BASEURL
    API_LOGIN_URL = BASEURL+"/api/account/login"
    loginRespose=WEBSESSION.post(url=API_LOGIN_URL,data=LOGINDATA,headers=HEADERS)
    # return loginRespose.cookies if loginRespose.ok == True else None

def checkCookieExpired():
    """
        *** 判断会话的cookie有没有到期,如果到期则返回False,否则True ***
    """
    global WEBSESSION
    for cookie in WEBSESSION.cookies:
        if cookie is not None and cookie.name == "GZCTF_Token":
            expire = datetime.fromtimestamp(cookie.expires)
            nowTime = datetime.now()
            if nowTime > expire:
                return False
    return True

def getNoticeById(GAME_ID:str):
    """
        *** 获取gzctf某场比赛的notices消息 ***
    """
    global WEBSESSION, HEADERS, BASEURL
    API_NOTICE_URL = BASEURL+f"/api/game/{GAME_ID}/notices"
    # request = requests.session()
    try:
        res = WEBSESSION.get(API_NOTICE_URL, headers=HEADERS)
    except:
        return []
    allList = json.loads(res.text)
    return allList

def getChallengesById(GAME_ID:str):
    """
        *** 获取gzctf某场比赛中的所有题目, 需要admin权限 ***
    """
    global WEBSESSION, HEADERS, BASEURL
    API_CHALLENGE_URL = BASEURL+f'/api/edit/games/{GAME_ID}/challenges'
    if not checkCookieExpired():
        getLogin()
    try:
        challengeResponse=WEBSESSION.get(url=API_CHALLENGE_URL,headers=HEADERS)
    except:
        return []
    return json.loads(challengeResponse.text)

async def sendMessageTo(bot:Bot, type:str, id:str, message:str):
    """
        *** 直接利用 bot API 发送消息到 '某人/某群' ***
    """
    if type == "user_id" or type == "user":
        try:
            await bot.call_api('send_msg',user_id=int(id,10),message=message)
        except:
            return False
    elif type == "group_id" or type == "group":
        try:
            await bot.call_api('send_msg',group_id=int(id,10),message=message)
        except:
            return False
    return True

def getGameMonitored():
    """
        *** 获取被监视比赛的信息 ***
    """
    global CONFIG,BASECONFIG
    CONTESTINFOS=getContestInfo()
    GAMEMONITORED=BASECONFIG.get('GAMEMONITORED') if BASECONFIG.get('GAMEMONITORED') else []
    if GAMEMONITORED:
        GAMEMONITOREDTMP=[]
        for gameId in GAMEMONITORED:
            gameAllowed = [gameInfo for gameInfo in CONTESTINFOS if gameInfo.get("title") == gameId]
            for gameInfo in gameAllowed:
                GAMEMONITOREDTMP.append(gameInfo)
        GAMEMONITORED=GAMEMONITOREDTMP
    else:
        GAMEMONITORED = CONTESTINFOS
    return GAMEMONITORED

def getNowNoticeList(gamemonitored: list):
    """
        *** 获取被监视比赛的notice ***
    """
    NOWNOTICEDICT={}
    for gameInfo in gamemonitored:
        NOWNOTICEDICT[f"{gameInfo['id']}"]=getNoticeById(f"{gameInfo['id']}")
    return NOWNOTICEDICT