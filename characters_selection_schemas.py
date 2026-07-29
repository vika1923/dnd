# ============================================================
# RACES
# ============================================================


class Character:
    def __init__(self):
        # Ability Score Modifiers
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0

        # Basic Characteristics
        self.size = ""
        self.speed = 0
        self.darkvision = False

        # Proficiencies
        self.skill_proficiency = []
        self.weapon_proficiency = []
        self.armor_proficiency = []
        self.tool_proficiency = []

        # Languages
        self.languages = []

        # Racial Mechanics
        self.traits = []
        self.resistances = []
        self.relationships = {}

        # Character Context
        self.longevity = 0
        self.mature_at = 0
        self.alignment = ""

    @staticmethod
    def get_multiple_choices(choices_list, n=1):
        available_choices = list(choices_list)
        chosen = []

        for _ in range(n):
            for index, choice in enumerate(available_choices):
                print(f"Item {index}: {choice}")

            while True:
                try:
                    choice_index = int(
                        input("Enter your choice index: ")
                    )

                    if 0 <= choice_index < len(available_choices):
                        chosen.append(
                            available_choices.pop(choice_index)
                        )
                        break

                except ValueError:
                    pass

                print("Invalid choice. Try again.")

        return chosen


class Dwarf(Character):
    def __init__(self):
        super().__init__()

        # Ability Score Modifiers
        self.constitution += 2
        self.strength += 2

        # Basic Characteristics
        self.size = "medium"
        self.speed = 25
        self.darkvision = True

        # Proficiencies
        self.weapon_proficiency = [
            "battleaxe",
            "handaxe",
            "light hammer",
            "warhammer"
        ]

        self.armor_proficiency = [
            "light armor",
            "medium armor"
        ]

        self.tool_proficiency = [self.get_multiple_choices(["smith's tools", "brewer's supplies", "mason's tools"])]

        # Languages
        self.languages = [
            "Common",
            "Dwarvish"
        ]

        # Racial Mechanics
        self.resistances = [
            "resistance against poison damage"
        ]

        self.traits = [
            "advantage on saving throws against poison",
            "Stonecunning: Whenever you make an Intelligence (History) check related to the origin of stonework, you are considered proficient in the History skill and add double your proficiency bonus to the check."
        ]

        self.relationships = {
            "elf": "neutral",
            "human": "good",
            "halfling": "good",
            "dwarf": "good",
        }

        # Character Context
        self.longevity = 350
        self.mature_at = 50

        self.alignment = (
            "Most dwarves are lawful, believing firmly in the benefits of a well-ordered society. They tend toward good as well, with a strong sense of fair play and a belief that everyone deserves to share in the benefits of a just order."
        )


class Elf(Character):
    def __init__(self):
        super().__init__()

        # Ability Score Modifiers
        self.dexterity += 2
        self.intelligence += 1  # High Elf

        # Basic Characteristics
        self.size = "medium"
        self.speed = 30
        self.darkvision = True

        # Proficiencies
        self.skill_proficiency = [
            "perception"
        ]

        self.weapon_proficiency = [
            "longsword",
            "shortsword",
            "shortbow",
            "longbow"
        ]

        # Languages
        self.languages = [
            "Common",
            "Elvish",
            self.get_multiple_choices(["Dwarvish", "Halfling", "Thieves' Cant"])
        ]

        # Racial Mechanics
        self.traits = [
            "advantage on saving throws against being charmed",
            "magic can't put you to sleep",
            "Trance: Elves do not need to sleep. They meditate for 4 hours instead and gain the same benefit that a human gains from 8 hours of sleep.",
        ]

        self.relationships = {
            "elf": "good",
            "human": "good",
            "halfling": "good",
            "dwarf": "neutral",
        }

        # Character Context
        self.longevity = 750
        self.mature_at = 100

        self.alignment = (
            "Elves love freedom, variety, and self-expression, so they lean strongly toward chaos. They value and protect others' freedom and are more often good than not."
        )


class Halfling(Character):
    def __init__(self):
        super().__init__()

        # Ability Score Modifiers
        self.dexterity += 2
        self.charisma += 1  # Lightfoot Halfling

        # Basic Characteristics
        self.size = "small"
        self.speed = 25

        # Languages
        self.languages = [
            "Common",
            "Halfling"
        ]

        # Racial Mechanics
        self.traits = [
            "Lucky: When you roll a 1 on a d20 for an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll.",
            "Brave: You have advantage on saving throws against being frightened.",
            "Halfling Nimbleness: You can move through the space of any creature larger than you.",
            "Naturally Stealthy: You can attempt to hide when obscured only by a creature at least one size larger than you."
        ]

        self.relationships = {
            "elf": "good",
            "human": "good",
            "halfling": "good",
            "dwarf": "good",
        }

        # Character Context
        self.longevity = 150
        self.mature_at = 20

        self.alignment = (
            "Most halflings are lawful good. They are generally kind-hearted, orderly, traditional, and strongly connected to their communities."
        )


