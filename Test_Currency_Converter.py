import sys
from unittest.mock import MagicMock, patch
import pytest
import requests

# ── Streamlit Stub Execution 
# This prevents Streamlit import errors during automated headless tests.
_st_stub = MagicMock()
_st_stub.tabs.return_value = (MagicMock(), MagicMock(), MagicMock())
_st_stub.columns.return_value = (MagicMock(), MagicMock())
sys.modules["streamlit"] = _st_stub

from Currency_Converter import (  
    AdvancedConverter,
    ValidationError,
    APIConnectionError,
    build_rate_rows,
    build_history_rows,
)

# ── Test Fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture()
def converter():
    """Return an AdvancedConverter configured for a local mock backend environment."""
    return AdvancedConverter(backend_url="http://127.0.0.1:8000/api")


# ── AdvancedConverter — convert() Suite ───────────────────────────────────────

class TestConvert:
    """Tests for the distributed core conversion action."""

    @patch('requests.get')
    def test_basic_conversion_returns_dict_payload(self, mock_get, converter):
        """Converting a valid pair returns a microservice response payload."""
        # Set up a fake successful mock backend JSON response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "from": "USD", "to": "EUR", "amt": 100.0, "res": 92.0, "rate": 0.92
        }
        mock_get.return_value = mock_response

        payload = converter.convert(100, "USD", "EUR")
        
        assert isinstance(payload, dict)
        assert payload["res"] == 92.0
        assert payload["rate"] == 0.92
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_invalid_currency_raises_validation_error(self, mock_get, converter):
        """An unrecognized currency code raises ValidationError before hitting network."""
        with pytest.raises(ValidationError):
            converter.convert(100, "USD", "XYZ")
        
        # Verify it didn't waste time making a network call
        mock_get.assert_not_called()

    @patch('requests.get')
    def test_backend_server_offline_raises_connection_error(self, mock_get, converter):
        """If the Flask server cannot be reached, raise an APIConnectionError."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with pytest.raises(APIConnectionError):
            converter.convert(100, "USD", "EUR")


# ── AdvancedConverter — get_history() Suite ───────────────────────────────────

class TestHistory:
    """Tests for distributed logging synchronization streams."""

    @patch('requests.get')
    def test_history_retrieval_returns_list(self, mock_get, converter):
        """get_history returns a parsed record matrix list from the Flask microservice."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"from": "GBP", "to": "USD", "amt": 200.0, "res": 254.0, "rate": 1.27}
        ]
        mock_get.return_value = mock_response

        history = converter.get_history()
        assert len(history) == 1
        assert history[0]["from"] == "GBP"
        assert history[0]["to"] == "USD"

    @patch('requests.get')
    def test_history_empty_when_backend_fails(self, mock_get, converter):
        """get_history gracefully downgrades to an empty list on server dropout."""
        mock_get.side_effect = requests.exceptions.Timeout("Server timed out")
        assert converter.get_history() == []


# ── HTML Helpers Suite ────────────────────────────────────────────────────────

class TestHTMLHelpers:
    """Tests for the cross-sectional frontend layout table-row configurations."""

    @patch('requests.get')
    def test_build_rate_rows_queries_backend_and_contains_code(self, mock_get):
        """build_rate_rows queries the endpoint baseline and sets layout rows."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rate": 0.92}
        mock_get.return_value = mock_response

        # Pass a base currency to dynamically populate the currency snapshot grid
        html = build_rate_rows("USD")
        
        # Ensure targeted codes from AVAILABLE_CURRENCIES are successfully generated
        assert "EUR" in html
        assert "GBP" in html

    def test_build_history_rows_skips_incomplete_records(self):
        """build_history_rows skips incomplete dictionary ledger structures without crashing."""
        records = [
            {"from": "USD", "to": "EUR", "amt": 100, "res": 92.0, "rate": 0.92},
            {"from": "USD", "to": "GBP"},  # missing 'amt'/'res' keys — must skip safely
        ]
        html = build_history_rows(records)
        assert "92" in html
        assert "GBP" not in html