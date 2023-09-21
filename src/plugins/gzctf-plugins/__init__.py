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

config=Config.parse_obj(get_driver().config).baseConfig

getLogin()

if not checkConfig(config=config):
    print("Config Must Set All Items in [\"ENDPOINT\",\"WHITE_LIST\"]")
    exit()