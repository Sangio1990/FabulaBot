import lightbulb

from classes.item import Item
from secretsData.data import *
from classes.character import check_doable, Character
from db.utilsDB import UtilsDB
from utils.cmdsLogic import multidice_roll
from utils.utils import bool_ita, clear_id_from_mention, is_item_sellable
from view.sellToPlayerView import SellToPlayerView

plugin = lightbulb.Plugin(name="Comandi Giocatore", description="Comandi disponibili solo per i giocatori")
plugin.add_checks(lightbulb.checks.has_roles(chosen_region[PLAYER_ROLE], chosen_region[ADMIN_ROLE], mode=any))
db = UtilsDB()


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


@plugin.command
@lightbulb.option("nome", "Come si chiama il tuo personaggio?", required=True)
@lightbulb.option("destrezza", "che taglia di dado ha su Destrezza?", type=int, required=True,
                  choices=new_char_dice_values)
@lightbulb.option("vigore", "Che taglia di dado ha su Vigore?", type=int, required=True, choices=new_char_dice_values)
@lightbulb.option("intuito", "Che taglia di dado ha su Intuito?", type=int, required=True, choices=new_char_dice_values)
@lightbulb.option("volonta", "Che taglia di dado ha su Volontà?", type=int, required=True, choices=new_char_dice_values)
@lightbulb.command("nuovopg", "Crea il tuo personaggio sul bot!")
@lightbulb.implements(lightbulb.SlashCommand)
async def create(ctx: lightbulb.SlashContext) -> None:
    if db.check_if_id_exists(ctx.user.id):
        await ctx.respond("Hai già un personaggio!")
    else:
        result = check_doable(ctx.options)
        if isinstance(result, str):
            await ctx.respond(result)
        else:
            db.save_character(result, ctx.user.id, new=True)
            await ctx.respond("Il personaggio è stato creato con successo!")


