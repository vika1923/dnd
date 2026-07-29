import json
import math

from characters_selection_schemas import Dwarf, Elf, Halfling, Human, Fighter, Rogue


# ============================================================
# CHARACTER CREATION
# ============================================================


RACES = {
    "dwarf": Dwarf,
    "elf": Elf,
    "halfling": Halfling,
    "human": Human,
}

CLASSES = {
    "fighter": Fighter,
    "rogue": Rogue,
}


ABILITY_NAMES = [
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma",
]

ABILITY_SCORE_POOL = [15, 14, 13, 12, 10, 8]


def calculate_modifier(score):
    """
    Calculate D&D ability modifier.

    Examples:
        15 -> +2
        14 -> +2
        13 -> +1
        12 -> +1
        10 -> +0
        8  -> -1
    """

    return math.floor((score - 10) / 2)


def choose_race():
    """
    Ask the player to choose a race.
    Returns an instantiated race object.
    """

    print("\nChoose your race:")

    race_names = list(RACES.keys())

    for index, race_name in enumerate(race_names):
        print(f"{index}: {race_name.capitalize()}")

    while True:
        try:
            choice = int(input("Enter race index: "))

            if 0 <= choice < len(race_names):
                selected_race = race_names[choice]
                return RACES[selected_race]()

        except ValueError:
            pass

        print("Invalid choice. Try again.")


def choose_class():
    """
    Ask the player to choose a class.
    Returns an instantiated class object.
    """

    print("\nChoose your class:")

    class_names = list(CLASSES.keys())

    for index, class_name in enumerate(class_names):
        print(f"{index}: {class_name.capitalize()}")

    while True:
        try:
            choice = int(input("Enter class index: "))

            if 0 <= choice < len(class_names):
                selected_class = class_names[choice]
                return CLASSES[selected_class]()

        except ValueError:
            pass

        print("Invalid choice. Try again.")


def choose_ability_scores():
    """
    Ask the player to assign the standard ability score array:
    15, 14, 13, 12, 10, 8

    Returns:
        scores: dictionary of final ability scores
        modifiers: dictionary of ability modifiers
    """

    available_scores = ABILITY_SCORE_POOL.copy()
    scores = {}
    modifiers = {}

    print("\nAssign your ability scores.")
    print("Available scores:", available_scores)

    for ability in ABILITY_NAMES:

        print(f"\nChoose a score for {ability.capitalize()}:")
        print("Available:", available_scores)

        while True:
            try:
                score = int(input("Enter score: "))

                if score in available_scores:
                    break

            except ValueError:
                pass

            print("Invalid choice. Choose one of the available scores.")

        available_scores.remove(score)

        scores[ability] = score
        modifiers[ability] = calculate_modifier(score)

    return scores, modifiers


def character_to_dict(race, character_class, scores, modifiers):
    """
    Convert the race, class, ability scores, and player description
    into a JSON-serializable character sheet.
    """

    character_sheet = {

        # ====================================================
        # CHARACTER INFORMATION
        # ====================================================

        "name": "",
        "race": race.__class__.__name__,
        "class": character_class.__class__.__name__,
        "level": 2,

        # ====================================================
        # ABILITY SCORES
        # ====================================================

        "ability_scores": scores,

        "ability_modifiers": modifiers,


        # ====================================================
        # RACIAL INFORMATION
        # ====================================================

        "race_features": {

            "size": race.size,
            "speed": race.speed,
            "darkvision": race.darkvision,

            "skill_proficiency": race.skill_proficiency,
            "weapon_proficiency": race.weapon_proficiency,
            "armor_proficiency": race.armor_proficiency,
            "tool_proficiency": race.tool_proficiency,

            "languages": race.languages,

            "traits": race.traits,
            "resistances": race.resistances,
            "relationships": race.relationships,

            "longevity": race.longevity,
            "mature_at": race.mature_at,
            "alignment": race.alignment,
        },


        # ====================================================
        # CLASS INFORMATION
        # ====================================================

        "class_features": {

            "hit_die": character_class.hit_die,

            "starting_hit_points": (
                character_class.starting_hit_points
                + modifiers["constitution"]
            ),

            "armor_proficiency": character_class.armor_proficiency,
            "weapon_proficiency": character_class.weapon_proficiency,
            "tool_proficiency": character_class.tool_proficiency,

            "saving_throw_proficiency":
                character_class.saving_throw_proficiency,

            "skill_proficiency":
                character_class.skill_proficiency,

            "starting_equipment":
                character_class.starting_equipment,

            "features":
                character_class.features,
        },

        # ====================================================
        # GAME STATE
        # ====================================================

        "current_hit_points": (
            character_class.starting_hit_points
            + modifiers["constitution"]
        ),

        "temporary_hit_points": 0,

        "conditions": [],

        "status_effects": [],
    }

    return character_sheet


def save_character_sheet(character_sheet, file_path="character_sheet.json"):
    """
    Save character sheet as a JSON file.
    """

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            character_sheet,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nCharacter sheet saved to: {file_path}")


def create_character_sheet(
    file_path="character_sheet.json"
):
    """
    Complete interactive character creation.

    1. Choose race.
    2. Choose class.
    3. Assign ability scores.
    4. Calculate ability modifiers.
    5. Write character description.
    6. Create JSON character sheet.
    7. Save JSON file.

    Returns:
        character_sheet
    """

    print("========================================")
    print("        D&D CHARACTER CREATION")
    print("========================================")

    # --------------------------------------------------------
    # STEP 1: RACE
    # --------------------------------------------------------

    race = choose_race()

    print(
        f"\nSelected race: "
        f"{race.__class__.__name__}"
    )


    # --------------------------------------------------------
    # STEP 2: CLASS
    # --------------------------------------------------------

    character_class = choose_class()

    print(
        f"\nSelected class: "
        f"{character_class.__class__.__name__}"
    )


    # --------------------------------------------------------
    # STEP 3: ABILITY SCORES
    # --------------------------------------------------------

    scores, modifiers = choose_ability_scores()

    # --------------------------------------------------------
    # STEP 5: CREATE CHARACTER SHEET
    # --------------------------------------------------------

    character_sheet = character_to_dict(
        race=race,
        character_class=character_class,
        scores=scores,
        modifiers=modifiers,
    )

    # --------------------------------------------------------
    # STEP 6: SAVE JSON
    # --------------------------------------------------------

    save_character_sheet(
        character_sheet,
        file_path
    )

    return character_sheet

if __name__ == "__main__":
    print(create_character_sheet())