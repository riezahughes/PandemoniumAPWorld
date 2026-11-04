# world/pandemonium/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification

from worlds.AutoWorld import World, WebWorld

from .Items import PandemoniumItem, PandemoniumItemCategory, item_dictionary, item_descriptions, BuildItemPool
from .Locations import PandemoniumLocation, PandemoniumLocationCategory, location_tables, location_dictionary
from .Options import PandemoniumOption
from .Rules import set_boss_rules
from .VictoryConditions import defeat_boss_victory


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

    def generate_early(self):
        self.enabled_location_categories.add(PandemoniumLocationCategory.PROGRESSION)
        self.enabled_location_categories.add(PandemoniumLocationCategory.FILLER)

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}

        list_of_regions = [
            "Menu",
            "Level 1",
            "Boss",
        ]

        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in list_of_regions})

        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", "Level 1")
        create_connection("Level 1", "Boss")

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        for location in location_table:
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
        randomized_location_count = 0
        for location in self.multiworld.get_locations(self.player):
            if not location.locked and location.address is not None:
                randomized_location_count += 1

        # Call BuildItemPool to get a list of item NAMES (strings)
        item_names_to_add = BuildItemPool(randomized_location_count, self.options)

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
        return "Fake Item"  # placeholder until real filler items exist

    def set_rules(self) -> None:
        self.set_completion_rule(defeat_boss_victory())

        set_boss_rules(self)

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
                "deathlink": self.options.deathlink.value,
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