@plugin.command
@lightbulb.command("datipg", "Vedi i dati del tuo personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def print_character(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(db.load_character(ctx.user.id))


@plugin.command
@lightbulb.option("sicuro", "Sicuro di aver scelto la classe giusta?", choices=BOOL_ITA, type=str, required=True)
@lightbulb.option("classe", "In che classe vuoi acquistare un livello?", choices=CLASSES, type=str, required=True)
@lightbulb.command("levelup",
                   "Acquista un livello nella tua classe! ATTENZIONE: UNA VOLTA LIVELLATO NON SI TORNA INDIETRO!")
@lightbulb.implements(lightbulb.SlashCommand)
async def buy_level(ctx: lightbulb.SlashContext) -> None:
    if bool_ita(ctx.options.sicuro):
        char = db.load_character(ctx.user.id)
        result = char.level_up(ctx.options.classe)
        if result[1]:
            db.save_character(char, ctx.user.id)
            await ctx.respond(result[0])
        else:
            await ctx.respond(result[0])
    else:
        await ctx.respond("Pensaci pure con calma, io non mi muovo ^^")


@plugin.command
@lightbulb.option("sicuro", "SEI SICURO DI VOLER ELIMINARE IL TUO PERSONAGGIO?", choices=BOOL_ITA, type=str,
                  required=True)
@lightbulb.command("cancellapg", "Tempo di dire addio al tuo personaggio?")
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_character(ctx: lightbulb.SlashContext) -> None:
    if bool_ita(ctx.options.sicuro):
        db.delete_character(ctx.user.id)
        await ctx.respond("Il personaggio è stato eliminato con successo!")
    else:
        await ctx.respond("Troppo legato al tuo personaggio?\n" +
                          "Ti capisco!")


@plugin.command
@lightbulb.option("forza", "Che forza ha il tuo legame?", type=int, required=True, choices=[1, 2, 3])
@lightbulb.option("descrizione", "Che sentimenti provi verso il tuo legame?", type=str, required=True)
@lightbulb.option("nome", "Con chi/cosa fai il tuo legame?", type=str, required=True)
@lightbulb.command("legame", "Crea un legame con qualcuno di speciale!")
@lightbulb.implements(lightbulb.SlashCommand)
async def create_bond(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.bond(ctx.options.nome, ctx.options.descrizione, ctx.options.forza)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("nome", "Con chi/cosa vuoi cancellare il legame?", type=str, required=True)
@lightbulb.command("cancellalegame", "Cancella un legame con qualcuno di speciale!")
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_bond(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.delete_bond(ctx.options.nome)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.command("usafabula", "Usa un Punto Fabula")
@lightbulb.implements(lightbulb.SlashCommand)
async def use_fabula(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.remove_fabula(1)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("bonus", "Dimmi cosa garantisce la tua classe", required=True, choices=["PV", "PM", "PI"], type=str)
@lightbulb.command("bonusclasse", "Aggiungi il bonus di classe al tuo personaggio")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_bonus(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.add_bonus(ctx.options.bonus)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("prezzo", "Quanti zenit costa?", type=int, required=True)
@lightbulb.option("descrizione", "Descrizione dell'oggetto", type=str, required=False)
@lightbulb.option("oggetto", "Quale oggetto vuoi comprare?", type=str, required=True)
@lightbulb.command("compraoggetto", "Compra un oggetto dal mercato base. "
                                    "ASSICURATI DI AVER AVVISATO UN MASTER DI QUESTO ACQUISTO!")
@lightbulb.implements(lightbulb.SlashCommand)
async def buy_item(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.buy_item(ctx.options.oggetto, ctx.options.descrizione, ctx.options.prezzo)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("oggetto", "Quale oggetto vuoi vendere?", type=str, required=True)
@lightbulb.command("vendioggetto", "Vendi un oggetto agli npc. "
                                   "RICORDA, RICAVERAI IL 50% DEL VALORE DELL'OGGETTO!")
@lightbulb.implements(lightbulb.SlashCommand)
async def sell_item(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.sell_item(ctx.options.oggetto)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("statistica", "Quale statistica vuoi aumentare??", type=str,
                  choices=["Vigore", "Intuito", "Volontà", "Destrezza"], required=True)
@lightbulb.command("aumentastatistica", "Usa un oggetto")
@lightbulb.implements(lightbulb.SlashCommand)
async def increase_stat(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.increase_stat(ctx.options.statistica)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("oggetto", "Quale oggetto vuoi eliminare=", type=str, required=True)
@lightbulb.command("eliminaoggetto", "Elimina un oggetto dal tuo inventario")
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_item(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.delete_item(ctx.options.oggetto)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("identita", "Piccola frase che identifica il tuo personaggio", type=str, required=True)
@lightbulb.option("tema", "Una parola che descriva il tema del tuo personaggio", type=str, required=True)
@lightbulb.command("tratti", "Che tratti ha il tuo personaggio?")
@lightbulb.implements(lightbulb.SlashCommand)
async def traits(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.change_traits(ctx.options.identita, ctx.options.tema)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("pi", "Quanti PI devi cokmpare?", type=int, required=True)
@lightbulb.command("comprapi", "Compra PI")
@lightbulb.implements(lightbulb.SlashCommand)
async def buy_pi(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.buy_ip(ctx.options.pi)
    db.save_character(char, ctx.user.id)
    await ctx.respond(result)


@plugin.command
@lightbulb.option("statistica1", "Quale statistica vuoi tirare?", type=str, required=True, choices=STATS)
@lightbulb.option("statistica2", "Quale statistica vuoi tirare?", type=str, required=True, choices=STATS)
@lightbulb.option("modificatore", "Hai bonus o malus?", type=int, required=False)
@lightbulb.command("fabularoll", "Fai un tiro in stile FABULA!")
@lightbulb.implements(lightbulb.SlashCommand)
async def fabula_roll_command(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = f"Il tiro di {ctx.options.statistica1} e {ctx.options.statistica1} ha fatto {multidice_roll(char.get_stat(STATS[ctx.options.statistica1]), char.get_stat(STATS[ctx.options.statistica2]), ctx.options.modificatore)}"
    await ctx.respond(result)


@plugin.command
@lightbulb.option("nomeoggetto", "Di che oggetto nel tuo inventario vuoi saperne di più?", type=str, required=True)
@lightbulb.command("infooggetto", "Vedi maggiori informazioni di un oggetto che possiedi")
@lightbulb.implements(lightbulb.SlashCommand)
async def info_item_cmd(ctx: lightbulb.SlashContext) -> None:
    char = db.load_character(ctx.user.id)
    result = char.info_item(ctx.options.nomeoggetto)
    await ctx.respond(result)


@plugin.command()
@lightbulb.option("nomeoggetto", "Che oggetto vuoi vendere?", type=str, required=True)
@lightbulb.option("prezzo", "A quanto lo vuoi vendere?", type=int, required=True)
@lightbulb.option("menzione", "Menzione il giocatore a cui vuoi vendere l'oggetto", type=str, required=True)
@lightbulb.command("vendiagiocatore", "Vendi un oggetto ad un altro giocatore", auto_defer=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def sell_to_player_command(ctx: lightbulb.SlashContext) -> None:
    mentioned_id = clear_id_from_mention(ctx.options.menzione)

    # Getting the basic info to do the transaction
    seller_char: Character = db.load_character(ctx.user.id)
    buyer_char: Character = db.load_character(mentioned_id)
    item: Item = next(
        (item for item in seller_char.inventory if item.name.lower() == ctx.options.nomeoggetto.lower()), None)

    # Error message in case of item not found
    if item is None:
        await ctx.respond(f"{ctx.options.nomeoggetto} non è presente nel tuo inventario.\n"
                          f"Assicurati di aver scritto l'oggetto correttamente, /datipg per vedere il tuo inventario")
        return

    # Checking if item is sellable
    result = is_item_sellable(seller_char, buyer_char, item)
    if result != "ok":
        await ctx.respond(result)
        return

    # Creating the view for selling the item
    view = SellToPlayerView(seller=seller_char, buyer=buyer_char, item=item)
    question = f"{ctx.options.menzione} Vuoi comprare {ctx.options.nomeoggetto} a {ctx.options.prezzo} zenit?"
    await ctx.respond(question, components=view)
    ctx.app.d.miru.start_view(view)

    # You can also wait until the view is stopped or times out
    await view.wait()
