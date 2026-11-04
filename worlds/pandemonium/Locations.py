from enum import IntEnum
from typing import Optional, NamedTuple, Dict
from BaseClasses import Location, Region
from .Items import PandemoniumItem


class PandemoniumLocationCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    EVENT = 2


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
            "Level 1",
            "Boss",
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
    "Level 1": [
        PandemoniumLocationData("Fake Location", "Fake Item", PandemoniumLocationCategory.PROGRESSION),
    ],
    "Boss": [
        PandemoniumLocationData("Cleared: Boss", "Victory", PandemoniumLocationCategory.EVENT),
    ],
}

location_dictionary: Dict[str, PandemoniumLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
