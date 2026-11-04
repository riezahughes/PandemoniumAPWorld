from rule_builder.rules import Rule

from .Rules import cleared


def defeat_boss_victory() -> Rule:
    return cleared("Boss")
