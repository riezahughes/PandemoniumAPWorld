import unittest

from . import PandemoniumTestBase
from ..Locations import percentage_thresholds


class TestPercentageThresholds(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(percentage_thresholds(30), [30, 60, 90, 100])
        self.assertEqual(percentage_thresholds(60), [60, 100])
        self.assertEqual(percentage_thresholds(25), [25, 50, 75, 100])
        self.assertEqual(percentage_thresholds(33), [33, 66, 99, 100])
        self.assertEqual(percentage_thresholds(100), [100])

    def test_one_percent_gives_every_percentage(self) -> None:
        self.assertEqual(percentage_thresholds(1), list(range(1, 101)))

    def test_count_rounds_up(self) -> None:
        for step in range(1, 101):
            self.assertEqual(len(percentage_thresholds(step)), -(-100 // step), step)

    def test_ninety_five_cap(self) -> None:
        self.assertEqual(percentage_thresholds(20, 95), [20, 40, 60, 80, 95])
        self.assertEqual(percentage_thresholds(25, 95), [25, 50, 75, 95])
        self.assertEqual(percentage_thresholds(95, 95), [95])
        self.assertEqual(percentage_thresholds(100, 95), [95])
        self.assertEqual(percentage_thresholds(1, 95), list(range(1, 96)))


def percentage_location_names(test: PandemoniumTestBase, level: str) -> set[str]:
    return {
        location.name
        for location in test.multiworld.get_locations(test.player)
        if location.name.endswith(f"Percent Cleared: {level}")
    }


class TestThirtyPercent(PandemoniumTestBase):
    options = {"level_percentage": "true", "level_percentage_range": 30}

    def test_four_checks_per_level(self) -> None:
        self.assertEqual(
            percentage_location_names(self, "Skull Fortress"),
            {
                "30 Percent Cleared: Skull Fortress",
                "60 Percent Cleared: Skull Fortress",
                "90 Percent Cleared: Skull Fortress",
                "100 Percent Cleared: Skull Fortress",
            },
        )

    def test_capped_level_ends_at_ninety_five(self) -> None:
        self.assertEqual(
            percentage_location_names(self, "Frozen Cavern"),
            {
                "30 Percent Cleared: Frozen Cavern",
                "60 Percent Cleared: Frozen Cavern",
                "90 Percent Cleared: Frozen Cavern",
                "95 Percent Cleared: Frozen Cavern",
            },
        )

    def test_no_checks_for_bosses(self) -> None:
        self.assertEqual(percentage_location_names(self, "Shroom Lord"), set())
        self.assertEqual(percentage_location_names(self, "Goon Honcho"), set())


class TestHundredPercent(PandemoniumTestBase):
    options = {"level_percentage": "true", "level_percentage_range": 100}

    def test_one_check_per_level(self) -> None:
        self.assertEqual(percentage_location_names(self, "Storm Temple"), {"100 Percent Cleared: Storm Temple"})

    def test_capped_levels_top_out_at_ninety_five(self) -> None:
        for level in ("Canopy Village", "Soldier Barracks", "Frozen Cavern"):
            self.assertEqual(percentage_location_names(self, level), {f"95 Percent Cleared: {level}"})


class TestOnePercent(PandemoniumTestBase):
    options = {"level_percentage": "true", "level_percentage_range": 1}

    def test_hundred_checks_per_level(self) -> None:
        self.assertEqual(len(percentage_location_names(self, "Lost Caves")), 100)

    def test_capped_levels_stop_at_ninety_five(self) -> None:
        for level in ("Canopy Village", "Soldier Barracks", "Frozen Cavern"):
            self.assertEqual(len(percentage_location_names(self, level)), 95)


class TestLevelPercentageOff(PandemoniumTestBase):
    options = {"level_percentage": "false", "level_percentage_range": 20}

    def test_no_percentage_checks(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertFalse(any(" Percent Cleared: " in name for name in names))
