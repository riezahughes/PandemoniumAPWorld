from . import PandemoniumTestBase


class TestSlotDataOptions(PandemoniumTestBase):
    options = {"level_percentage": "true", "level_percentage_range": 25, "full_tilt": "false", "speed_greed": "true", "enemysanity": "true"}

    def test_client_option_keys(self) -> None:
        # the client reads these keys by name, so renaming one here means updating the client too
        options = self.world.fill_slot_data()["options"]
        self.assertEqual(
            set(options),
            {
                "goal", "deathlink", "multiclear", "character_option", "starting_characters",
                "starting_level", "starting_keys", "starting_levels", "level_percentage", "level_percentage_range", "level_percentage_max_range", "speed_greed", "full_tilt",
                "enemysanity", "transformations_in_pool", "pointsanity", "pointsanity_range", "spellbook_pages", "max_health_containers",
            },
        )
        self.assertEqual(options["level_percentage"], 1)
        self.assertEqual(options["level_percentage_range"], 25)
        self.assertEqual(options["full_tilt"], 0)
        self.assertEqual(options["speed_greed"], 1)
        self.assertEqual(options["enemysanity"], 1)
