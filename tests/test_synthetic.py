"""Synthetic demonstrations stay reproducible and visibly distinct from responses."""

import pandas as pd
import pytest

from picking_classes_blind.cleaning import clean_responses
from picking_classes_blind.synthetic import make_synthetic


def test_generation_is_reproducible_and_all_rows_are_clearly_synthetic():
    first = make_synthetic()
    pd.testing.assert_frame_equal(first, make_synthetic())
    assert len(first) == 60
    assert first["ResponseId"].str.startswith("SYN_").all()
    assert not first.equals(make_synthetic(seed=7))


def test_demo_injects_one_exclusive_example_of_each_exclusion():
    result = clean_responses(make_synthetic())
    assert result.qa["analysis_rows"] == 50
    assert result.qa["excluded_rows"] == 10
    assert result.qa["disposition_counts"] == {
        "preview_test": 1,
        "not_consented": 1,
        "ineligible": 1,
        "incomplete": 1,
        "quarantined": 1,
        "possible_dupe": 1,
        "failed_attention": 1,
        "speeder": 1,
        "straightline": 1,
        "logic_error": 1,
        "analysis": 50,
    }


def test_demo_accepts_custom_size_at_least_twelve_and_rejects_smaller():
    assert len(make_synthetic(n=12)) == 12
    assert clean_responses(make_synthetic(n=12)).qa["analysis_rows"] == 2
    with pytest.raises(ValueError, match="12"):
        make_synthetic(n=11)
