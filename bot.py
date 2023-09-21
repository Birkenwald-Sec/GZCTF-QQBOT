import nonebot
from nonebot.adapters.cqhttp import Adapter

nonebot.init()
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})


driver = nonebot.get_driver()
driver.register_adapter(Adapter)


nonebot.load_builtin_plugins("echo")  # 内置插件
# nonebot.load_plugin("thirdparty_plugin")  # 第三方插件
nonebot.load_plugins("src/plugins")  # 本地插件


if __name__ == "__main__":
    nonebot.run()