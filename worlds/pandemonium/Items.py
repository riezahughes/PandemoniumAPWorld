from enum import IntEnum
from typing import NamedTuple, List, Optional
from BaseClasses import Item, ItemClassification


class PandemoniumItemCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    EVENT = 2


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
    ("Fake Item", 1, PandemoniumItemCategory.PROGRESSION, True),
    # Events (no code, never sent over the network)
    ("Victory", None, PandemoniumItemCategory.EVENT, True),
]
# Convert raw list of tuples into PandemoniumItemData NamedTuple instances
_all_items = [PandemoniumItemData(row[0], row[1], row[2], row[3]) for row in _all_items]


item_descriptions = {
    "Fake Item": "A placeholder item that opens the way to the boss.",
}

# Create a dictionary for quick lookup of item data by name
item_dictionary: dict[str, PandemoniumItemData] = {item_data.name: item_data for item_data in _all_items}


def BuildItemPool(count: int, options) -> List[str]:
    """
    Generates a list of item names to be used for the item pool.
    This function does NOT create Archipelago Item objects; it only provides their names.
    The actual Item objects are created in PandemoniumWorld.create_items.
    """
    item_pool_names: List[str] = [
        item_data.name for item_data in _all_items if item_data.category == PandemoniumItemCategory.PROGRESSION
    ]

    if len(item_pool_names) != count:
        print(f"Warning: Item pool size ({len(item_pool_names)}) does not match location count ({count}).")

    return item_pool_names
