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


@plugin.command
@lightbulb.option("ip", "Che valore di ip vuoi assegnargli?", type=int, required=True)
@lightbulb.option("menzione", "Menziona il giocatore a cui assegnare l'oggetto", type=str, required=True)
@lightbulb.command("assegnaip", "Assegna ip ad un personaggio!")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_pv(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)
    char = db.load_character(mentioned_id)
    result = char.set_ip(ctx.options.ip)
    db.save_character(char, mentioned_id)
    await ctx.respond(result)


@plugin.command
@lightbulb.command("backup", "Forza il backup del database!")
@lightbulb.implements(lightbulb.SlashCommand)
async def backup(ctx: lightbulb.SlashContext) -> None:
    db.backup_db()
    await ctx.respond("Backup effettuato!")

@plugin.command
@lightbulb.option("nomepg", "Scrivi il nome del pg da cancellare")
@lightbulb.command("eliminagiocatore", "Elimina la scheda di un giocatore")
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_character(ctx: lightbulb.SlashContext) -> None:
    db.delete_character_with_char_name(ctx.options.nomepg)
    await ctx.respond("Il personaggio è stato eliminato con successo!")