class Human(Character):
    def __init__(self):
        super().__init__()

        # Ability Score Modifiers
        self.strength += 1
        self.dexterity += 1
        self.constitution += 1
        self.intelligence += 1
        self.wisdom += 1
        self.charisma += 1

        # Basic Characteristics
        self.size = "medium"
        self.speed = 30

        # Languages
        self.languages = [
            "Common",
            self.get_multiple_choices(["Dwarvish", "Halfling", "Elvish", "Thieves' Cant"])
        ]

        self.relationships = {
            "elf": "neutral",
            "human": "good",
            "halfling": "good",
            "dwarf": "good",
        }

        # Character Context
        self.longevity = 90
        self.mature_at = 18

        self.alignment = (
            "Humans tend toward no particular alignment. Both the best and the worst can be found among them."
        )


# ============================================================
# CLASSES
# ============================================================


class Class(Character):
    def __init__(self):
        # Hit Points
        self.hit_die = ""
        self.starting_hit_points = 0

        # Proficiencies
        self.armor_proficiency = []
        self.weapon_proficiency = []
        self.tool_proficiency = []
        self.saving_throw_proficiency = []
        self.skill_proficiency = []

        # Equipment
        self.starting_equipment = []

        # Class Mechanics
        self.features = []


class Fighter(Class):
    def __init__(self):
        super().__init__()

        # Hit Points
        self.hit_die = "1d10"
        self.starting_hit_points = 10

        # Proficiencies
        self.armor_proficiency = [
            "all armor",
            "shields"
        ]

        self.weapon_proficiency = [
            "simple weapons",
            "martial weapons"
        ]

        self.tool_proficiency = []

        self.saving_throw_proficiency = [
            "strength",
            "constitution"
        ]

        self.skill_proficiency = self.get_multiple_choices(
            [
                "Acrobatics",
                "Animal Handling",
                "Athletics",
                "History",
                "Insight",
                "Intimidation",
                "Perception",
                "Survival",
            ],
            2,
        )

        # Equipment
        self.starting_equipment = [
            self.get_multiple_choices([
                "chain mail",
                "leather armor + longbow + 20 arrows",
            ]),

            self.get_multiple_choices([
                "a martial weapon + shield",
                "two martial weapons",
            ]),

            self.get_multiple_choices([
                "light crossbow + 20 bolts",
                "two handaxes",
            ]),

            self.get_multiple_choices([
                "dungeoneer's pack",
                "explorer's pack",
            ]),
        ]

        # Class Mechanics
        self.features = [
            "Great Weapon Fighting: When you roll a 1 or 2 on a damage die for a melee weapon wielded with two hands, you can reroll the die and must use the new roll. The weapon must have the two-handed or versatile property."
        ]


class Rogue(Class):
    def __init__(self):
        super().__init__()

        # Hit Points
        self.hit_die = "1d8"
        self.starting_hit_points = 8

        # Proficiencies
        self.armor_proficiency = [
            "light armor"
        ]

        self.weapon_proficiency = [
            "simple weapons",
            "hand crossbows",
            "longswords",
            "rapiers",
            "shortswords"
        ]

        self.tool_proficiency = [
            "thieves' tools"
        ]

        self.saving_throw_proficiency = [
            "dexterity",
            "intelligence"
        ]

        self.skill_proficiency = self.get_multiple_choices(
            [
                "Acrobatics",
                "Athletics",
                "Deception",
                "Insight",
                "Intimidation",
                "Investigation",
                "Perception",
                "Performance",
                "Persuasion",
                "Sleight of Hand",
                "Stealth",
            ],
            4,
        )

        # Equipment
        self.starting_equipment = [
            self.get_multiple_choices([
                "rapier",
                "shortsword",
            ]),

            self.get_multiple_choices([
                "shortbow + quiver of 20 arrows",
                "shortsword",
            ]),

            self.get_multiple_choices([
                "burglar's pack",
                "dungeoneer's pack",
                "explorer's pack",
            ]),

            "leather armor",
            "two daggers",
            "thieves' tools"
        ]

        # Class Mechanics
        self.features = [
            "Expertise: Choose two of your skill proficiencies, "
            "or one skill proficiency and your proficiency with "
            "thieves' tools. Your proficiency bonus is doubled "
            "for ability checks using the chosen proficiencies.",

            "Sneak Attack: Once per turn, you can deal an extra "
            "1d6 damage to one creature you hit with an attack "
            "if you have advantage on the attack roll. The attack "
            "must use a finesse or ranged weapon. You can also "
            "use Sneak Attack when another enemy of the target "
            "is within 5 feet of it, that enemy is not incapacitated, "
            "and you do not have disadvantage.",

            "Thieves' Cant: You know the secret language and symbols "
            "used by thieves to communicate hidden messages.",

            "Cunning Action: You can take a bonus action on each "
            "of your turns in combat. This bonus action can be "
            "used to Dash, Disengage, or Hide."
        ]