# virtu

import json


def increase_virtu(ctx, amount):
    with open('virtu.json', 'r') as file:
        virtu_levels = json.load(file)

    if ctx.author.id not in virtu_levels:
        virtu_levels[str(ctx.author.id)] += amount

    with open('virtu.json', 'w') as file:
        json.dump(virtu_levels, file, indent=4)
