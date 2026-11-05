from . import PandemoniumTestBase


class TestWishingEngine(PandemoniumTestBase):
    options = {"startinglevel": "skull_fortress"}

    def test_game_completed_is_in_wishing_engine(self) -> None:
        self.assertEqual(self.world.get_location("Game Completed").parent_region.name, "The Wishing Engine")

    def test_requires_both_bosses(self) -> None:
        self.assertFalse(self.can_reach_region("The Wishing Engine"))

        self.collect_by_name("Shroom Lord Unlock")
        self.assertFalse(self.can_reach_region("The Wishing Engine"))

        self.collect_by_name("Goon Honcho Unlock")
        self.assertTrue(self.can_reach_region("The Wishing Engine"))
        self.assertTrue(self.can_reach_location("Game Completed"))

    def test_goon_honcho_alone_is_not_enough(self) -> None:
        self.collect_by_name("Goon Honcho Unlock")
        self.assertFalse(self.can_reach_region("The Wishing Engine"))
