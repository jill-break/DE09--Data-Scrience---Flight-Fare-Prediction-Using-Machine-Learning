"""
Quick data summary script for Flight Price Dataset.
Generates a comprehensive report without external dependencies like Pandera.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def generate_data_summary(filepath: str) -> dict:
    """Generate comprehensive data summary."""

    print("\n" + "=" * 70)
    print("FLIGHT PRICE DATASET - DATA SUMMARY REPORT")
    print("=" * 70)

    # Load data
    print(f"\nLoading data from: {filepath}")
    df = pd.read_csv(filepath)
    print("Data loaded successfully!")

    # Basic info
    print(f"\n{'='*70}")
    print("DATASET OVERVIEW")
    print("=" * 70)
    print(f"Total Rows:    {len(df):>15,}")
    print(f"Total Columns: {len(df.columns):>15,}")
    print(f"Memory Usage:  {df.memory_usage(deep=True).sum() / 1024**2:>14,.2f} MB")

    # Columns
    print(f"\n{'='*70}")
    print("COLUMNS")
    print("=" * 70)
    for i, col in enumerate(df.columns, 1):
        dtype = str(df[col].dtype)
        unique = df[col].nunique()
        print(f"{i:2d}. {col:<40} {dtype:<10} (Unique: {unique:>7,})")

    # Missing values
    print(f"\n{'='*70}")
    print("MISSING VALUES")
    print("=" * 70)
    missing = df.isnull().sum()
    total_missing = missing.sum()

    if total_missing > 0:
        for col in missing[missing > 0].index:
            count = missing[col]
            pct = (count / len(df)) * 100
            print(f"   {col:<40} {count:>8,} ({pct:>5.2f}%)")
    else:
        print("   No missing values found!")

    # Duplicates
    print(f"\n{'='*70}")
    print("DUPLICATE ANALYSIS")
    print("=" * 70)
    dup_rows = df.duplicated().sum()
    dup_flights = df.duplicated(
        subset=["Airline", "Source", "Destination", "Departure Date & Time"]
    ).sum()
    print(f"Duplicate Rows:          {dup_rows:>10,} ({dup_rows/len(df)*100:>5.2f}%)")
    print(f"Duplicate Flight Records:{dup_flights:>10,}")

    # Numerical summary
    print(f"\n{'='*70}")
    print("NUMERICAL FEATURES SUMMARY")
    print("=" * 70)

    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        print(f"\n{col}:")
        print(f"   Mean:   {df[col].mean():>15,.2f}")
        print(f"   Median: {df[col].median():>15,.2f}")
        print(f"   Min:    {df[col].min():>15,.2f}")
        print(f"   Max:    {df[col].max():>15,.2f}")
        print(f"   Std:    {df[col].std():>15,.2f}")

    # Categorical summary
    print(f"\n{'='*70}")
    print("CATEGORICAL FEATURES SUMMARY")
    print("=" * 70)

    categorical_cols = ["Airline", "Class", "Stopovers", "Seasonality", "Booking Source"]
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n{col}:")
            value_counts = df[col].value_counts()
            for val, count in value_counts.head(5).items():
                pct = (count / len(df)) * 100
                print(f"   {str(val):<30} {count:>8,} ({pct:>5.2f}%)")
            if len(value_counts) > 5:
                print(f"   ... and {len(value_counts) - 5} more")

    # Business insights
    print(f"\n{'='*70}")
    print("KEY BUSINESS INSIGHTS")
    print("=" * 70)

    # Average fare by airline
    print("\nAverage Fare by Airline (Top 5):")
    airline_fares = (
        df.groupby("Airline")["Total Fare (BDT)"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
        .head(5)
    )
    for i, (airline, row) in enumerate(airline_fares.iterrows(), 1):
        print(f"   {i}. {airline:<30} {row['mean']:>12,.2f} BDT (n={row['count']:,})")

    # Most popular routes
    df["Route"] = df["Source"] + " → " + df["Destination"]
    print("\nMost Popular Routes (Top 5):")
    top_routes = df["Route"].value_counts().head(5)
    for i, (route, count) in enumerate(top_routes.items(), 1):
        avg_fare = df[df["Route"] == route]["Total Fare (BDT)"].mean()
        print(f"   {i}. {route:<30} {count:>6,} flights, Avg: {avg_fare:>10,.2f} BDT")

    # Seasonal impact
    print("\nSeasonal Fare Variation:")
    seasonal = (
        df.groupby("Seasonality")["Total Fare (BDT)"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
    )
    for i, (season, row) in enumerate(seasonal.iterrows(), 1):
        print(f"   {i}. {season:<30} {row['mean']:>12,.2f} BDT (n={row['count']:,})")

    # Class impact
    print("\nClass Impact:")
    class_impact = (
        df.groupby("Class")["Total Fare (BDT)"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
    )
    for i, (cls, row) in enumerate(class_impact.iterrows(), 1):
        print(f"   {i}. {cls:<30} {row['mean']:>12,.2f} BDT (n={row['count']:,})")

    # Data quality score
    print(f"\n{'='*70}")
    print("DATA QUALITY SCORE")
    print("=" * 70)

    completeness = ((len(df) - df.isnull().any(axis=1).sum()) / len(df)) * 100
    uniqueness = (1 - dup_rows / len(df)) * 100
    overall_quality = (completeness + uniqueness) / 2

    print(f"Completeness:  {completeness:>6.2f}%  {'✅' if completeness > 95 else '⚠️'}")
    print(f"Uniqueness:    {uniqueness:>6.2f}%  {'✅' if uniqueness > 95 else '⚠️'}")
    print(f"Overall Score: {overall_quality:>6.2f}%  {'✅' if overall_quality > 90 else '⚠️'}")

    # Recommendations
    print(f"\n{'='*70}")
    print("RECOMMENDATIONS")
    print("=" * 70)

    recommendations = []

    if total_missing > 0:
        recommendations.append("• Handle missing values with appropriate imputation strategy")

    if dup_rows > 0:
        recommendations.append("• Investigate and remove duplicate rows")

    # Check fare calculation
    df["Calculated Total"] = df["Base Fare (BDT)"] + df["Tax & Surcharge (BDT)"]
    fare_mismatches = (abs(df["Total Fare (BDT)"] - df["Calculated Total"]) > 1.0).sum()
    if fare_mismatches > 0:
        recommendations.append(
            f"• Verify {fare_mismatches:,} rows with fare calculation mismatches"
        )

    # Check for outliers
    Q1 = df["Total Fare (BDT)"].quantile(0.25)
    Q3 = df["Total Fare (BDT)"].quantile(0.75)
    IQR = Q3 - Q1
    outliers = (
        (df["Total Fare (BDT)"] < Q1 - 1.5 * IQR) | (df["Total Fare (BDT)"] > Q3 + 1.5 * IQR)
    ).sum()
    if outliers > 0:
        recommendations.append(f"• Investigate {outliers:,} potential outliers in Total Fare")

    recommendations.append("• Create temporal features from date columns")
    recommendations.append("• Encode categorical variables for modeling")
    recommendations.append("• Normalize/scale numerical features")

    if recommendations:
        for rec in recommendations:
            print(f"   {rec}")
    else:
        print("   Data quality is excellent! Ready for modeling.")

    print("\n" + "=" * 70)
    print("DATA SUMMARY COMPLETE!")
    print("=" * 70 + "\n")

    return {
        "shape": df.shape,
        "missing_total": total_missing,
        "duplicates": dup_rows,
        "quality_score": overall_quality,
    }


if __name__ == "__main__":
    filepath = "data/01-raw/Flight_Price_Dataset_of_Bangladesh.csv"

    if not Path(filepath).exists():
        print(f"File not found: {filepath}")
        print("Please ensure the dataset is in the correct location.")
    else:
        summary = generate_data_summary(filepath)

        print("\nNext Steps:")
        print("1. Run the EDA notebook: jupyter notebook notebooks/01_data_exploration.ipynb")
        print("2. Begin preprocessing: Create data cleaning pipeline")
        print("3. Feature engineering: Extract temporal and categorical features")
