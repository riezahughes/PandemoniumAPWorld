from dataclasses import dataclass
from Options import DeathLink, PerGameCommonOptions


@dataclass
class PandemoniumOption(PerGameCommonOptions):
    deathlink: DeathLink
