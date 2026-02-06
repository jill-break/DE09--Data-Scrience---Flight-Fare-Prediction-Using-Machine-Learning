"""
Data loading utilities for Flight Fare Prediction project.
"""

import pandas as pd
from pathlib import Path


def load_flight_data(
    data_path: str = "../data/01-raw/Flight_Price_Dataset_of_Bangladesh.csv",
) -> pd.DataFrame:
    """
    Load the flight price dataset.

    Args:
        data_path: Path to the CSV file

    Returns:
        DataFrame containing flight data

    Raises:
        FileNotFoundError: If dataset file doesn't exist
    """
    path = Path(data_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    df = pd.read_csv(path)

    print("Dataset loaded successfully!")
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    return df


def display_basic_info(df: pd.DataFrame) -> None:
    """Display basic dataset information."""
    print("Dataset Information:")
    df.info()

    print("\nColumn Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")
