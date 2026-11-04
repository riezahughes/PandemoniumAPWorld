from . import PandemoniumTestBase


class TestDefeatBossVictory(PandemoniumTestBase):
    def test_boss_requires_fake_item(self) -> None:
        self.assertFalse(self.can_reach_location("Cleared: Boss"))
        self.collect_by_name("Fake Item")
        self.assertTrue(self.can_reach_location("Cleared: Boss"))

    def test_victory_requires_fake_item(self) -> None:
        self.assertBeatable(False)
        self.collect_by_name("Fake Item")
        self.assertBeatable(True)
