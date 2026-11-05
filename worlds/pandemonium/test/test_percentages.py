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


def percentage_location_names(test: PandemoniumTestBase, level: str) -> set[str]:
    return {
        location.name
        for location in test.multiworld.get_locations(test.player)
        if location.name.endswith(f"Percent Cleared: {level}")
    }


class TestThirtyPercent(PandemoniumTestBase):
    options = {"levelpercentage": 30}

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

    def test_no_checks_for_bosses(self) -> None:
        self.assertEqual(percentage_location_names(self, "Shroom Lord"), set())
        self.assertEqual(percentage_location_names(self, "Goon Honcho"), set())


class TestHundredPercent(PandemoniumTestBase):
    options = {"levelpercentage": 100}

    def test_one_check_per_level(self) -> None:
        self.assertEqual(percentage_location_names(self, "Storm Temple"), {"100 Percent Cleared: Storm Temple"})


class TestOnePercent(PandemoniumTestBase):
    options = {"levelpercentage": 1}

    def test_hundred_checks_per_level(self) -> None:
        self.assertEqual(len(percentage_location_names(self, "Lost Caves")), 100)
