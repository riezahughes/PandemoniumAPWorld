from typing import TYPE_CHECKING

from rule_builder.rules import CanReachLocation, Has, Rule

from .Options import GoalOptions

if TYPE_CHECKING:
    from . import PandemoniumWorld


def cleared(world: "PandemoniumWorld", level: str) -> Rule:
    # With per-character clears there is no single "Level Cleared" location, so either character's clear counts
    if world.options.multiclear.value:
        return CanReachLocation(f"Fargus Cleared: {level}") | CanReachLocation(f"Nikki Cleared: {level}")
    return CanReachLocation(f"Level Cleared: {level}")


def playable(character: str) -> Rule:
    # Starting characters have their unlock given at the start, so this holds for them too
    return Has(f"{character} Unlock")


def unlocked(level: str) -> Rule:
    return Has(f"{level} Unlock")


def set_level_unlock_rules(self: "PandemoniumWorld") -> None:
    # Every level on the map needs its own unlock item to enter, except The Wishing Engine
    for entrance in self.get_region("Map").exits:
        if entrance.connected_region.name == "The Wishing Engine":
            continue
        self.set_rule(entrance, unlocked(entrance.connected_region.name))


def set_wishing_engine_rules(self: "PandemoniumWorld") -> None:
    bosses = cleared(self, "Shroom Lord") & cleared(self, "Goon Honcho")
    spell_pages = Has("Spellbook Page", count=self.spell_pages_required)

    if self.options.goal.value == GoalOptions.SPELL_PAGES:
        rule = spell_pages
    elif self.options.goal.value == GoalOptions.BOTH:
        rule = bosses & spell_pages
    else:
        rule = bosses

    self.set_rule(self.get_entrance("Map -> The Wishing Engine"), rule)


def set_character_clear_rules(self: "PandemoniumWorld") -> None:
    # A per-character clear needs that character's unlock
    if not self.options.multiclear.value:
        return

    for location in self.multiworld.get_locations(self.player):
        for character in ("Fargus", "Nikki"):
            if location.name.startswith(f"{character} Cleared: "):
                self.set_rule(location, playable(character))
