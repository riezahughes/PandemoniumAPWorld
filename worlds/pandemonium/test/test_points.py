from . import PandemoniumTestBase
from ..Locations import POINT_MAXIMUMS, percentage_thresholds


def point_location_names(test: PandemoniumTestBase, level: str) -> set[str]:
    return {
        location.name
        for location in test.multiworld.get_locations(test.player)
        if location.name.startswith(f"{level}: ") and location.name.endswith(" Points Collected")
    }


class TestPointMaximums(PandemoniumTestBase):
    def test_level_groups(self) -> None:
        for level in ("Skull Fortress", "Hollow Stairway", "Dungeon Tower", "Lost Caves"):
            self.assertEqual(POINT_MAXIMUMS[level], 150)
        for level in ("Fungus Grotto", "Honcho's Logmill"):
            self.assertEqual(POINT_MAXIMUMS[level], 250)
        for level in ("Honcho's Airship", "Storm Temple"):
            self.assertEqual(POINT_MAXIMUMS[level], 350)
        self.assertNotIn("Shroom Lord", POINT_MAXIMUMS)
        self.assertNotIn("Goon Honcho", POINT_MAXIMUMS)
        self.assertEqual(len(POINT_MAXIMUMS), 18)

    def test_break_points(self) -> None:
        self.assertEqual(percentage_thresholds(50, 150), [50, 100, 150])
        self.assertEqual(percentage_thresholds(100, 250), [100, 200, 250])
        self.assertEqual(percentage_thresholds(200, 150), [150])


class TestPointSanityOff(PandemoniumTestBase):
    options = {"pointsanity": "false"}

    def test_no_point_checks(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertFalse(any(name.endswith(" Points Collected") for name in names))


class TestPointSanityFifty(PandemoniumTestBase):
    options = {"pointsanity": "true", "pointsanity_range": 50}

    def test_break_points_per_level(self) -> None:
        self.assertEqual(point_location_names(self, "Skull Fortress"), {f"Skull Fortress: {n} Points Collected" for n in (50, 100, 150)})
        self.assertEqual(point_location_names(self, "Acid Pools"), {f"Acid Pools: {n} Points Collected" for n in (50, 100, 150, 200, 250)})
        self.assertEqual(point_location_names(self, "Storm Temple"), {f"Storm Temple: {n} Points Collected" for n in range(50, 351, 50)})

    def test_point_checks_are_real_locations(self) -> None:
        # a category missing from enabled_location_categories would turn these into events with no ID
        points = [location for location in self.multiworld.get_locations(self.player) if location.name.endswith(" Points Collected")]
        self.assertTrue(points)
        self.assertTrue(all(location.address is not None for location in points))

    def test_no_point_checks_for_bosses(self) -> None:
        self.assertEqual(point_location_names(self, "Shroom Lord"), set())
        self.assertEqual(point_location_names(self, "Goon Honcho"), set())


class TestPointSanityUneven(PandemoniumTestBase):
    options = {"pointsanity": "true", "pointsanity_range": 100}

    def test_maximum_added_when_multiples_miss_it(self) -> None:
        self.assertEqual(point_location_names(self, "Lost Caves"), {f"Lost Caves: {n} Points Collected" for n in (100, 150)})
        self.assertEqual(point_location_names(self, "Frozen Cavern"), {f"Frozen Cavern: {n} Points Collected" for n in (100, 200, 300, 350)})
