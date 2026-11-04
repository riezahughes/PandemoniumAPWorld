from typing import TYPE_CHECKING

from rule_builder.rules import CanReachLocation, Has, Rule

if TYPE_CHECKING:
    from . import PandemoniumWorld


def cleared(level: str) -> Rule:
    return CanReachLocation(f"Cleared: {level}")


def set_boss_rules(self: "PandemoniumWorld") -> None:
    self.set_rule(self.get_entrance("Level 1 -> Boss"), Has("Fake Item"))
