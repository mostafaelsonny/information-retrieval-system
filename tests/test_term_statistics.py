import pytest
from src.statistics.term_statistics import calculate_raw_tf, calculate_weighted_tf

def test_raw_and_weighted_tf():
    mock_index = {"customer": {"d1": [1], "d2": [1, 4]}}
    raw = calculate_raw_tf(mock_index)
    assert raw["customer"]["d1"] == 1
    assert raw["customer"]["d2"] == 2
    weighted = calculate_weighted_tf(raw)
    assert weighted["customer"]["d1"] == 1.0
    assert round(weighted["customer"]["d2"], 4) == 1.3010
