from . import PandemoniumTestBase
from ..Items import filler_item_names


class TestItemPool(PandemoniumTestBase):
    def test_health_upgrade_count(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Progressive Health Upgrade")), 5)

    def test_filler_is_weapons_and_extra_lives(self) -> None:
        self.assertIn("Extra Life", filler_item_names)
        self.assertIn("Freeze Ray", filler_item_names)
        self.assertNotIn("Progressive Health Upgrade", filler_item_names)


class TestMaxHealthContainers(PandemoniumTestBase):
    options = {"max_health_containers": 16}

    def test_health_upgrade_count_follows_option(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Progressive Health Upgrade")), 16)
