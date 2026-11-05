from rule_builder.rules import Has, Rule


def credits_victory() -> Rule:
    return Has("Credits")
