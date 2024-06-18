import lightbulb

from db.utilsDB import UtilsDB
from secretsData.data import *

plugin = lightbulb.Plugin(name="Comandi Sessioni", description="Comandi disponibili solo ai Master")
plugin.add_checks(lightbulb.checks.has_roles(chosen_region[MASTER_ROLE], chosen_region[ADMIN_ROLE], mode=any))
db = UtilsDB()


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


@plugin.command
@lightbulb.option("prova", "prova", type=str)
@lightbulb.command("prova", "prova")
@lightbulb.implements(lightbulb.SlashCommand)
async def prova(ctx: lightbulb.SlashContext) -> None:
    print(ctx.options.prova)
    await ctx.respond(ctx.options.prova)
