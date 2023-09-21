import requests, json, pytz
from datetime import datetime
from nonebot import get_driver
from .config import Config

baseConfig = Config.parse_obj(get_driver().config).baseConfig
GAME_ID = 1 if not baseConfig.get("GAME_ID") else baseConfig.get("GAME_ID")
BASEURL=baseConfig['BASEURL'].rstrip('/')
API_NOTICE_URL = BASEURL+f"/api/game/{GAME_ID}/notices"
API_CHALLENGE_URL = BASEURL+f'/api/edit/games/{GAME_ID}/challenges'
API_LOGIN_URL = BASEURL+"/api/account/login"
HEADERS=baseConfig['HEADERS']
LOGINDATA="{"+f'"userName": "{baseConfig["GZCTF_USER"]}", "password": "{baseConfig["GZCTF_USER_PASS"]}"'+"}"
WEBSESSION=requests.session()
UTC_TIMEZONE = pytz.timezone('UTC')
UTC_PLUS_8_TIMEZONE = pytz.timezone('Asia/Shanghai')

def checkConfig(config: dict):
    return True if config.get("WHITE_LIST") and config.get("ENDPOINT") else False

def parseTime(strTime):
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
    nowTime=f"{hour}:{minute}:{second}"
    return nowTime

def getLogin():
    """
        *** 使用gzctf暴露的api进行登录 ***
    """
    global API_LOGIN_URL,LOGINDATA,HEADERS,WEBSESSION
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

def getNotice():
    """
        *** 获取gzctf某场比赛的notices消息 ***
    """
    global API_NOTICE_URL, WEBSESSION, HEADERS
    # request = requests.session()
    try:
        res = WEBSESSION.get(API_NOTICE_URL, headers=HEADERS)
    except:
        return []
    allList = json.loads(res.text)
    return allList

def getChallenges():
    """
        *** 获取gzctf某场比赛中的所有题目, 需要admin权限 ***
    """
    global WEBSESSION, API_CHALLENGE_URL, HEADERS
    if not checkCookieExpired():
        getLogin()
    try:
        challengeResponse=WEBSESSION.get(url=API_CHALLENGE_URL,headers=HEADERS)
    except:
        return []
    return json.loads(challengeResponse.text)

