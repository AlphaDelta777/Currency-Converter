import sys
from unittest.mock import MagicMock

import pytest
from Currency_Converter import (  
    APIClient,
    AdvancedConverter,
    ValidationError,
    build_rate_rows,
    build_history_rows,
)
# ── Streamlit stub
# app.py runs Streamlit calls at import time (st.set_page_config, st.tabs …).
# We replace the 'streamlit' module with a MagicMock before importing app so
# those calls become no-ops. st.tabs must return exactly 3 objects to satisfy
# the tuple-unpacking on line:  tab_convert, tab_snapshot, tab_history = st.tabs(…)
_st_stub = MagicMock()
_st_stub.tabs.return_value = (MagicMock(), MagicMock(), MagicMock())
_st_stub.columns.return_value = (MagicMock(), MagicMock())
sys.modules["streamlit"] = _st_stub




# Fixtures

@pytest.fixture()
def converter(tmp_path):
    """Return an AdvancedConverter that writes history to a temp file."""
    return AdvancedConverter(storage_file=str(tmp_path / "history.json"))


# APIClient

class TestAPIClient:
    """Tests for the singleton exchange-rate client."""

    def test_fetch_rate_known_pair(self):
        """A known currency pair returns a positive rate."""
        rate = APIClient().fetch_rate("USD", "EUR")
        assert rate > 0

    def test_fetch_rate_unknown_pair_returns_zero(self):
        """An unknown pair returns 0.0 instead of raising."""
        rate = APIClient().fetch_rate("USD", "XYZ")
        assert rate == 0.0

    def test_get_all_rates_returns_dict(self):
        """get_all_rates returns a non-empty dict for a valid base."""
        rates = APIClient().get_all_rates("USD")
        assert isinstance(rates, dict)
        assert len(rates) > 0

    def test_singleton_same_instance(self):
        """Two APIClient() calls return the exact same object."""
        assert APIClient() is APIClient()


# AdvancedConverter — convert()

class TestConvert:
    """Tests for the core conversion method."""

    def test_basic_conversion_returns_float(self, converter):
        """Converting a valid pair returns a positive float."""
        result = converter.convert(100, "USD", "EUR")
        assert isinstance(result, float)
        assert result > 0

    def test_result_is_rounded_to_two_decimals(self, converter):
        """The result has at most two decimal places."""
        result = converter.convert(100, "USD", "JPY")
        assert result == round(result, 2)

    def test_same_currency_returns_same_amount(self, converter):
        """Converting USD → USD returns the original amount unchanged."""
        assert converter.convert(50, "USD", "USD") == 50.0

    def test_invalid_currency_raises_validation_error(self, converter):
        """An unrecognised currency code raises ValidationError."""
        with pytest.raises(ValidationError):
            converter.convert(100, "USD", "XYZ")

    def test_lowercase_currency_codes_accepted(self, converter):
        """Lower-case codes are normalised and work correctly."""
        result = converter.convert(100, "usd", "eur")
        assert result > 0


# AdvancedConverter — get_history()

class TestHistory:
    """Tests for history persistence and retrieval."""

    def test_history_saved_after_conversion(self, converter):
        """A conversion is persisted and appears in get_history."""
        converter.convert(200, "GBP", "USD")
        history = converter.get_history()
        assert len(history) == 1
        assert history[0]["from"] == "GBP"
        assert history[0]["to"] == "USD"

    def test_history_empty_when_no_conversions(self, converter):
        """get_history returns an empty list when no conversions exist."""
        assert converter.get_history() == []

    def test_history_limit_respected(self, converter):
        """get_history(limit=2) returns at most 2 records."""
        for _ in range(5):
            converter.convert(10, "USD", "EUR")
        assert len(converter.get_history(limit=2)) == 2


# HTML helpers

class TestHTMLHelpers:
    """Tests for the table-row builder functions."""

    def test_build_rate_rows_contains_currency_code(self):
        """build_rate_rows includes the target currency code in the output."""
        html = build_rate_rows({"EUR": 0.92, "GBP": 0.79})
        assert "EUR" in html
        assert "GBP" in html

    def test_build_history_rows_skips_incomplete_records(self):
        """build_history_rows silently skips records missing 'amt' or 'res'."""
        records = [
            {"from": "USD", "to": "EUR", "amt": 100, "res": 92.0, "rate": 0.92},
            {"from": "USD", "to": "GBP"},  # missing amt/res — should be skipped
        ]
        html = build_history_rows(records)
        assert "92" in html       # valid record was rendered
        assert "GBP" not in html  # incomplete record was skipped
