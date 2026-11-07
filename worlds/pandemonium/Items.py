from enum import IntEnum
from random import Random
from typing import NamedTuple, List, Optional
from BaseClasses import Item, ItemClassification
from .Options import GoalOptions


class PandemoniumItemCategory(IntEnum):
    FILLER = 0
    CHARACTER = 1
    WEAPON = 2
    TRANSFORMATION = 3
    LEVEL = 4
    STAT_ITEM = 5
    PROGRESSION = 6
    EVENT = 7


class PandemoniumItemData(NamedTuple):
    name: str
    p_code: Optional[int]
    category: PandemoniumItemCategory
    progression: bool


class PandemoniumItem(Item):
    game: str = "Pandemonium"
    category: PandemoniumItemCategory
    p_code: Optional[int]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)

        # Store game-specific data directly on the item instance
        item_data = item_dictionary.get(name)
        if item_data:
            self.p_code = item_data.p_code
            self.category = item_data.category
        else:
            self.p_code = None
            self.category = PandemoniumItemCategory.FILLER  # Fallback for unknown items

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 9903000
        # Create a dictionary mapping item names to their unique Archipelago IDs.
        return {item_data.name: (base_id + item_data.p_code) for item_data in _all_items if item_data.p_code is not None}


_all_items = [
    # Character Unlock Items
    ("Fargus Unlock", 1, PandemoniumItemCategory.CHARACTER, True),
    ("Nikki Unlock", 2, PandemoniumItemCategory.CHARACTER, True),
    # Weapon Items
    ("Eldritch Fireball", 3, PandemoniumItemCategory.WEAPON, False),
    ("Phoenix Fireball", 4, PandemoniumItemCategory.WEAPON, False),
    ("Freeze Ray", 5, PandemoniumItemCategory.WEAPON, False),
    ("Shrink Ray", 6, PandemoniumItemCategory.WEAPON, False),
    ("Invincibility Shield", 7, PandemoniumItemCategory.WEAPON, False),
    # Level Unlock Items
    ("Skull Fortress Unlock", 8, PandemoniumItemCategory.LEVEL, True),
    ("Hollow Stairway Unlock", 9, PandemoniumItemCategory.LEVEL, True),
    ("Dungeon Tower Unlock", 10, PandemoniumItemCategory.LEVEL, True),
    ("Lost Caves Unlock", 11, PandemoniumItemCategory.LEVEL, True),
    ("Fungus Grotto Unlock", 12, PandemoniumItemCategory.LEVEL, True),
    ("Acid Pools Unlock", 13, PandemoniumItemCategory.LEVEL, True),
    ("Shroom Lord Unlock", 14, PandemoniumItemCategory.LEVEL, True),
    ("Burning Desert Unlock", 15, PandemoniumItemCategory.LEVEL, True),
    ("Branky Wastes Unlock", 16, PandemoniumItemCategory.LEVEL, True),
    ("Spider Forest Unlock", 17, PandemoniumItemCategory.LEVEL, True),
    ("Canopy Village Unlock", 18, PandemoniumItemCategory.LEVEL, True),
    ("Soldier Barracks Unlock", 19, PandemoniumItemCategory.LEVEL, True),
    ("Honcho's Logmill Unlock", 20, PandemoniumItemCategory.LEVEL, True),
    ("Goon Honcho Unlock", 21, PandemoniumItemCategory.LEVEL, True),
    ("Honcho's Airship Unlock", 22, PandemoniumItemCategory.LEVEL, True),
    ("Dragoon Skyfort Unlock", 23, PandemoniumItemCategory.LEVEL, True),
    ("Cloud Citadel Unlock", 24, PandemoniumItemCategory.LEVEL, True),
    ("Efreet Palace Unlock", 25, PandemoniumItemCategory.LEVEL, True),
    ("Frozen Cavern Unlock", 26, PandemoniumItemCategory.LEVEL, True),
    ("Storm Temple Unlock", 27, PandemoniumItemCategory.LEVEL, True),
    # ("Wishing Engine Unlock", 28, PandemoniumItemCategory.LEVEL, True),  # Ignored, as this will be unlocked by collecting mcguffins
    # Transformation Unlock Items
    ("Frog Transformation Unlock", 29, PandemoniumItemCategory.TRANSFORMATION, True),
    ("Rhino Transformation Unlock", 30, PandemoniumItemCategory.TRANSFORMATION, True),
    ("Dragon Transformation Unlock", 31, PandemoniumItemCategory.TRANSFORMATION, True),
    ("Turtle Transformation Unlock", 32, PandemoniumItemCategory.TRANSFORMATION, True),
    # Player Stat Items
    ("Progressive Health Upgrade", 34, PandemoniumItemCategory.STAT_ITEM, True),
    ("Free Health", 35, PandemoniumItemCategory.STAT_ITEM, False),
    ("Extra Life", 36, PandemoniumItemCategory.STAT_ITEM, False),
    # Progression Items
    ("Spellbook Page", 37, PandemoniumItemCategory.PROGRESSION, True),
    # Events (no code, never sent over the network)
    ("Credits", None, PandemoniumItemCategory.EVENT, True),
]
# Convert raw list of tuples into PandemoniumItemData NamedTuple instances
_all_items = [PandemoniumItemData(row[0], row[1], row[2], row[3]) for row in _all_items]


