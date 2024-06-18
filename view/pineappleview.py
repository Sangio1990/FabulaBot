import hikari
import miru


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


class PineappleView(miru.View):
    # Include our custom buttons.
    yes = YesButton()
    no = NoButton(style=hikari.ButtonStyle.DANGER)
    # Let's also add a link button.
    # Link buttons cannot have a callback,
    # they simply direct the user to the given website
    learn_more = miru.LinkButton(
        url="https://en.wikipedia.org/wiki/Hawaiian_pizza", label="Learn More"
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.answer: bool | None = None
