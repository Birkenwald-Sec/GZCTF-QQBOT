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

conf=Config.parse_obj(get_driver().config).BASECONFIG

getLogin()

if not checkConfig(config=conf):
    print("Config Must Set All Items in [\"ENDPOINT\",\"WHITE_LIST\"]")
    exit()