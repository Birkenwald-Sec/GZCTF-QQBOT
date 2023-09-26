from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from .config import Config
from . import gzctf_broadcast, gzctf_help
from .gzctf_tools import checkConfig, getLogin

__plugin_meta = PluginMetadata(
    name="mybooot",
    description="",
    usage="",
    config=Config,
)

BASECONFIG=Config.parse_obj(get_driver().config).BASECONFIG

if BASECONFIG.get("GZCTF_USER") != "" and BASECONFIG.get("GZCTF_USER_PASS") != "":
    getLogin()

if not checkConfig(config=BASECONFIG):
    print("Config Must Set All Items in [\"ENDPOINT\",\"WHITE_LIST\"]")
    exit()