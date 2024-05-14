import random


def roll(sides: int, times: int, modifier: int):
    if modifier is None:
        modifier = 0
    if times is None:
        times = 1
    rolls = []
    for i in range(times):
        rolls.append(random.randint(1, sides))
    total = sum(rolls) + modifier
    if modifier == 0:
        return f"{times}d{sides} = **{total}** {rolls}"
    elif modifier > 0:
        return f"{times}d{sides} + {modifier} = **{total}** {rolls}"
    elif modifier < 0:
        return f"{times}d{sides} - {abs(modifier)} = **{total}** {rolls}"


def multidice_roll(dice1: int, dice2: int, modifier: int):
    text = ""
    if modifier is None:
        modifier = 0
    rolls = [random.randint(1, dice1), random.randint(1, dice2)]
    total = sum(rolls) + modifier
    if modifier == 0:
        text = f"**{total}** {rolls}"
    elif modifier > 0:
        text = f"**{total}** {rolls}(+{modifier})"
    elif modifier < 0:
        text = f"**{total}** {rolls}(-{abs(modifier)})"

    if rolls[0] == rolls[1]:
        if rolls[0] >= 6:
            text += "```ansi\n\u001b[1;32mSUCCESSO CRITICO!\u001b[0;0m ```"
        elif rolls[0] == 1:
            text += "\n```ansi\n\u001b[1;31mFALLIMENTO CRITICO!\u001b[0;0m ```"
    return text
