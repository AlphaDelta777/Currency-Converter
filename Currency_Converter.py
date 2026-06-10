import json
import time
import functools
import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Any

import streamlit as st

# ── Page config (must be first Streamlit call)
st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered",
)

# ── Custom CSS — financial-terminal aesthetic
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

.result-card {
    background: #0f1923; border-left: 4px solid #00e5ff;
    border-radius: 4px; padding: 1.4rem 1.8rem; margin: 1.2rem 0;
}
.result-card .label {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem;
    letter-spacing: 0.12em; color: #7a9ab0; text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.result-card .amount {
    font-family: 'IBM Plex Mono', monospace; font-size: 2.4rem;
    font-weight: 600; color: #00e5ff; line-height: 1;
}
.result-card .rate-note {
    font-size: 0.8rem; color: #7a9ab0; margin-top: 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
}
.rate-table, .hist-table {
    width: 100%; border-collapse: collapse;
    font-family: 'IBM Plex Mono', monospace; font-size: 0.88rem;
}
.rate-table th, .hist-table th {
    text-align: left; color: #7a9ab0; font-weight: 600; font-size: 0.72rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 0.4rem 0.8rem; border-bottom: 1px solid #1e2e3a;
}
.rate-table td, .hist-table td {
    padding: 0.45rem 0.8rem; border-bottom: 1px solid #1a2530; color: #cdd9e0;
}
.rate-table tr:hover td, .hist-table tr:hover td { background: #111e28; }
.rate-accent { color: #00e5ff; font-weight: 600; }
.eyebrow {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #7a9ab0; margin-bottom: 0.2rem;
}
.err-box {
    background: #1f0d0d; border-left: 3px solid #ff4c4c; border-radius: 3px;
    padding: 0.8rem 1.1rem; font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem; color: #ff8080;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Setup & Configuration ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
AVAILABLE_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY"]
STORAGE_FILE = "history.json"

CURRENCY_NAMES: Dict[str, str] = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "CHF": "Swiss Franc",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "CNY": "Chinese Yuan",
}


# ── Exceptions ────────────────────────────────────────────────────────────────
class CurrencyError(Exception):
    """Base class for all application-specific exceptions."""


class APIConnectionError(CurrencyError):
    """Raised when the exchange-rate API cannot return a valid rate."""


class ValidationError(CurrencyError):
    """Raised when user input fails validation."""


class PersistenceError(CurrencyError):
    """Raised when file-system operations fail."""


# ── Decorator ─────────────────────────────────────────────────────────────────
def log_performance(func: Any) -> Any:
    """Decorator that logs method execution time."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Inner wrapper that times the decorated function."""
        start = time.perf_counter()
        call_result = func(*args, **kwargs)
        logging.info(
            "Method '%s' completed in %.6fs.",
            func.__name__,
            time.perf_counter() - start,
        )
        return call_result

    return wrapper


# ── API Client (singleton) ────────────────────────────────────────────────────
class APIClient:
    """Singleton providing a hardcoded exchange-rate matrix."""

    _instance = None
    MARKET_DATA: Dict[str, Dict[str, float]] = {
        "USD": {
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 150.2,
            "CHF": 0.91,
            "CAD": 1.36,
            "AUD": 1.52,
            "CNY": 7.24,
        },
        "EUR": {
            "USD": 1.09,
            "GBP": 0.86,
            "JPY": 163.5,
            "CHF": 0.99,
            "CAD": 1.48,
            "AUD": 1.65,
            "CNY": 7.85,
        },
        "GBP": {
            "USD": 1.27,
            "EUR": 1.16,
            "JPY": 190.1,
            "CHF": 1.15,
            "CAD": 1.72,
            "AUD": 1.91,
            "CNY": 9.12,
        },
        "JPY": {
            "USD": 0.0067,
            "EUR": 0.0061,
            "GBP": 0.0053,
            "CHF": 0.0061,
            "CAD": 0.0091,
            "AUD": 0.010,
            "CNY": 0.048,
        },
        "CHF": {
            "USD": 1.10,
            "EUR": 1.01,
            "GBP": 0.87,
            "JPY": 165.0,
            "CAD": 1.49,
            "AUD": 1.67,
            "CNY": 7.90,
        },
        "CAD": {
            "USD": 0.73,
            "EUR": 0.67,
            "GBP": 0.58,
            "JPY": 110.2,
            "CHF": 0.67,
            "AUD": 1.11,
            "CNY": 5.30,
        },
        "AUD": {
            "USD": 0.66,
            "EUR": 0.60,
            "GBP": 0.52,
            "JPY": 99.1,
            "CHF": 0.60,
            "CAD": 0.90,
            "CNY": 4.75,
        },
        "CNY": {
            "USD": 0.14,
            "EUR": 0.13,
            "GBP": 0.11,
            "JPY": 20.8,
            "CHF": 0.13,
            "CAD": 0.19,
            "AUD": 0.21,
        },
    }

    def __new__(cls) -> "APIClient":
        """Return the singleton instance, creating it on first call."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def fetch_rate(self, src: str, dst: str) -> float:
        """Return the exchange rate from *src* to *dst*, or 0.0 if unknown."""
        return self.MARKET_DATA.get(src, {}).get(dst, 0.0)

    def get_all_rates(self, src_base: str) -> Dict[str, float]:
        """Return all rates for *src_base*, or an empty dict if unknown."""
        return self.MARKET_DATA.get(src_base, {})


# ── Transaction record dataclass ──────────────────────────────────────────────
@dataclass
class TransactionRecord:
    """Holds the data for a single conversion transaction."""

    from_currency: str
    to_currency: str
    amount: float
    result: float
    rate: float


# ── Converter ─────────────────────────────────────────────────────────────────
class AdvancedConverter:
    """Handles conversions and JSON-file persistence."""

    def __init__(self, storage_file: str = STORAGE_FILE) -> None:
        """Initialise with an APIClient and a path to the history file."""
        self.api = APIClient()
        self.storage_file = storage_file

    @log_performance
    def convert(self, input_amount: float, src: str, dst: str) -> float:
        """Convert *input_amount* from *src* to *dst* and persist the record."""
        f_curr = src.upper()
        t_curr = dst.upper()
        if f_curr not in AVAILABLE_CURRENCIES or t_curr not in AVAILABLE_CURRENCIES:
            raise ValidationError(
                f"Invalid currency. Choose from: {AVAILABLE_CURRENCIES}"
            )
        if f_curr == t_curr:
            return round(input_amount, 2)
        exchange_rate = self.api.fetch_rate(f_curr, t_curr)
        if exchange_rate == 0.0:
            raise APIConnectionError("Unsupported currency pair.")
        converted = round(input_amount * exchange_rate, 2)
        record = TransactionRecord(
            from_currency=f_curr,
            to_currency=t_curr,
            amount=input_amount,
            result=converted,
            rate=exchange_rate,
        )
        self._record(record)
        return converted

    def _record(self, record: TransactionRecord) -> None:
        """Append a TransactionRecord to the JSON history file."""
        try:
            with open(self.storage_file, "a", encoding="utf-8") as file_handle:
                json.dump(
                    {
                        "from": record.from_currency,
                        "to": record.to_currency,
                        "amt": record.amount,
                        "res": record.result,
                        "rate": record.rate,
                    },
                    file_handle,
                )
                file_handle.write("\n")
        except IOError as err:
            raise PersistenceError(f"I/O error: {err}") from err

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return the last *limit* transactions, most recent first."""
        records: List[Dict[str, Any]] = []
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as file_handle:
                for line in file_handle:
                    try:
                        if line.strip():
                            records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return list(reversed(records[-limit:]))


# ── Helpers for rendering HTML tables ────────────────────────────────────────
def build_rate_rows(rates: Dict[str, float]) -> str:
    """Return HTML <tr> rows for the rate-snapshot table."""
    return "".join(
        f"<tr><td class='rate-accent'>{target}</td>"
        f"<td>{CURRENCY_NAMES[target]}</td>"
        f"<td style='text-align:right'>{rate_val:.4f}</td></tr>"
        for target, rate_val in rates.items()
    )


def build_history_rows(records: List[Dict[str, Any]]) -> str:
    """Return HTML <tr> rows for the history table."""
    return "".join(
        f"<tr>"
        f"<td>{rec.get('from', '—')}</td>"
        f"<td>{rec.get('to', '—')}</td>"
        f"<td style='text-align:right'>{float(rec['amt']):,.2f}</td>"
        f"<td style='text-align:right' class='rate-accent'>{float(rec['res']):,.2f}</td>"
        f"<td style='text-align:right'>{rec.get('rate', '—')}</td>"
        f"</tr>"
        for rec in records
        if "amt" in rec and "res" in rec
    )


# ── Streamlit App ─────────────────────────────────────────────────────────────
def render_convert_tab(app_converter: AdvancedConverter, app_api: APIClient) -> None:
    """Render the Convert tab."""
    st.markdown("#### Enter conversion details")
    col1, col2 = st.columns(2)
    with col1:
        sel_from = st.selectbox(
            "From",
            AVAILABLE_CURRENCIES,
            format_func=lambda c: f"{c} — {CURRENCY_NAMES[c]}",
            key="from_curr",
        )
    with col2:
        to_options = [c for c in AVAILABLE_CURRENCIES if c != sel_from]
        sel_to = st.selectbox(
            "To",
            to_options,
            format_func=lambda c: f"{c} — {CURRENCY_NAMES[c]}",
            key="to_curr",
        )
    sel_amount = st.number_input(
        "Amount", min_value=0.01, value=100.00, step=1.0, format="%.2f"
    )
    if st.button("Convert", type="primary", use_container_width=True):
        try:
            conv_result = app_converter.convert(sel_amount, sel_from, sel_to)
            conv_rate = app_api.fetch_rate(sel_from, sel_to)
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="label">Converted amount</div>
                    <div class="amount">
                        {conv_result:,.2f}
                        <span style="font-size:1.2rem;color:#7a9ab0">{sel_to}</span>
                    </div>
                    <div class="rate-note">
                        1 {sel_from} = {conv_rate:.4f} {sel_to}
                        &nbsp;·&nbsp; {sel_amount:,.2f} {sel_from} input
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except (ValidationError, APIConnectionError) as exc:
            st.markdown(f'<div class="err-box">⚠ {exc}</div>', unsafe_allow_html=True)


def render_snapshot_tab(app_api: APIClient) -> None:
    """Render the Rate Snapshot tab."""
    st.markdown("#### Live rate matrix")
    snap_base = st.selectbox(
        "Base currency",
        AVAILABLE_CURRENCIES,
        format_func=lambda c: f"{c} — {CURRENCY_NAMES[c]}",
        key="snapshot_base",
    )
    rows_html = build_rate_rows(app_api.get_all_rates(snap_base))
    st.markdown(
        f"""
        <table class="rate-table">
            <thead><tr>
                <th>Code</th><th>Currency</th>
                <th style="text-align:right">1 {snap_base} =</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


def render_history_tab(app_converter: AdvancedConverter) -> None:
    """Render the History tab."""
    st.markdown("#### Recent conversions")
    records = app_converter.get_history()
    if not records:
        st.info("No conversions yet. Run a conversion and it will appear here.")
        return
    rows_html = build_history_rows(records)
    st.markdown(
        f"""
        <table class="hist-table">
            <thead><tr>
                <th>From</th><th>To</th>
                <th style="text-align:right">Input</th>
                <th style="text-align:right">Result</th>
                <th style="text-align:right">Rate</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Clear history", type="secondary"):
        if os.path.exists(STORAGE_FILE):
            os.remove(STORAGE_FILE)
        st.rerun()


@st.cache_resource
def get_converter() -> AdvancedConverter:
    """Return a cached AdvancedConverter instance."""
    return AdvancedConverter()


if __name__ == "__main__":
    APP_CONVERTER = get_converter()
    APP_API = APIClient()

    st.markdown('<p class="eyebrow">Enterprise FX</p>', unsafe_allow_html=True)
    st.title("Currency Converter")

    tab_convert, tab_snapshot, tab_history = st.tabs(
        ["Convert", "Rate Snapshot", "History"]
    )
    with tab_convert:
        render_convert_tab(APP_CONVERTER, APP_API)
    with tab_snapshot:
        render_snapshot_tab(APP_API)
    with tab_history:
        render_history_tab(APP_CONVERTER)
