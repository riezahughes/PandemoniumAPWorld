from . import PandemoniumTestBase


class TestDefeatFinalBossGoal(PandemoniumTestBase):
    options = {"goal": "defeat_final_boss", "spellpages": 10}

    def test_no_spell_pages_in_pool(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Spell Page")), 0)
        self.assertEqual(self.world.spell_pages_required, 0)


class TestSpellPageHuntGoal(PandemoniumTestBase):
    options = {"goal": "spell_page_hunt", "spellpages": 10, "startinglevel": "skull_fortress"}

    def test_spell_pages_in_pool(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Spell Page")), 10)
        self.assertEqual(self.world.spell_pages_required, 10)

    def test_wishing_engine_needs_only_spell_pages(self) -> None:
        pages = self.get_items_by_name("Spell Page")
        self.collect(pages[:-1])
        self.assertFalse(self.can_reach_region("The Wishing Engine"))
        self.collect(pages[-1])
        self.assertTrue(self.can_reach_region("The Wishing Engine"))


class TestBothGoal(PandemoniumTestBase):
    options = {"goal": "both", "spellpages": 10, "startinglevel": "skull_fortress"}

    def test_spell_pages_in_pool(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Spell Page")), 10)

    def test_wishing_engine_needs_bosses_and_spell_pages(self) -> None:
        self.collect_by_name("Spell Page")
        self.assertFalse(self.can_reach_region("The Wishing Engine"))

        self.collect_by_name(["Shroom Lord Unlock", "Goon Honcho Unlock"])
        self.assertTrue(self.can_reach_region("The Wishing Engine"))

    def test_bosses_alone_are_not_enough(self) -> None:
        self.collect_by_name(["Shroom Lord Unlock", "Goon Honcho Unlock"])
        self.assertFalse(self.can_reach_region("The Wishing Engine"))


class TestTooManySpellPages(PandemoniumTestBase):
    # Keep the location count low so 100 spell pages can't fit
    options = {"goal": "spell_page_hunt", "spellpages": 100, "levelpercentage": 100, "fulltilt": "false", "speedgreed": "false"}

    def test_requirement_lowered_to_fit(self) -> None:
        pages = len(self.get_items_by_name("Spell Page"))
        self.assertLess(pages, 100)
        self.assertEqual(self.world.spell_pages_required, pages)
