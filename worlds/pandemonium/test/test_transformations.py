from . import PandemoniumTestBase

TRANSFORMATIONS = {f"{form} Transformation Unlock" for form in ("Frog", "Rhino", "Dragon", "Turtle")}


def pool_item_names(test: PandemoniumTestBase) -> list[str]:
    return [item.name for item in test.multiworld.itempool if item.player == test.player]


class TestTransformationsInPool(PandemoniumTestBase):
    options = {"transformations_in_pool": "true"}

    def test_all_transformations_in_pool(self) -> None:
        names = pool_item_names(self)
        for transformation in TRANSFORMATIONS:
            self.assertEqual(names.count(transformation), 1, transformation)


class TestTransformationsNotInPool(PandemoniumTestBase):
    options = {"transformations_in_pool": "false"}

    def test_no_transformations_in_pool(self) -> None:
        self.assertFalse(TRANSFORMATIONS & set(pool_item_names(self)))

    def test_pool_still_fills_every_location(self) -> None:
        unfilled = [location for location in self.multiworld.get_unfilled_locations(self.player) if location.address is not None]
        self.assertEqual(len(pool_item_names(self)), len(unfilled))
