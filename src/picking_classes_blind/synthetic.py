"""Reproducible synthetic data for engineering demonstrations only."""

from random import Random

import pandas as pd

from .schema import CANONICAL_COLUMNS, DURATION_COLUMN


def make_synthetic(seed: int = 20260913, n: int = 60) -> pd.DataFrame:
    """Create n total rows with exactly 10 injected excluded cases.

    The last ten records cover preview, no consent, ineligible, incomplete,
    quarantine, duplicate, attention, speeding, straightlining and logic error,
    respectively. The duplicate repeats the first synthetic ID. Default n=60
    therefore yields 50 analysis rows and 10 exclusive exclusions. Eligible
    outcomes and hours are balanced, while campus outcome cells are deliberately
    small, so the default demo exercises both release and withholding. Source
    subsets are uniformly sampled at each random size (2-5); most-useful is
    sampled uniformly from each selected subset. None are evidence about students.
    """
    if isinstance(n, bool) or not isinstance(n, int) or n < 12:
        raise ValueError("Synthetic demo size n must be an integer of at least 12.")
    rng = Random(seed)
    rows = []
    for index in range(n):
        sources = sorted(rng.sample(range(1, 9), rng.randint(2, 5)))
        rows.append(
            {
                "ResponseId": f"SYN_{index + 1:04d}",
                "Finished": 1,
                "Status": 0,
                DURATION_COLUMN: rng.randint(100, 360),
                "C0": 1,
                "S1": 1,
                "S2": rng.randint(1, 3),
                "B1": rng.randint(1, 4),
                "B2": rng.randint(1, 6),
                "B3": rng.randint(1, 2),
                "B4": rng.choice([12, 14, 16, 18, 20]),
                "P1": rng.randint(1, 5),
                "P2": ",".join(map(str, sources)),
                "P3": rng.choice(sources),
                "P4": rng.randint(1, 4),
                "P5": rng.randint(1, 5),
                "O1": rng.randint(1, 5),
                "O2": rng.randint(1, 3),
                "O3": rng.randint(0, 10),
                "A1_1": rng.choice([1, 3, 4, 5]),
                "A1_2": rng.randint(1, 5),
                "A1_3": 2,
                "A1_4": rng.randint(1, 5),
            }
        )
    # Engineer the release-rule fixture without changing random source choices
    # or the ten injected exclusions. Every default hours group contains two
    # examples of each satisfaction score; campus cells remain below five.
    for index, row in enumerate(rows[:-10]):
        row.update({"S2": index % 3 + 1, "P1": (index // 5) % 5 + 1, "O1": index % 5 + 1})
    injections = [
        {"Status": 1},
        {"C0": 2},
        {"S1": 2},
        {"Finished": 0},
        {"B4": 25},
        {"ResponseId": rows[0]["ResponseId"]},
        {"A1_3": 1, "A1_1": 4},
        {DURATION_COLUMN: 89},
        {"A1_1": 2, "A1_2": 2, "A1_3": 2, "A1_4": 2},
        {"P2": "1,4", "P3": 8},
    ]
    for row, changes in zip(rows[-10:], injections):
        row.update(changes)
    return pd.DataFrame(rows, columns=CANONICAL_COLUMNS)
