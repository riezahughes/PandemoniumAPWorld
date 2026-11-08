# world/pandemonium/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification

from worlds.AutoWorld import World, WebWorld

from .Items import PandemoniumItem, PandemoniumItemCategory, item_dictionary, item_descriptions, filler_item_names, BuildItemPool
from .Locations import (
    PandemoniumLocation,
    PandemoniumLocationCategory,
    PandemoniumLocationData,
    location_tables,
    location_dictionary,
    BOSS_LEVELS,
    percentage_thresholds,
    percentage_from_name,
    percentage_level_from_name,
    points_from_name,
    points_level_from_name,
    POINT_MAXIMUMS,
    max_percentage,
)
from .Options import PandemoniumOption, StartingLevelOptions, CharacterOptions
from .Rules import set_level_unlock_rules, set_wishing_engine_rules, set_character_clear_rules
from .VictoryConditions import credits_victory


# Levels whose keys can be given at the start, in level order (Progressive takes them from the front, Random picks
# from anywhere). Boss levels are never given at the start, and The Wishing Engine is left out as it has no unlock item.
random_starting_levels = [region_name for region_name in location_tables if region_name not in ("Menu", "Map", "The Wishing Engine") and region_name not in BOSS_LEVELS]


class PandemoniumWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Pandemonium randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["RiezaHughes"],
    )

    tutorials = [setup_en]


