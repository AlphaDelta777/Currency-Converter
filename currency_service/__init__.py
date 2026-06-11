"""Enterprise FX Distributed Currency Converter Microservice Package Layer."""

# Explicitly expose the backend main entry point for easy access
from currency_service.app_backend import main as run_backend

__all__ = ["run_backend"]