from . import PandemoniumTestBase
from .. import random_starting_levels


def starting_unlocks(test: PandemoniumTestBase) -> list[str]:
    return [item.name for item in test.multiworld.precollected_items[test.player] if item.name.endswith(" Unlock") and item.name.removesuffix(" Unlock") in random_starting_levels]


class TestProgressiveOneKey(PandemoniumTestBase):
    options = {"starting_level": "progressive", "starting_keys": 1}

    def test_skull_fortress_unlocked_at_start(self) -> None:
        self.assertEqual(self.world.starting_levels, ["Skull Fortress"])
        self.assertEqual(starting_unlocks(self), ["Skull Fortress Unlock"])
        self.assertTrue(self.can_reach_region("Skull Fortress"))
        self.assertEqual(len(self.get_items_by_name("Skull Fortress Unlock")), 0)

    def test_other_levels_locked(self) -> None:
        self.assertFalse(self.can_reach_region("Hollow Stairway"))
        self.collect_by_name("Hollow Stairway Unlock")
        self.assertTrue(self.can_reach_region("Hollow Stairway"))


class TestProgressiveThreeKeys(PandemoniumTestBase):
    options = {"starting_level": "progressive", "starting_keys": 3}

    def test_first_three_levels_unlocked(self) -> None:
        expected = ["Skull Fortress", "Hollow Stairway", "Dungeon Tower"]
        self.assertEqual(self.world.starting_levels, expected)
        self.assertEqual(sorted(starting_unlocks(self)), sorted(f"{level} Unlock" for level in expected))
        for level in expected:
            self.assertTrue(self.can_reach_region(level))
            self.assertEqual(len(self.get_items_by_name(f"{level} Unlock")), 0)
        self.assertFalse(self.can_reach_region("Lost Caves"))


class TestProgressiveMaxKeys(PandemoniumTestBase):
    options = {"starting_level": "progressive", "starting_keys": 13}

    def test_first_thirteen_levels_unlocked(self) -> None:
        self.assertEqual(self.world.starting_levels, random_starting_levels[:13])
        self.assertTrue(self.can_reach_region("Honcho's Logmill"))
        self.assertFalse(self.can_reach_region("Goon Honcho"))


class TestRandomFiveKeys(PandemoniumTestBase):
    options = {"starting_level": "random_level", "starting_keys": 5}

    def test_five_different_levels_unlocked(self) -> None:
        levels = self.world.starting_levels
        self.assertEqual(len(levels), 5)
        self.assertEqual(len(set(levels)), 5)
        self.assertNotIn("The Wishing Engine", levels)
        for level in levels:
            self.assertIn(level, random_starting_levels)
            self.assertTrue(self.can_reach_region(level))
            self.assertEqual(len(self.get_items_by_name(f"{level} Unlock")), 0)
        self.assertEqual(len(starting_unlocks(self)), 5)