class PandemoniumWorld(World):
    """
    Pandemonium is a 2.5D platformer about Sheogorath being stuck inside a PS1 Game
    """

    game: str = "Pandemonium"
    explicit_indirect_conditions = False
    options_dataclass = PandemoniumOption
    options: PandemoniumOption
    topology_present: bool = True
    web = PandemoniumWeb()
    base_id = 1250000
    enabled_location_categories: Set[PandemoniumLocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = PandemoniumItem.get_name_to_id()
    location_name_to_id = PandemoniumLocation.get_name_to_id()
    item_name_groups = {}
    item_descriptions = item_descriptions

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.enabled_location_categories = set()
        # the levels whose keys the player starts with
        self.starting_levels: List[str] = ["Skull Fortress"]
        self.spell_pages_required = 0
        self.starting_characters: List[str] = ["Fargus"]
        # the percentage thresholds each level gives checks at
        self.percentages: Dict[str, Set[int]] = {}
        # the point break points each level gives checks at (Pointsanity)
        self.point_thresholds: Dict[str, Set[int]] = {}

    def generate_early(self):
        starting_keys = min(self.options.starting_keys.value, len(random_starting_levels))
        if self.options.starting_level.value == StartingLevelOptions.RANDOM_LEVEL:
            # any levels, in level order so they read nicely
            picked = set(self.random.sample(random_starting_levels, starting_keys))
            self.starting_levels = [level for level in random_starting_levels if level in picked]
        else:
            # Progressive: the first levels in order, so 3 keys gives Skull Fortress, Hollow Stairway and Dungeon Tower
            self.starting_levels = random_starting_levels[:starting_keys]

        step = self.options.level_percentage_range.value
        max_range = self.options.level_percentage_max_range.value
        self.percentages = {level: set(percentage_thresholds(step, min(max_range, max_percentage(level)))) for level in location_tables}

        # same break point rule as the percentages, capped at each level's point maximum
        point_step = self.options.pointsanity_range.value
        self.point_thresholds = {level: set(percentage_thresholds(point_step, maximum)) for level, maximum in POINT_MAXIMUMS.items()}

        character_option = self.options.character_option.value
        if character_option == CharacterOptions.NIKKI:
            self.starting_characters = ["Nikki"]
        elif character_option == CharacterOptions.BOTH:
            self.starting_characters = ["Fargus", "Nikki"]
        elif character_option == CharacterOptions.RANDOM_CHARACTER:
            self.starting_characters = [self.random.choice(["Fargus", "Nikki"])]

        # EVENT is deliberately left out: event locations get a locked event item in create_region
        self.enabled_location_categories.add(PandemoniumLocationCategory.PROGRESSION)
        self.enabled_location_categories.add(PandemoniumLocationCategory.LEVEL_CLEAR)
        self.enabled_location_categories.add(PandemoniumLocationCategory.RACE_CLEAR)
        self.enabled_location_categories.add(PandemoniumLocationCategory.PINBALL_CLEAR)
        self.enabled_location_categories.add(PandemoniumLocationCategory.LEVEL_PERCENTAGE)
        self.enabled_location_categories.add(PandemoniumLocationCategory.ENEMY_KILL)
        self.enabled_location_categories.add(PandemoniumLocationCategory.TRANSFORM_GATE)
        self.enabled_location_categories.add(PandemoniumLocationCategory.CHARACTER_CLEAR)
        self.enabled_location_categories.add(PandemoniumLocationCategory.POINTS)

    def is_location_enabled(self, location: PandemoniumLocationData) -> bool:
        """Whether the player's options include this location in their world"""
        multiclear = bool(self.options.multiclear.value)

        if location.category == PandemoniumLocationCategory.LEVEL_CLEAR:
            return not multiclear
        if location.category == PandemoniumLocationCategory.CHARACTER_CLEAR:
            return multiclear
        if location.category == PandemoniumLocationCategory.PINBALL_CLEAR:  # Full Tilt
            return bool(self.options.full_tilt.value)
        if location.category == PandemoniumLocationCategory.RACE_CLEAR:  # Speed Greed
            return bool(self.options.speed_greed.value)
        if location.category == PandemoniumLocationCategory.POINTS:
            if not self.options.pointsanity.value:
                return False
            return points_from_name(location.name) in self.point_thresholds[points_level_from_name(location.name)]
        if location.category == PandemoniumLocationCategory.ENEMY_KILL:
            return bool(self.options.enemysanity.value)
        if location.category == PandemoniumLocationCategory.LEVEL_PERCENTAGE:
            if not self.options.level_percentage.value:
                return False
            return percentage_from_name(location.name) in self.percentages[percentage_level_from_name(location.name)]
        return True

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}

        list_of_regions = [
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

        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in list_of_regions})

        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", "Map")
        create_connection("Map", "Skull Fortress")
        create_connection("Map", "Hollow Stairway")
        create_connection("Map", "Dungeon Tower")
        create_connection("Map", "Lost Caves")
        create_connection("Map", "Fungus Grotto")
        create_connection("Map", "Acid Pools")
        create_connection("Map", "Shroom Lord")
        create_connection("Map", "Burning Desert")
        create_connection("Map", "Branky Wastes")
        create_connection("Map", "Spider Forest")
        create_connection("Map", "Canopy Village")
        create_connection("Map", "Soldier Barracks")
        create_connection("Map", "Honcho's Logmill")
        create_connection("Map", "Goon Honcho")
        create_connection("Map", "Honcho's Airship")
        create_connection("Map", "Dragoon Skyfort")
        create_connection("Map", "Cloud Citadel")
        create_connection("Map", "Efreet Palace")
        create_connection("Map", "Frozen Cavern")
        create_connection("Map", "Storm Temple")
        create_connection("Map", "The Wishing Engine")

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        for location in location_table:
            if not self.is_location_enabled(location):
                continue

            if location.category in self.enabled_location_categories:
                new_location = PandemoniumLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region,
                )
            else:
                # Event locations hold a locked event item with no code
                new_location = PandemoniumLocation(self.player, location.name, location.category, location.default_item, None, new_region)
                event_item = PandemoniumItem(location.default_item, ItemClassification.progression, None, self.player)
                new_location.place_locked_item(event_item)

            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        # Start the player with their starting levels already unlocked
        for level in self.starting_levels:
            self.multiworld.push_precollected(self.create_item(f"{level} Unlock"))

        # ...and with their starting characters, so every character rule can simply check for the unlock
        for character in self.starting_characters:
            self.multiworld.push_precollected(self.create_item(f"{character} Unlock"))

        randomized_location_count = 0
        for location in self.multiworld.get_locations(self.player):
            if not location.locked and location.address is not None:
                randomized_location_count += 1

        # Call BuildItemPool to get a list of item NAMES (strings)
        item_names_to_add = BuildItemPool(randomized_location_count, self.options, self.random, self.starting_levels, self.starting_characters)

        # With few checks enabled there may not be room for everything. Health upgrades are the only
        # non-progression items that have to exist, so any that don't fit are given at the start instead.
        while len(item_names_to_add) > randomized_location_count and "Progressive Health Upgrade" in item_names_to_add:
            item_names_to_add.remove("Progressive Health Upgrade")
            self.multiworld.push_precollected(self.create_item("Progressive Health Upgrade"))

        # The Wishing Engine needs every spell page that made it into the pool
        self.spell_pages_required = item_names_to_add.count("Spellbook Page")

        generated_items: List[Item] = []
        for item_name in item_names_to_add:
            new_item = self.create_item(item_name)
            generated_items.append(new_item)

        # Add the generated PandemoniumItem objects to the multiworld's item pool
        self.multiworld.itempool.extend(generated_items)

    def create_item(self, name: str) -> Item:
        item_data = item_dictionary.get(name)

        if not item_data:
            # Fallback for unknown items. This indicates a data inconsistency.
            print(f"Warning: Attempted to create unknown item: {name}. Falling back to filler.")
            return PandemoniumItem(name, ItemClassification.filler, None, self.player)

        # Determine the Archipelago ItemClassification based on PandemoniumItemData.
        item_classification: ItemClassification

        if item_data.progression or item_data.category == PandemoniumItemCategory.PROGRESSION:
            item_classification = ItemClassification.progression
        else:
            item_classification = ItemClassification.filler

        return PandemoniumItem(name, item_classification, self.item_name_to_id.get(name), self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_names)

    def set_rules(self) -> None:
        self.set_completion_rule(credits_victory())

        set_level_unlock_rules(self)
        set_wishing_engine_rules(self)
        set_character_clear_rules(self)

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        name_to_pandemonium_code = {item.name: item.p_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():
            if location.address is None:
                continue

            if location.item.player == self.player:
                # we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_pandemonium_code[location.item.name])

            if location.player == self.player:
                # we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].p_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_pandemonium_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "goal": self.options.goal.value,
                "deathlink": self.options.deathlink.value,
                "multiclear": self.options.multiclear.value,
                "character_option": self.options.character_option.value,
                "starting_characters": self.starting_characters,
                "starting_level": self.options.starting_level.value,
                "starting_keys": self.options.starting_keys.value,
                "starting_levels": self.starting_levels,
                "level_percentage": self.options.level_percentage.value,
                "level_percentage_range": self.options.level_percentage_range.value,
                "level_percentage_max_range": self.options.level_percentage_max_range.value,
                "speed_greed": self.options.speed_greed.value,
                "full_tilt": self.options.full_tilt.value,
                "enemysanity": self.options.enemysanity.value,
                "transformations_in_pool": self.options.transformations_in_pool.value,
                "pointsanity": self.options.pointsanity.value,
                "pointsanity_range": self.options.pointsanity_range.value,
                "spellbook_pages": self.spell_pages_required,
                "max_health_containers": self.options.max_health_containers.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address,
        }

        return slot_data
