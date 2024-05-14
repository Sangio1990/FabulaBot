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
