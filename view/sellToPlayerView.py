import copy

import hikari
import miru

from classes.character import Character
from classes.item import Item


class BuyButton(miru.Button):
    def __init__(self) -> None:
        # Initialize our button with some pre-defined properties
        super().__init__(style=hikari.ButtonStyle.SUCCESS, label="Acquista")

    async def callback(self, ctx: miru.ViewContext) -> None:
        if ctx.user.id == self.view.buyer:
            if self.view.item.quantity > 0:
                temp_item = copy.deepcopy(self.view.item)
                temp_item.quantity = 1
                self.view.buyer.inventory.append(temp_item)
                self.view.buyer.zenit -= self.view.item.price
                self.view.seller.inventory[self.view.item] -= 1
            else:
                self.view.buyer.inventory.append(copy.deepcopy(self.view.item))
                self.view.buyer.zenit -= self.view.item.price
                self.view.seller.inventory.pop(self.view.item)
        else:
            await ctx.respond("Non sei il compratore!", flags=hikari.MessageFlag.EPHEMERAL)


class RefuseButton(miru.Button):
    def __init__(self) -> None:
        # Initialize our button with some pre-defined properties
        super().__init__(style=hikari.ButtonStyle.DANGER, label="Rifiuta")

    async def callback(self, ctx: miru.ViewContext) -> None:
        if ctx.user.id == self.view.buyer:
            await ctx.get_channel().send("L'acquirente ha rifiutato l'acquisto")
            self.view.stop()
        else:
            await ctx.respond("Non sei il compratore!", flags=hikari.MessageFlag.EPHEMERAL)


class SellToPlayerView(miru.View):
    accept = BuyButton()
    refuse = RefuseButton()

    def __init__(self, seller, buyer, item, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.seller: Character = seller
        self.buyer: Character = buyer
        self.item: Item = item
