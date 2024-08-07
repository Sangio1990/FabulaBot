import typing as t

import hikari
import miru
from miru import ViewContext, SelectOption, AutodeferOptions

from data.data import CLASSES, cls_json


class YesButton(miru.Button):
    def __init__(self) -> None:
        # Initialize our button with some pre-defined properties
        super().__init__(style=hikari.ButtonStyle.SUCCESS, label="Yes")
        self.value = True

    # The callback is the function that gets called when the button is pressed
    # If you are subclassing, you must use the name "callback" when defining it.
    async def callback(self, ctx: miru.ViewContext) -> None:
        # You can specify the ephemeral message flag
        # to make your response ephemeral
        await ctx.respond(
            "I'm sorry but this is unacceptable.",
            flags=hikari.MessageFlag.EPHEMERAL
        )
        # You can access the view an item is attached to
        # by accessing it's view property
        self.view.answer = self.value
        # self.view.stop()


class NoButton(miru.Button):
    # Let's leave our arguments dynamic this time, instead of hard-coding them
    def __init__(self, style: hikari.ButtonStyle, label: str = "No") -> None:
        super().__init__(style=style, label=label)
        self.value = False

    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond(
            "This is the only correct answer.",
            flags=hikari.MessageFlag.EPHEMERAL
        )
        self.view.answer = self.value
        self.view.stop()


class LevelUpView(miru.View):
    """
    # Include our custom buttons.
    yes = YesButton()
    no = NoButton(style=hikari.ButtonStyle.DANGER)
    # Let's also add a link button.
    # Link buttons cannot have a callback,
    # they simply direct the user to the given website
    learn_more = miru.LinkButton(
        url="https://en.wikipedia.org/wiki/Hawaiian_pizza", label="Learn More"
    )
    """

    class_options = [miru.SelectOption(label=class_name) for class_name in CLASSES]

    @miru.text_select(
        options=class_options,
        placeholder="Selezione la classe",
    )
    async def get_class(self, ctx: miru.ViewContext, class_select: miru.TextSelect) -> None:
        await ctx.respond(f"You've chosen {class_select.values[0]}!")
        choosen_class = class_select.values[0]
        class_info = cls_json.get(choosen_class)
        if class_info:
            abilities = class_info.get('abilities', [])
        abilities_options = [miru.SelectOption(label=ability_name) for ability_name in abilities]

        @miru.text_select(
            options=abilities_options,
            placeholder="Seleziona un'abilità"
        )
        async def choose_print(self, ability_select: miru.SelectOption, ctx: miru.ViewContext) -> None:
            await ctx.respond(f"You've chosen {ability_select.value}")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.answer: bool | None = None