item_descriptions = {
    # Optional: Add detailed descriptions for items here
}

# Create a dictionary for quick lookup of item data by name
item_dictionary: dict[str, PandemoniumItemData] = {item_data.name: item_data for item_data in _all_items}


HEALTH_UPGRADE_COUNT = 4

# Items used to pad out the pool once everything else has been added
filler_item_names: List[str] = [item_data.name for item_data in _all_items if item_data.category == PandemoniumItemCategory.WEAPON] + ["Extra Life"]


def BuildItemPool(count: int, options, random: Random, starting_levels: List[str], starting_characters: List[str]) -> List[str]:
    """
    Generates a list of item names to be used for the item pool.
    This function does NOT create Archipelago Item objects; it only provides their names.
    The actual Item objects are created in PandemoniumWorld.create_items.
    """
    item_pool_names: List[str] = [
        item_data.name
        for item_data in _all_items
        if (item_data.category == PandemoniumItemCategory.PROGRESSION and item_data.name != "Spellbook Page")
        or item_data.category == PandemoniumItemCategory.LEVEL
        or item_data.category == PandemoniumItemCategory.TRANSFORMATION
    ]

    # The starting levels' unlocks are given to the player up front instead
    for level in starting_levels:
        item_pool_names.remove(f"{level} Unlock")

    # Only the characters you don't start with go into the pool
    for character in ("Fargus", "Nikki"):
        if character not in starting_characters:
            item_pool_names.append(f"{character} Unlock")

    item_pool_names.extend(["Progressive Health Upgrade"] * HEALTH_UPGRADE_COUNT)

    # Spell pages only go in for the spell page goals, and are capped to the room left in the pool
    if options.goal.value in (GoalOptions.SPELL_PAGES, GoalOptions.BOTH):
        spell_page_count = min(options.spellbook_pages.value, max(count - len(item_pool_names), 0))
        if spell_page_count < options.spellbook_pages.value:
            print(f"Warning: Only room for {spell_page_count} of {options.spellbook_pages.value} spell pages. Lowering the requirement to match.")
        item_pool_names.extend(["Spellbook Page"] * spell_page_count)

    if len(item_pool_names) > count:
        print(f"Warning: Item pool size ({len(item_pool_names)}) is larger than location count ({count}).")

    # Pad out the remaining locations with filler
    while len(item_pool_names) < count:
        item_pool_names.append(random.choice(filler_item_names))

    return item_pool_names
