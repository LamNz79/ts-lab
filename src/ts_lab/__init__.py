"""Reusable time-series code (loaders, metrics, models) shared by notebooks and, later, the Telegram bot."""
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
