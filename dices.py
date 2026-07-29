import random

def roll_dice(count: int, sides: int) -> dict:
    """Roll one or more D&D dice."""

    valid_sides = (4, 6, 8, 10, 12, 20, 100)

    if sides not in valid_sides:
        raise ValueError(f"Invalid die size: d{sides}")

    if count < 1:
        raise ValueError("Dice count must be at least 1")

    rolls = [
        random.randint(1, sides)
        for _ in range(count)
    ]

    return {
        "rolls": rolls,
        "total": sum(rolls),
    }

if __name__=="__main__":
    print(roll_dice(2, 12))
