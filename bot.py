import nonebot
from nonebot.adapters.cqhttp import Adapter



nonebot.init()
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})

driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run()