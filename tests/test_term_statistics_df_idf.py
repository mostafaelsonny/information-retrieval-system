import pytest
from src.statistics.term_statistics import calculate_df, calculate_idf

# Mock positional index based on the Business dataset example
def mock_positional_index():
    return {
        "customer": {"d1": [1], "d2": [1], "d3": [1], "d4": [1], "d5": [1], "d6": [1], "d7": [1]},
        "service":  {"d1": [1], "d2": [1], "d3": [1], "d4": [1]},
        "sales":    {"d1": [1], "d2": [1], "d3": [1], "d4": [1]},
        "growth":   {"d1": [1], "d2": [1], "d3": [1], "d4": [1]},
        "improves": {"d1": [1], "d2": [1], "d3": [1], "d4": [1], "d5": [1]},
    }


def test_df_and_idf():
    df = calculate_df(mock_positional_index())
    assert df["customer"] == 7
    assert df["service"] == 4
    assert df["sales"] == 4
    assert df["growth"] == 4
    assert df["improves"] == 5

    idf = calculate_idf(df, total_documents=10)
    # round to 4 decimal places for comparison
    assert round(idf["customer"], 4) == 0.1549
    assert round(idf["service"], 4) == 0.3979
    assert round(idf["sales"], 4) == 0.3979
    assert round(idf["growth"], 4) == 0.3979
    assert round(idf["improves"], 4) == 0.3010
