import random

import lightbulb

from db.utilsDB import UtilsDB
from utils.cmdsLogic import roll
from utils.utils import get_server_statistics, get_server_levels
from view.LevelUpView import LevelUpView
from view.pineappleview import PineappleView

plugin = lightbulb.Plugin(name="Comandi Utente", description="Comandi disponibili a tutti gli utenti")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


@plugin.command
@lightbulb.option("numero", "Il numero che scegli", type=int, choices=[1, 2, 3, 4, 5, 6])
@lightbulb.command("gambling", "Scegli 1 numero da 1 a 6 e vediamo se azzecchi il tiro di dado!")
@lightbulb.implements(lightbulb.SlashCommand)
async def gambling(ctx: lightbulb.SlashContext) -> None:
    num = random.randint(1, 6)
    if ctx.options.numero == num:
        await ctx.respond(f"Hai azzeccato, il dado ha fatto {num}")
    else:
        await ctx.respond(f"Mi dispiace, il dado ha fatto {num}!")


@plugin.command
@lightbulb.command("ping", "Controlla se il bot è vivo")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")


@plugin.command
@lightbulb.command("ping", "Controlla se il bot è vivo")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond("Pong from slash!")


@plugin.command
@lightbulb.option("taglia", "Qante facce ha il tuo dado?", type=int, required=True)
@lightbulb.option("quanti", "Quanti dadi vuoi tirare?", type=int, required=False)
@lightbulb.option("modificatore", "Quale modificatore vuoi aggiungere?", type=int, required=False)
@lightbulb.command("roll", "Tira i dadi!")
@lightbulb.implements(lightbulb.SlashCommand)
async def roll_command(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(roll(ctx.options.taglia, ctx.options.quanti, ctx.options.modificatore))


@plugin.command()
@lightbulb.command("pineapplepizza", "description", auto_defer=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def some_slash_command(ctx: lightbulb.SlashContext) -> None:
    view = PineappleView()  # Create the view

    await ctx.respond("Do you put pineapple on your pizza?", components=view)

    ctx.app.d.miru.start_view(view)

    # You can also wait until the view is stopped or times out
    await view.wait()

    if view.answer is not None:
        print(f"Received an answer! It is: {view.answer}")
    else:
        print("Did not receive an answer in time!")

@plugin.command
@lightbulb.command("testlevelup", "test nuovo level up")
@lightbulb.implements(lightbulb.SlashCommand)
async def print_character(ctx: lightbulb.SlashContext) -> None:
    view = LevelUpView()

    await ctx.respond("Pronto per fare aumentare di livello?", components=view)

    ctx.app.d.miru.start_view(view)

    await view.wait()

    if view.answer is not None:
        print(f"Received an answer! It is: {view.answer}")



@plugin.command
@lightbulb.command("statisticheserver", "Scopri cose sui pg del server")
@lightbulb.implements(lightbulb.SlashCommand)
async def statistics(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(get_server_statistics())


@plugin.command
@lightbulb.command("livellogiocatori", "Lista dei personaggi e relativi livelli")
@lightbulb.implements(lightbulb.SlashCommand)
async def level_statistics(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(get_server_levels())
