"""Survey recodes and fixed, pre-collection quality rules."""

RULES_VERSION = "1.0.0"
DURATION_COLUMN = "Duration (in seconds)"
SOURCE_LABELS = {
    1: "Albert catalog",
    2: "Syllabi",
    3: "Academic advisor",
    4: "Upperclassmen or peers",
    5: "Student group chats",
    6: "Course-review sites",
    7: "Professor's own page",
    8: "Other",
}
CAMPUS_LABELS = {1: "NYU Shanghai", 2: "NYU Abu Dhabi", 3: "Another NYU global site"}
HOURS_LABELS = {1: "0–2", 2: "3–5", 3: "6–10", 4: "11–20", 5: "More than 20"}

# (inclusive minimum, inclusive maximum, integer required)
NUMERIC_RULES = {
    "Finished": (0, 1, True),
    DURATION_COLUMN: (0, float("inf"), False),
    "C0": (1, 2, True),
    "S1": (1, 2, True),
    "S2": (1, 3, True),
    "B1": (1, 4, True),
    "B2": (1, 6, True),
    "B3": (1, 2, True),
    "B4": (0, 24, False),
    "P1": (1, 5, True),
    "P3": (1, 8, True),
    "P4": (1, 4, True),
    "P5": (1, 5, True),
    "O1": (1, 5, True),
    "O2": (1, 3, True),
    "O3": (0, 10, True),
    "A1_1": (1, 5, True),
    "A1_2": (1, 5, True),
    "A1_3": (1, 5, True),
    "A1_4": (1, 5, True),
}
CANONICAL_COLUMNS = (
    "ResponseId",
    "Finished",
    "Status",
    DURATION_COLUMN,
    "C0",
    "S1",
    "S2",
    "B1",
    "B2",
    "B3",
    "B4",
    "P1",
    "P2",
    "P3",
    "P4",
    "P5",
    "O1",
    "O2",
    "O3",
    "A1_1",
    "A1_2",
    "A1_3",
    "A1_4",
)
REQUIRED_COLUMNS = tuple(name for name in CANONICAL_COLUMNS if name != "Status")
MATRIX_COLUMNS = ("A1_1", "A1_2", "A1_3", "A1_4")
DISPOSITION_PRIORITY = (
    "preview_test",
    "not_consented",
    "ineligible",
    "incomplete",
    "quarantined",
    "possible_dupe",
    "failed_attention",
    "speeder",
    "straightline",
    "logic_error",
)


def validate_columns(columns: object) -> None:
    """Fail for an incompatible instrument instead of silently guessing its mapping."""
    missing = sorted(set(REQUIRED_COLUMNS) - set(columns))
    if missing:
        raise ValueError(
            "Missing required survey columns: "
            + ", ".join(missing)
            + ". Use the documented Qualtrics export tags and export numeric values."
        )
