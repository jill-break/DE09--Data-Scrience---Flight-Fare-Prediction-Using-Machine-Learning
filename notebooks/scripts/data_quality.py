"""
Data quality assessment utilities.
"""

import pandas as pd
from typing import Dict, Any


def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze missing values in the dataset.

    Args:
        df: DataFrame to analyze

    Returns:
        DataFrame with missing value statistics
    """
    print("Missing Values Analysis:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100

    missing_df = pd.DataFrame(
        {"Column": missing.index, "Missing Count": missing.values, "Percentage": missing_pct.values}
    ).sort_values("Missing Count", ascending=False)

    return missing_df[missing_df["Missing Count"] > 0]


def check_duplicates(df: pd.DataFrame) -> Dict[str, int]:
    """
    Check for duplicate rows and flight records.

    Args:
        df: DataFrame to analyze

    Returns:
        Dictionary with duplicate counts
    """
    duplicates = df.duplicated().sum()
    duplicate_flights = df.duplicated(
        subset=["Airline", "Source", "Destination", "Departure Date & Time"]
    ).sum()

    print(f"Duplicate Rows: {duplicates:,} ({duplicates/len(df)*100:.2f}%)")
    print(f"Duplicate Flight Records: {duplicate_flights:,}")

    return {"duplicate_rows": duplicates, "duplicate_flights": duplicate_flights}


def display_data_types(df: pd.DataFrame) -> None:
    """Display data types and unique value counts."""
    print("Data Types and Unique Values:")
    for col in df.columns:
        unique_count = df[col].nunique()
        dtype = df[col].dtype
        print(f"{col:<30} | Type: {str(dtype):<10} | Unique: {unique_count:>6,}")


def verify_fare_calculation(df: pd.DataFrame, tolerance: float = 1.0) -> pd.DataFrame:
    """
    Verify that Total Fare = Base Fare + Tax & Surcharge.

    Args:
        df: DataFrame to check
        tolerance: Maximum allowed difference in BDT

    Returns:
        DataFrame with rows that have mismatches
    """
    df_temp = df.copy()
    df_temp["Calculated Total"] = df_temp["Base Fare (BDT)"] + df_temp["Tax & Surcharge (BDT)"]
    df_temp["Fare Difference"] = abs(df_temp["Total Fare (BDT)"] - df_temp["Calculated Total"])

    mismatches = (df_temp["Fare Difference"] > tolerance).sum()
    print(f"\nFare Calculation Mismatches: {mismatches:,} rows ({mismatches/len(df)*100:.2f}%)")

    if mismatches > 0:
        print("\nSample mismatches:")
        return df_temp[df_temp["Fare Difference"] > tolerance][
            ["Base Fare (BDT)", "Tax & Surcharge (BDT)", "Total Fare (BDT)", "Fare Difference"]
        ].head()

    return pd.DataFrame()


def generate_quality_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate comprehensive data quality summary.

    Args:
        df: DataFrame to analyze

    Returns:
        Dictionary with quality metrics
    """
    print("=" * 60)
    print("DATA QUALITY SUMMARY")
    print("=" * 60)

    print("\nDataset Size:")
    print(f"   Total Records: {len(df):,}")
    print(f"   Total Features: {df.shape[1]}")

    print("\nData Quality:")
    missing_total = df.isnull().sum().sum()
    duplicate_total = df.duplicated().sum()
    print(f"   Missing Values: {missing_total:,}")
    print(f"   Duplicate Rows: {duplicate_total:,}")
    print(f"   Complete Records: {len(df) - df.isnull().any(axis=1).sum():,}")

    print("\nTarget Variable (Total Fare):")
    print(
        f"   Range: {df['Total Fare (BDT)'].min():,.2f} - {df['Total Fare (BDT)'].max():,.2f} BDT"
    )
    print(f"   Mean: {df['Total Fare (BDT)'].mean():,.2f} BDT")
    print(f"   Median: {df['Total Fare (BDT)'].median():,.2f} BDT")
    print(f"   Std Dev: {df['Total Fare (BDT)'].std():,.2f} BDT")

    print("\n" + "=" * 60)

    return {
        "total_rows": len(df),
        "total_columns": df.shape[1],
        "missing_values": missing_total,
        "duplicates": duplicate_total,
        "quality_score": 100 * (1 - (missing_total + duplicate_total) / (len(df) * df.shape[1])),
    }
