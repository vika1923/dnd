import random

def d20():
    return random.randint(1, 20)


def d12():
    return random.randint(1, 12)


def d10():
    return random.randint(0, 9)


def d8():
    return random.randint(1, 8)


def d6():
    return random.randint(1, 6)


def d4():
    return random.randint(1, 4)

def d_percent():
    return random.randint(0, 90) + d10()
