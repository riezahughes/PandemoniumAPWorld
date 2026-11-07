from . import PandemoniumTestBase


class TestStartAsFargus(PandemoniumTestBase):
    options = {"character_option": "fargus"}

    def test_only_nikki_in_pool(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Nikki Unlock")), 1)
        self.assertEqual(len(self.get_items_by_name("Fargus Unlock")), 0)


class TestStartAsNikki(PandemoniumTestBase):
    options = {"character_option": "nikki"}

    def test_only_fargus_in_pool(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Fargus Unlock")), 1)
        self.assertEqual(len(self.get_items_by_name("Nikki Unlock")), 0)


class TestStartAsBoth(PandemoniumTestBase):
    options = {"character_option": "both"}

    def test_no_characters_in_pool(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Fargus Unlock")), 0)
        self.assertEqual(len(self.get_items_by_name("Nikki Unlock")), 0)
