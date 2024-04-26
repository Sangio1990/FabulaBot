import random

import lightbulb

u_plugin = lightbulb.Plugin(name="Comandi Utente", description="Comandi disponibili a tutti gli utenti")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(u_plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(u_plugin)


@u_plugin.command
@lightbulb.option("numero", "Il numero che scegli", type=int, choices=[1, 2, 3, 4, 5, 6])
@lightbulb.command("gambling", "Scegli 1 numero da 1 a 6 e vediamo se azzecchi il tiro di dado!")
@lightbulb.implements(lightbulb.SlashCommand)
async def gambling(ctx: lightbulb.SlashContext) -> None:
    num = random.randint(1, 6)
    if ctx.options.numero == num:
        await ctx.respond(f"Hai azzeccato, il dado ha fatto {num}")
    else:
        await ctx.respond(f"Mi dispiace, il dado ha fatto {num}!")


@u_plugin.command
@lightbulb.command("ping", "Controlla se il bot è vivo")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")


@u_plugin.command
@lightbulb.command("ping", "Controlla se il bot è vivo")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond("Pong from slash!")

