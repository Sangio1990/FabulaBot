import lightbulb

from db.utilsDB import UtilsDB
from secretsData.data import *

plugin = lightbulb.Plugin(name="Comandi Admin", description="Comandi disponibili solo agli Admin")
plugin.add_checks(lightbulb.checks.has_roles(chosen_region[ADMIN_ROLE]))
db = UtilsDB()

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
