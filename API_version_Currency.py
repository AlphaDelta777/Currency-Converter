import json
import time
import functools
import logging
import os
import csv
from abc import ABC, abstractmethod
from typing import Dict, List, Any

#  Setup & Configuration 
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
AVAILABLE_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY"]


class CurrencyError(Exception):
    """Base class for all application-specific exceptions."""


class APIConnectionError(CurrencyError):
    """Raised when the simulated API fails to provide data."""


class ValidationError(CurrencyError):
    """Raised when user input fails validation."""


class PersistenceError(CurrencyError):
    """Raised when file system operations fail."""


def log_performance(func: Any) -> Any:
    """Decorator to measure method execution time."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # info: Using performance counter for high-resolution timing
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start_time
        logging.info("Method '%s' completed in %.6fs.", func.__name__, duration)
        return result

    return wrapper


class APIClient:
    """Singleton providing market data matrix."""

    _instance = None
    # Hardcoded matrix serves as a mock API for demonstration
    MARKET_DATA = {
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
        # info: Singleton implementation ensures only one API connection
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def fetch_rate(self, from_curr: str, to_curr: str) -> float:
        """Retrieves exchange rate from the internal matrix."""
        return self.MARKET_DATA.get(from_curr, {}).get(to_curr, 0.0)

    def get_summary(self, base: str) -> str:
        """Returns a string summary of rates for a given base."""
        data = self.MARKET_DATA.get(base.upper(), {})
        if not data:
            return "Invalid base currency."
        lines = [
            f"1 {base.upper()} = {rate:.4f} {target}" for target, rate in data.items()
        ]
        return "\n".join(lines)


class AdvancedConverter:
    """Handles business logic, analytics, and file persistence."""

    def __init__(self, storage_file: str = "history.json"):
        self.api = APIClient()
        self.storage_file = storage_file

    @log_performance
    def convert(self, amount: float, from_curr: str, to_curr: str) -> float:
        """Performs conversion and records the transaction."""
        # info: Data sanitization using upper() for consistency
        f_curr, t_curr = from_curr.upper(), to_curr.upper()
        if f_curr not in AVAILABLE_CURRENCIES or t_curr not in AVAILABLE_CURRENCIES:
            raise ValidationError(f"Invalid. Choose from: {AVAILABLE_CURRENCIES}")
        rate = self.api.fetch_rate(f_curr, t_curr)
        if rate == 0.0:
            raise APIConnectionError("Unsupported pair.")
        res = round(amount * rate, 2)
        self._record_transaction(amount, f_curr, t_curr, res)
        return res

    def _record_transaction(
        self, amount: float, from_curr: str, to_curr: str, res: float
    ) -> None:
        """Appends transaction to the JSON log."""
        # info: Using append mode to ensure we don't overwrite previous logs
        try:
            with open(self.storage_file, "a", encoding="utf-8") as file:
                json.dump(
                    {"from": from_curr, "to": to_curr, "amt": amount, "res": res}, file
                )
                file.write("\n")
        except IOError as err:
            raise PersistenceError(f"I/O error: {err}") from err

    def get_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Parses the history log file safely."""
        # info: Fault-tolerant parsing skips malformed lines instead of crashing
        history = []
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as file:
                for line in file:
                    try:
                        if line.strip():
                            history.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return history[-limit:]


class ConsoleUI:
    """Handles CLI user interaction."""

    def __init__(self, converter: AdvancedConverter):
        self.converter = converter

    def run(self) -> None:
        """Main event loop with user guidance."""
        while True:
            print("\n--- ENTERPRISE SYSTEM ---")
            print("1. Snapshot | 2. Convert | 3. History | 4. Exit")
            cmd = input("> ")
            if cmd == "1":
                # info: Prompting guide to ensure user types valid codes
                print(f"Guide: {', '.join(AVAILABLE_CURRENCIES)}")
                base = input("Select Base: ")
                print(self.converter.api.get_summary(base))
            elif cmd == "2":
                print(f"Guide: {', '.join(AVAILABLE_CURRENCIES)}")
                try:
                    amt = float(input("Amount: "))
                    f_c = input("From: ")
                    t_c = input("To: ")
                    print(f"Result: {self.converter.convert(amt, f_c, t_c)}")
                except (ValueError, ValidationError, APIConnectionError) as exc:
                    print(f"Error: {exc}")
            elif cmd == "3":
                print(f"Recent: {self.converter.get_history()}")
            elif cmd == "4":
                break


if __name__ == "__main__":
    ConsoleUI(AdvancedConverter()).run()
