from . import PandemoniumTestBase


class TestCreditsVictory(PandemoniumTestBase):
    def test_credits_locked_at_game_completed(self) -> None:
        location = self.world.get_location("Game Completed")
        self.assertTrue(location.locked)
        self.assertEqual(location.item.name, "Credits")

    def test_victory_requires_credits(self) -> None:
        completion_condition = self.multiworld.completion_condition[self.player]
        self.assertFalse(completion_condition(self.multiworld.state))
        self.collect(self.world.get_location("Game Completed").item)
        self.assertTrue(completion_condition(self.multiworld.state))
