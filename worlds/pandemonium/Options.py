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
    !! DOES NOT WORK. CANNOT FIGURE OUT HOW TO CHANGE CHARACTERS YET. THE OPTIONS HERE GENERATE CORRECTLY THOUGH. LEAVE IT AS BOTH
    """

    display_name = "Starting Character"
    default = CharacterOptions.BOTH
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
    How many percent of a level must be completed between each check. Boss levels have no percentage checks.
    A check is given at every multiple of this number, plus one at the level's maximum if the multiples don't land on it.
    The maximum is 100%, or the Level Percentage Max Range if that is lower.
    EG: 25 gives 4 checks per level (25, 50, 75, 100), 30 gives 4 checks per level (30, 60, 90, 100),
    60 gives 2 checks per level (60, 100), and 100 gives 1 check per level
    Note: stage 10, 11 and 17 are impossible to get 100% on, so it will max out at 95%.
    """

    display_name = "Level Percentage Break Point"
    range_start = 1
    range_end = 100
    default = 20


class LevelPercentageMaxRange(Range):
    """
    The highest percentage of a level that gives a check. Boss levels have no percentage checks.
    EG: a break point of 10 with a max range of 60 gives checks at 10, 20, 30, 40, 50 and 60.
    Levels that can't reach 100% (stage 10, 11 and 17 max out at 95%) never go above their own maximum.
    If the break point doesn't land on this number, a final check is given at the max range.
    """

    display_name = "Level Percentage Max Range"
    range_start = 1
    range_end = 100
    default = 80


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


class TransformationsInPoolOption(Toggle):
    """If enabled, the Frog, Rhino, Dragon and Turtle transformation unlocks are shuffled into the item pool.
    If disabled, they are not in the pool.
    !!! DOES NOT WORK YET. I CANT CHANGE IT IN THE GAME CORRECTLY. LEAVE IT AS OFF.
    """

    display_name = "Transformations in Pool"
    default = 0
    option_true = 1
    option_false = 0


class EnemySanityOption(Toggle):
    """If enabled, defeating each tracked enemy in a level gives a check. Boss levels have no enemy checks."""

    display_name = "EnemySanity"
    default = 1
    option_true = 1
    option_false = 0


class PointSanityOption(Toggle):
    """If enabled, each level gives checks as you collect its treasure points. Boss levels have no point checks."""

    display_name = "Pointsanity"
    default = 1
    option_true = 1
    option_false = 0


class PointSanityRange(Range):
    """
    If Pointsanity is on, how many treasure points between each check.
    A check is given at every multiple of this number, plus one at the level's maximum if the multiples don't land on it.
    Levels 1 to 4 have 150 points, levels 5 to 12 have 250 and levels 13 to 18 have 350 (boss levels aren't counted).
    EG: 50 gives 50, 100 and 150 in the first four levels, and 50 to 350 in steps of 50 in the last six.
    """

    display_name = "Pointsanity Break Point"
    range_start = 1
    range_end = 350
    default = 50


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


class MaxHealthContainers(Range):
    """
    How many Progressive Health Upgrades are in the game. Each one adds a heart container.
    More containers makes the game easier. If there isn't room for them all in the item pool, the rest are given at the start.
    """

    display_name = "Max Health Containers"
    range_start = 1
    range_end = 16
    default = 5


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
    level_percentage_max_range: LevelPercentageMaxRange
    speed_greed: IncludeSpeedGreedOption
    full_tilt: IncludeFullTiltOption
    enemysanity: EnemySanityOption
    transformations_in_pool: TransformationsInPoolOption
    pointsanity: PointSanityOption
    pointsanity_range: PointSanityRange
    spellbook_pages: SpellbookPageRange
    max_health_containers: MaxHealthContainers
