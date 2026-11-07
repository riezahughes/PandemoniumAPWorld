from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions


class GoalOptions:
    DEFEAT_FINAL_BOSS = 0
    SPELL_PAGES = 1
    BOTH = 2


class CharacterOptions:
    FARGUS = 0
    NIKKI = 1
    BOTH = 2
    RANDOM_CHARACTER = 3


class StartingLevelOptions:
    RANDOM_LEVEL = 0
    PROGRESSIVE = 1


class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""

    display_name = "Guaranteed Items"


class CharacterOption(Choice):
    """Lets the user choose what character to start the game with. The other will be put into the item pool.
    Fargus - Start the game with Fargus
    Nikki - Start the game with Nikki
    Both - Start the game with both characters unlocked
    Random Character - Start the game with either Fargus or Nikki, picked at random
    """

    display_name = "Starting Character"
    default = CharacterOptions.FARGUS
    option_fargus = CharacterOptions.FARGUS
    option_nikki = CharacterOptions.NIKKI
    option_both = CharacterOptions.BOTH
    option_random_character = CharacterOptions.RANDOM_CHARACTER


class LevelClearBothCharactersOption(Toggle):
    """If enabled, each characters will have individual level clear checks."""

    display_name = "Level Clear Requires Both Characters"
    default = 1
    option_true = 1
    option_false = 0


class LevelPercentageOption(Toggle):
    """If enabled, Each level will give you a check at the end based on percentage complete."""

    display_name = "Include Level Percentage Checks"
    default = 1
    option_true = 1
    option_false = 0


class LevelPercentageRange(Range):
    """
    How much percentage of the level must be completed to get a check. Boss levels have no percentage checks.
    A check is given at every multiple of this number, plus one at 100% if the multiples don't land on it.
    EG: 25 gives 4 checks per level (25, 50, 75, 100), 30 gives 4 checks per level (30, 60, 90, 100),
    60 gives 2 checks per level (60, 100), and 100 gives 1 check per level
    Note: stage 10, 11 and 17 are impossible to get 100% on, so it will max out at 95%.
    """

    display_name = "Level Completion Percentage for Checks"
    range_start = 1
    range_end = 100
    default = 20


class IncludeSpeedGreedOption(Toggle):
    """If enabled, the Speed Greed checks will be included"""

    display_name = "Include Speed Greed Checks"
    default = 1
    option_true = 1
    option_false = 0


class IncludeFullTiltOption(Toggle):
    """If enabled, the Full Tilt checks will be included"""

    display_name = "Include Full Tilt Checks"
    default = 1
    option_true = 1
    option_false = 0


class EnemySanityOption(Toggle):
    """If enabled, defeating each tracked enemy in a level gives a check. Boss levels have no enemy checks."""

    display_name = "EnemySanity"
    default = 1
    option_true = 1
    option_false = 0


class GoalOption(Choice):
    """Lets the user choose the completion goal
    Defeat Final Boss - find the level unlock and beat the final boss
    Spell Page Hunt - Collect all spell pages in the item pool to unlock the boss
    Both - Collect all parts to unlock the boss, then beat the final boss
    """

    display_name = "Completion Goal"
    default = GoalOptions.DEFEAT_FINAL_BOSS
    option_defeat_final_boss = GoalOptions.DEFEAT_FINAL_BOSS
    option_spell_page_hunt = GoalOptions.SPELL_PAGES
    option_both = GoalOptions.BOTH


class SpellbookPageRange(Range):
    """
    If you've chosen Spell Page Hunt or Both, how many spell pages must be collected to unlock the final boss?
    This many spell pages are added to the item pool. If there isn't room for them all, it is lowered to fit.
    """

    display_name = "Spell Pages Required for Final Boss"
    range_start = 0
    range_end = 100
    default = 20


class StartingLevelOption(Choice):
    """Lets the user choose which level is unlocked at the start of the game
    Random Level - Start with a random level unlocked (never The Wishing Engine)
    Progressive - Start with the first level unlocked and progress through the levels in order
    """

    display_name = "Starting Level"
    default = StartingLevelOptions.RANDOM_LEVEL
    option_progressive = StartingLevelOptions.PROGRESSIVE
    option_random_level = StartingLevelOptions.RANDOM_LEVEL


class RandomStartingKeys(Range):
    """
    How many keys should be given to the player at the start of a game?
    If Random, it'll be x number of keys for any levels.
    If Progressive, It'll be keys for level 1 onwards
    """

    display_name = "Starting Keys"
    range_start = 1
    range_end = 13
    default = 1


class DeathLinkToggle(Toggle):
    """Sets if you want deathlink or not"""

    display_name = "Death Link"
    default = 0
    option_true = 1
    option_false = 0


@dataclass
class PandemoniumOption(PerGameCommonOptions):
    goal: GoalOption
    deathlink: DeathLinkToggle
    multiclear: LevelClearBothCharactersOption
    character_option: CharacterOption
    starting_level: StartingLevelOption
    starting_keys: RandomStartingKeys
    level_percentage: LevelPercentageOption
    level_percentage_range: LevelPercentageRange
    speed_greed: IncludeSpeedGreedOption
    full_tilt: IncludeFullTiltOption
    enemysanity: EnemySanityOption
    spellbook_pages: SpellbookPageRange
