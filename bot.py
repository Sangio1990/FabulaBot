import lightbulb
from hikari import Intents
import sqlite3

from db.utilsDB import UtilsDB, NoCharFound
from secretsData.data import *
from utils.utils import role_name

# Setting up the DB
db = UtilsDB()
db.init_db(connection=sqlite3.connect("db/Iridis.db"))

INTENTS = Intents.ALL

bot = lightbulb.BotApp(
    chosen_region[TOKEN],
    intents=INTENTS,
    prefix="!!",
    banner=None,
    default_enabled_guilds=chosen_region[GUILD]
)

bot.load_extensions("cmds.userCommands", "cmds.adminCommands", "cmds.masterCommands", "cmds.playerCommands")


# Define a listener for handling command errors in the bot
@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    """
    Handle command errors that occur during bot command invocation.

    Parameters:
    - event (lightbulb.CommandErrorEvent): The event object containing information about the error.

    Returns:
    - None

    This function checks the type of the exception that occurred during command execution and responds accordingly.
    If the exception is of type NoCharFound, it responds with a message indicating that the character was not found.
    If the exception is of type MissingRequiredRole, it responds with a message indicating the required role for using the command.
    If the exception is of type CommandInvocationError, it prints the original exception and responds with a generic error message.
    If the exception is of any other type, it prints the exception and its information and responds with a generic error message.
    """
    if isinstance(event.exception, NoCharFound):
        await event.context.respond("Non ho trovato il personaggio, assicurati che sia stato creato.")
    elif isinstance(event.exception, lightbulb.errors.MissingRequiredRole):
        role = event.exception.missing_roles[0]
        await event.context.respond(f"Sono spiacente, per usare questo comando devi avere il ruolo {role_name(role)}.")
    elif isinstance(event.exception, lightbulb.errors.CommandInvocationError):
        print(event.exception.original)
        await event.context.respond("Errore nell'esecuzione del comando, contatta un amministratore.")
    else:
        print(event.exception)
        print(event.exc_info)
        await event.context.respond("Errore nel bot, contatta un amministratore.")


if __name__ == "__main__":
    bot.run()
