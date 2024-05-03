import lightbulb

from db.utilsDB import UtilsDB
from secretsData.data import *
from utils.utils import clear_id_from_mention

plugin = lightbulb.Plugin(name="Comandi Admin", description="Comandi disponibili solo agli Admin")
plugin.add_checks(lightbulb.checks.has_roles(chosen_region[ADMIN_ROLE]))
db = UtilsDB()


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


@plugin.command
@lightbulb.option("pv", "Che valore di pv vuoi assegnargli?", type=int, required=True)
@lightbulb.option("menzione", "Menziona il giocatore a cui assegnare l'oggetto", type=str, required=True)
@lightbulb.command("assegnapv", "Assegna Pv ad un personaggio!")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_pv(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.set_pv(ctx.options.pv)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("mp", "Che valore di pm vuoi assegnargli?", type=int, required=True)
@lightbulb.option("menzione", "Menziona il giocatore a cui assegnare l'oggetto", type=str, required=True)
@lightbulb.command("assegnapm", "Assegna pm ad un personaggio!")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_pv(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.set_mp(ctx.options.mp)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)
