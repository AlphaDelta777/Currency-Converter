"""Streamlit Frontend Client for the Distributed Currency Converter Microservice System."""

import json
import time
import functools
import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Any

import streamlit as st
import requests  # <-- Added for microservice network communication

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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght=400;600&family=IBM+Plex+Sans:wght=400;600&display=swap');

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

# URL endpoint mapping for the backend Flask service
BACKEND_URL = "http://127.0.0.1:8000/api"

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
    """Raised when the backend Flask API cannot connect or returns an error."""


class ValidationError(CurrencyError):
    """Raised when user input fails client or server-side validation."""


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


# ── Distributed Architecture Converter (Microservice Interface Client) ────────
class AdvancedConverter:
    """Communicates with the background Flask REST API service for actions."""

    def __init__(self, backend_url: str = BACKEND_URL) -> None:
        """Initialize with target connection API address."""
        self.backend_url = backend_url

    @log_performance
    def convert(self, input_amount: float, src: str, dst: str) -> Dict[str, Any]:
        """Request transaction calculation and log telemetry via backend API."""
        f_curr = src.upper()
        t_curr = dst.upper()
        
        if f_curr not in AVAILABLE_CURRENCIES or t_curr not in AVAILABLE_CURRENCIES:
            raise ValidationError(
                f"Invalid currency. Choose from: {AVAILABLE_CURRENCIES}"
            )
            
        params = {"source": f_curr, "target": t_curr, "amount": input_amount}
        try:
            response = requests.get(f"{self.backend_url}/convert", params=params, timeout=5)
            response.raise_for_status() # If you use status checks
        except requests.exceptions.RequestException as err:
            raise APIConnectionError(f"Flask Server is Offline: {err}") from err
        except ValueError as exc:
            raise APIConnectionError("Server returned non-JSON response.") from exc

        # DEFENSIVE CHECK: Ensure the server actually sent back JSON
        try:
            payload = response.json()
        except ValueError:
            raise APIConnectionError(f"Server returned non-JSON response (Status Code: {response.status_code}). Is the backend routing correct?")

        if response.status_code != 200:
            error_msg = payload.get("error", "Unknown server fault.")
            raise ValidationError(error_msg)
            
        return payload

    def get_history(self) -> List[Dict[str, Any]]:
        """Retrieve audit history matrix logs streamed from the backend."""
        try:
            response = requests.get(f"{self.backend_url}/history", timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass  # Fail gracefully to keep UI stable if network times out
        return []

    def clear_history_remote(self) -> bool:
        """Trigger backend endpoint to purge local history file data."""
        try:
            response = requests.delete(f"{self.backend_url}/history", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


# ── Helpers for rendering HTML tables ────────────────────────────────────────
def build_rate_rows(base_currency: str) -> str:
    """Dynamically compile snapshot matrix by contacting the backend server."""
    html_buffer = []
    for target in AVAILABLE_CURRENCIES:
        if target == base_currency:
            rate_val = 1.0000
        else:
            try:
                # Query flask endpoint safely for a unit baseline matrix rate
                res = requests.get(f"{BACKEND_URL}/convert", params={"source": base_currency, "target": target, "amount": 1.0}, timeout=2)
                rate_val = res.json().get('rate', 0.0) if res.status_code == 200 else 0.0
            except Exception:
                rate_val = 0.0
                
        html_buffer.append(
            f"<tr><td class='rate-accent'>{target}</td>"
            f"<td>{CURRENCY_NAMES[target]}</td>"
            f"<td style='text-align:right'>{rate_val:.4f}</td></tr>"
        )
    return "".join(html_buffer)


def build_history_rows(records: List[Dict[str, Any]]) -> str:
    """Return HTML <tr> rows for the history table from microservice logs."""
    return "".join(
        f"<tr>"
        f"<td>{rec.get('from', '—')}</td>"
        f"<td>{rec.get('to', '—')}</td>"
        f"<td style='text-align:right'>{float(rec.get('amt', 0)):,.2f}</td>"
        f"<td style='text-align:right' class='rate-accent'>{float(rec.get('res', 0)):,.2f}</td>"
        f"<td style='text-align:right'>{rec.get('rate', '—')}</td>"
        f"</tr>"
        for rec in records
        if "amt" in rec and "res" in rec
    )


# ── Streamlit App Tabs ────────────────────────────────────────────────────────
def render_convert_tab(app_converter: AdvancedConverter) -> None:
    """Render the Convert tab targeting microservice workflows."""
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
            # Query backend service
            payload = app_converter.convert(sel_amount, sel_from, sel_to)
            
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="label">Converted amount (Via Flask API)</div>
                    <div class="amount">
                        {payload['res']:,.2f}
                        <span style="font-size:1.2rem;color:#7a9ab0">{sel_to}</span>
                    </div>
                    <div class="rate-note">
                        1 {sel_from} = {payload['rate']:.4f} {sel_to}
                        &nbsp;·&nbsp; {sel_amount:,.2f} {sel_from} input
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except (ValidationError, APIConnectionError) as exc:
            st.markdown(f'<div class="err-box">⚠ {exc}</div>', unsafe_allow_html=True)


def render_snapshot_tab() -> None:
    """Render the Rate Snapshot tab from cross-sectional network data."""
    st.markdown("#### Live rate matrix")
    snap_base = st.selectbox(
        "Base currency",
        AVAILABLE_CURRENCIES,
        format_func=lambda c: f"{c} — {CURRENCY_NAMES[c]}",
        key="snapshot_base",
    )
    rows_html = build_rate_rows(snap_base)
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
    """Render the History tab sourcing transaction streams from Flask."""
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
        if app_converter.clear_history_remote():
            st.success("Remote ledger cleared successfully.")
            st.rerun()
        else:
            st.error("Could not communicate clear request to server.")


@st.cache_resource
def get_converter() -> AdvancedConverter:
    """Return a cached AdvancedConverter gateway instance."""
    return AdvancedConverter()


# ── System Orchestrator Execution ─────────────────────────────────────────────
if __name__ == "__main__":
    APP_CONVERTER = get_converter()

    st.markdown('<p class="eyebrow">Enterprise FX Distributed Client</p>', unsafe_allow_html=True)
    st.title("Currency Converter")

    tab_convert, tab_snapshot, tab_history = st.tabs(
        ["Convert", "Rate Snapshot", "History"]
    )
    with tab_convert:
        render_convert_tab(APP_CONVERTER)
    with tab_snapshot:
        render_snapshot_tab()
    with tab_history:
        render_history_tab(APP_CONVERTER)