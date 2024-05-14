import random

import lightbulb

from utils.cmdsLogic import roll

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
