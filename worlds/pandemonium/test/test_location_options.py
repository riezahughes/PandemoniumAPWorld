from . import PandemoniumTestBase


def location_names(test: PandemoniumTestBase) -> set[str]:
    return {location.name for location in test.multiworld.get_locations(test.player)}


class TestSingleClear(PandemoniumTestBase):
    options = {"multiclear": "false"}

    def test_only_regular_level_clears(self) -> None:
        names = location_names(self)
        self.assertIn("Level Cleared: Skull Fortress", names)
        self.assertNotIn("Fargus Cleared: Skull Fortress", names)
        self.assertNotIn("Nikki Cleared: Skull Fortress", names)


class TestMultiClearStartAsFargus(PandemoniumTestBase):
    options = {"multiclear": "true", "character_option": "fargus", "starting_level": "progressive", "starting_keys": 1}

    def test_only_character_level_clears(self) -> None:
        names = location_names(self)
        self.assertNotIn("Level Cleared: Skull Fortress", names)
        self.assertIn("Fargus Cleared: Skull Fortress", names)
        self.assertIn("Nikki Cleared: Skull Fortress", names)

    def test_nikki_clear_needs_nikki(self) -> None:
        self.assertTrue(self.can_reach_location("Fargus Cleared: Skull Fortress"))
        self.assertFalse(self.can_reach_location("Nikki Cleared: Skull Fortress"))
        self.collect_by_name("Nikki Unlock")
        self.assertTrue(self.can_reach_location("Nikki Cleared: Skull Fortress"))

    def test_wishing_engine_uses_character_clears(self) -> None:
        self.collect_by_name(["Shroom Lord Unlock", "Goon Honcho Unlock"])
        self.assertTrue(self.can_reach_region("The Wishing Engine"))


class TestMultiClearStartAsBoth(PandemoniumTestBase):
    options = {"multiclear": "true", "character_option": "both", "starting_level": "progressive", "starting_keys": 1}

    def test_both_clears_open_from_start(self) -> None:
        self.assertTrue(self.can_reach_location("Fargus Cleared: Skull Fortress"))
        self.assertTrue(self.can_reach_location("Nikki Cleared: Skull Fortress"))


class TestRandomCharacter(PandemoniumTestBase):
    options = {"character_option": "random_character"}

    def test_one_character_at_start_and_the_other_in_pool(self) -> None:
        self.assertEqual(len(self.world.starting_characters), 1)
        other = "Nikki" if self.world.starting_characters[0] == "Fargus" else "Fargus"
        self.assertEqual(len(self.get_items_by_name(f"{other} Unlock")), 1)


class TestChallengesOff(PandemoniumTestBase):
    options = {"full_tilt": "false", "speed_greed": "false", "multiclear": "false"}

    def test_challenge_locations_removed(self) -> None:
        names = location_names(self)
        self.assertFalse(any(name.startswith(("Full Tilt: ", "Speed Greed: ")) for name in names))

    def test_health_upgrades_still_total_default(self) -> None:
        in_pool = len(self.get_items_by_name("Progressive Health Upgrade"))
        at_start = sum(item.name == "Progressive Health Upgrade" for item in self.multiworld.precollected_items[self.player])
        self.assertEqual(in_pool + at_start, 8)


class TestChallengesOn(PandemoniumTestBase):
    options = {"full_tilt": "true", "speed_greed": "false"}

    def test_only_full_tilt_included(self) -> None:
        names = location_names(self)
        self.assertIn("Full Tilt: Skull Fortress", names)
        self.assertNotIn("Speed Greed: Skull Fortress", names)


class TestCharacterClearRules(PandemoniumTestBase):
    options = {"multiclear": "true", "character_option": "both", "starting_level": "progressive", "starting_keys": 1}

    def test_character_clears_require_their_unlock(self) -> None:
        state = self.multiworld.get_all_state(False)
        for character in ("Fargus", "Nikki"):
            location = self.world.get_location(f"{character} Cleared: Skull Fortress")
            state.remove(self.world.create_item(f"{character} Unlock"))
            self.assertFalse(location.access_rule(state), f"{character} clear reachable without {character} Unlock")
            state.collect(self.world.create_item(f"{character} Unlock"))
            self.assertTrue(location.access_rule(state))

    def test_starting_characters_given_as_items(self) -> None:
        start_inventory = {item.name for item in self.multiworld.precollected_items[self.player]}
        self.assertIn("Fargus Unlock", start_inventory)
        self.assertIn("Nikki Unlock", start_inventory)


class TestEnemySanityOff(PandemoniumTestBase):
    options = {"enemysanity": "false"}

    def test_enemy_locations_removed(self) -> None:
        names = location_names(self)
        self.assertFalse(any(name.endswith(" Defeated") for name in names))


class TestEnemySanityOn(PandemoniumTestBase):
    options = {"enemysanity": "true"}

    def test_enemy_locations_included(self) -> None:
        names = location_names(self)
        self.assertIn("Skull Fortress: Part 1 - 1st Enemy Defeated", names)
        self.assertIn("Dragoon Skyfort: Part 1 - Bomb 4 Defeated", names)

    def test_boss_levels_have_no_enemies(self) -> None:
        names = location_names(self)
        self.assertFalse(any(name.startswith(("Shroom Lord: ", "Goon Honcho: ")) and name.endswith(" Defeated") for name in names))
