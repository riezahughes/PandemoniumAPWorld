from enum import IntEnum
from typing import Optional, NamedTuple, Dict, List
from BaseClasses import Location, Region
from .Items import PandemoniumItem


class PandemoniumLocationCategory(IntEnum):
    PROGRESSION = 0
    EVENT = 1
    LEVEL_CLEAR = 2
    RACE_CLEAR = 3
    PINBALL_CLEAR = 4
    LEVEL_PERCENTAGE = 5
    ENEMY_KILL = 6
    TRANSFORM_GATE = 7
    CHARACTER_CLEAR = 8


class PandemoniumLocationData(NamedTuple):
    name: str
    default_item: str
    category: PandemoniumLocationCategory


class PandemoniumLocation(Location):
    game: str = "Pandemonium"
    category: PandemoniumLocationCategory
    default_item_name: str

    def __init__(
        self,
        player: int,
        name: str,
        category: PandemoniumLocationCategory,
        default_item_name: str,
        address: Optional[int] = None,
        parent: Optional[Region] = None,
    ):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category
        self.name = name

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 99270000
        region_offset = 1000
        table_order = [
            "Menu",
            "Map",
            "Skull Fortress",
            "Hollow Stairway",
            "Dungeon Tower",
            "Lost Caves",
            "Fungus Grotto",
            "Acid Pools",
            "Shroom Lord",
            "Burning Desert",
            "Branky Wastes",
            "Spider Forest",
            "Canopy Village",
            "Soldier Barracks",
            "Honcho's Logmill",
            "Goon Honcho",
            "Honcho's Airship",
            "Dragoon Skyfort",
            "Cloud Citadel",
            "Efreet Palace",
            "Frozen Cavern",
            "Storm Temple",
            "The Wishing Engine",
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            current_region_base_id = base_id + (i * region_offset)
            for j, location_data in enumerate(location_tables[region_name]):
                if location_data.category != PandemoniumLocationCategory.EVENT:
                    output[location_data.name] = current_region_base_id + j

        return output

    def place_locked_item(self, item: PandemoniumItem):
        self.item = item
        self.locked = True
        item.location = self


location_tables = {
    "Menu": [],
    "Map": [],
    "Skull Fortress": [
        PandemoniumLocationData("Full Tilt: Skull Fortress", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Skull Fortress", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Skull Fortress", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Hollow Stairway": [
        PandemoniumLocationData("Full Tilt: Hollow Stairway", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Hollow Stairway", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Hollow Stairway", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Dungeon Tower": [
        PandemoniumLocationData("Full Tilt: Dungeon Tower", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Dungeon Tower", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Dungeon Tower", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Lost Caves": [
        PandemoniumLocationData("Full Tilt: Lost Caves", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Lost Caves", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Lost Caves", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Fungus Grotto": [
        PandemoniumLocationData("Full Tilt: Fungus Grotto", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Fungus Grotto", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Fungus Grotto", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
        PandemoniumLocationData("Frog Gate: Fungus Grotto", "Extra Life", PandemoniumLocationCategory.TRANSFORM_GATE),
    ],
    "Acid Pools": [
        PandemoniumLocationData("Full Tilt: Acid Pools", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Acid Pools", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Acid Pools", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
        PandemoniumLocationData("Frog Gate: Acid Pools", "Extra Life", PandemoniumLocationCategory.TRANSFORM_GATE),
    ],
    "Shroom Lord": [
        PandemoniumLocationData("Level Cleared: Shroom Lord", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Burning Desert": [
        PandemoniumLocationData("Full Tilt: Burning Desert", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Burning Desert", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Burning Desert", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Branky Wastes": [
        PandemoniumLocationData("Full Tilt: Branky Wastes", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Branky Wastes", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Branky Wastes", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
        PandemoniumLocationData("Rhino Gate: Branky Wastes", "Extra Life", PandemoniumLocationCategory.TRANSFORM_GATE),
    ],
    "Spider Forest": [
        PandemoniumLocationData("Full Tilt: Spider Forest", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Spider Forest", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Spider Forest", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Canopy Village": [
        PandemoniumLocationData("Full Tilt: Canopy Village", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Canopy Village", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Canopy Village", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
        PandemoniumLocationData("Turtle Gate: Canopy Village", "Extra Life", PandemoniumLocationCategory.TRANSFORM_GATE),
    ],
    "Soldier Barracks": [
        PandemoniumLocationData("Full Tilt: Soldier Barracks", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Soldier Barracks", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Soldier Barracks", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Honcho's Logmill": [
        PandemoniumLocationData("Full Tilt: Honcho's Logmill", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Honcho's Logmill", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Honcho's Logmill", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Goon Honcho": [
        PandemoniumLocationData("Level Cleared: Goon Honcho", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Honcho's Airship": [
        PandemoniumLocationData("Full Tilt: Honcho's Airship", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Honcho's Airship", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Honcho's Airship", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
        PandemoniumLocationData("Dragon Gate: Honcho's Airship", "Extra Life", PandemoniumLocationCategory.TRANSFORM_GATE),
    ],
    "Dragoon Skyfort": [
        PandemoniumLocationData("Full Tilt: Dragoon Skyfort", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Dragoon Skyfort", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Dragoon Skyfort", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Cloud Citadel": [
        PandemoniumLocationData("Full Tilt: Cloud Citadel", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Cloud Citadel", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Cloud Citadel", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Efreet Palace": [
        PandemoniumLocationData("Full Tilt: Efreet Palace", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Efreet Palace", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Efreet Palace", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Frozen Cavern": [
        PandemoniumLocationData("Full Tilt: Frozen Cavern", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Frozen Cavern", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Frozen Cavern", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "Storm Temple": [
        PandemoniumLocationData("Full Tilt: Storm Temple", "Extra Life", PandemoniumLocationCategory.PINBALL_CLEAR),
        PandemoniumLocationData("Speed Greed: Storm Temple", "Extra Life", PandemoniumLocationCategory.RACE_CLEAR),
        PandemoniumLocationData("Level Cleared: Storm Temple", "Extra Life", PandemoniumLocationCategory.LEVEL_CLEAR),
    ],
    "The Wishing Engine": [
        # The client reports the goal when the credits roll, so this is an event rather than a check
        PandemoniumLocationData("Game Completed", "Credits", PandemoniumLocationCategory.EVENT),
    ],
}


CHARACTERS = ("Fargus", "Nikki")
BOSS_LEVELS = ("Shroom Lord", "Goon Honcho")


def percentage_thresholds(step: int) -> List[int]:
    """Every multiple of `step` below 100, then 100 itself. This gives ceil(100 / step) checks per level."""
    return list(range(step, 100, step)) + [100]


def percentage_from_name(name: str) -> int:
    return int(name.split(" Percent Cleared: ")[0])


# Each level clear also gets a per-character clear, used when levels must be cleared as both characters.
# These are appended to the end of each region so the IDs of the locations above never move.
for location_table in location_tables.values():
    level_clears = [location_data for location_data in location_table if location_data.category == PandemoniumLocationCategory.LEVEL_CLEAR]
    for location_data in level_clears:
        level = location_data.name.removeprefix("Level Cleared: ")
        location_table.extend(
            PandemoniumLocationData(f"{character} Cleared: {level}", location_data.default_item, PandemoniumLocationCategory.CHARACTER_CLEAR)
            for character in CHARACTERS
        )

# Every possible percentage check (1% to 100%) for every non-boss level, so the IDs are the same whatever the
# player chooses. Each world only keeps the thresholds its option produces. Appended last so earlier IDs never move.
for region_name, location_table in location_tables.items():
    has_level_clear = any(location_data.category == PandemoniumLocationCategory.LEVEL_CLEAR for location_data in location_table)
    if not has_level_clear or region_name in BOSS_LEVELS:
        continue
    location_table.extend(
        PandemoniumLocationData(f"{percentage} Percent Cleared: {region_name}", "Extra Life", PandemoniumLocationCategory.LEVEL_PERCENTAGE)
        for percentage in range(1, 101)
    )

location_dictionary: Dict[str, PandemoniumLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
