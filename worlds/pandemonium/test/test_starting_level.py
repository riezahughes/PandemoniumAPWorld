from . import PandemoniumTestBase
from .. import random_starting_levels


class TestStartAtSkullFortress(PandemoniumTestBase):
    options = {"startinglevel": "skull_fortress"}

    def test_skull_fortress_unlocked_at_start(self) -> None:
        self.assertEqual(self.world.starting_level, "Skull Fortress")
        self.assertTrue(self.can_reach_region("Skull Fortress"))
        self.assertEqual(len(self.get_items_by_name("Skull Fortress Unlock")), 0)

    def test_other_levels_locked(self) -> None:
        self.assertFalse(self.can_reach_region("Hollow Stairway"))
        self.collect_by_name("Hollow Stairway Unlock")
        self.assertTrue(self.can_reach_region("Hollow Stairway"))


class TestStartAtRandomLevel(PandemoniumTestBase):
    options = {"startinglevel": "random_level"}

    def test_random_level_unlocked_at_start(self) -> None:
        level = self.world.starting_level
        self.assertIn(level, random_starting_levels)
        self.assertNotEqual(level, "The Wishing Engine")
        self.assertTrue(self.can_reach_region(level))
        self.assertEqual(len(self.get_items_by_name(f"{level} Unlock")), 0)
