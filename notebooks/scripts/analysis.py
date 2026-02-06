"""
Analysis utilities for Flight Fare Prediction project.
"""

import pandas as pd
from typing import Any, Dict


def analyze_categorical_variable(df: pd.DataFrame, column: str, top_n: int = 10) -> None:
    """
    Analyze a categorical variable.

    Args:
        df: DataFrame containing the data
        column: Column name to analyze
        top_n: Number of top categories to display
    """
    print(f"\n{column} Distribution:")
    value_counts = df[column].value_counts()

    if len(value_counts) <= top_n:
        print(value_counts)
    else:
        print(value_counts.head(top_n))
        print(f"... and {len(value_counts) - top_n} more")


def analyze_fare_by_category(
    df: pd.DataFrame, category_col: str, fare_col: str = "Total Fare (BDT)", top_n: int = 5
) -> pd.DataFrame:
    """
    Analyze average fares by category.

    Args:
        df: DataFrame containing the data
        category_col: Column to group by
        fare_col: Fare column name
        top_n: Number of top categories to show

    Returns:
        DataFrame with aggregated statistics
    """
    stats = (
        df.groupby(category_col)[fare_col]
        .agg(["mean", "median", "count"])
        .sort_values("mean", ascending=False)
    )

    print(f"\nAverage {fare_col} by {category_col} (Top {top_n}):")
    print(stats.head(top_n))

    return stats


def create_route_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create route feature from source and destination.

    Args:
        df: DataFrame containing the data

    Returns:
        DataFrame with new Route column
    """
    df_copy = df.copy()
    df_copy["Route"] = df_copy["Source"] + " → " + df_copy["Destination"]
    return df_copy


def analyze_routes(df: pd.DataFrame, top_n: int = 10) -> Dict[str, pd.Series]:
    """
    Analyze most popular and expensive routes.

    Args:
        df: DataFrame with Route column
        top_n: Number of routes to show

    Returns:
        Dictionary with popular and expensive routes
    """
    # Most popular routes
    print(f"\nTop {top_n} Most Popular Routes:")
    popular = df["Route"].value_counts().head(top_n)
    print(popular)

    # Most expensive routes (minimum flights filter)
    route_fares = (
        df.groupby("Route")["Total Fare (BDT)"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
    )
    expensive = route_fares[route_fares["count"] >= 10].head(top_n)

    print(f"\nTop {top_n} Most Expensive Routes (min 10 flights):")
    print(expensive)

    return {"popular": popular, "expensive": expensive}


def calculate_tax_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate tax percentage from fare components.

    Args:
        df: DataFrame containing fare data

    Returns:
        DataFrame with Tax Percentage column
    """
    df_copy = df.copy()
    df_copy["Tax Percentage"] = (
        df_copy["Tax & Surcharge (BDT)"] / df_copy["Base Fare (BDT)"]
    ) * 100

    print("\nFare Components:")
    print(f"Base Fare - Mean:       {df_copy['Base Fare (BDT)'].mean():,.2f} BDT")
    print(f"Tax & Surcharge - Mean: {df_copy['Tax & Surcharge (BDT)'].mean():,.2f} BDT")
    print(f"Total Fare - Mean:      {df_copy['Total Fare (BDT)'].mean():,.2f} BDT")
    print(f"\nAverage Tax Percentage: {df_copy['Tax Percentage'].mean():.2f}%")

    return df_copy


def generate_business_insights(df: pd.DataFrame, top_n: int = 3) -> Dict[str, Any]:
    """
    Generate key business insights from the data.

    Args:
        df: DataFrame containing flight data
        top_n: Number of top items to show per category

    Returns:
        Dictionary with insights
    """
    print("=" * 60)
    print("KEY BUSINESS INSIGHTS")
    print("=" * 60)

    # Top airlines by fare
    print(f"\nAverage Fare Per Airline (Top {top_n}):")
    top_airlines = (
        df.groupby("Airline")["Total Fare (BDT)"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
        .head(top_n)
    )
    for idx, (airline, row) in enumerate(top_airlines.iterrows(), 1):
        print(f"   {idx}. {airline}: {row['mean']:,.2f} BDT (n={row['count']:,})")

    # Most popular routes (assuming Route column exists)
    if "Route" in df.columns:
        print(f"\nMOST POPULAR ROUTES (Top {top_n}):")
        top_routes = df["Route"].value_counts().head(top_n)
        for idx, (route, count) in enumerate(top_routes.items(), 1):
            avg_fare = df[df["Route"] == route]["Total Fare (BDT)"].mean()
            print(f"   {idx}. {route}: {count:,} flights, Avg Fare: {avg_fare:,.2f} BDT")

    # Seasonal variation
    print("\nSEASONAL FARE VARIATION:")
    seasonal = df.groupby("Seasonality")["Total Fare (BDT)"].mean().sort_values(ascending=False)
    for idx, (season, fare) in enumerate(seasonal.items(), 1):
        print(f"   {idx}. {season}: {fare:,.2f} BDT")

    # Class impact
    print("\nCLASS IMPACT ON FARES:")
    class_impact = (
        df.groupby("Class")["Total Fare (BDT)"]
        .agg(["mean", "count"])
        .sort_values("mean", ascending=False)
    )
    for idx, (cls, row) in enumerate(class_impact.iterrows(), 1):
        print(f"   {idx}. {cls}: {row['mean']:,.2f} BDT ({row['count']:,} flights)")

    print("\n" + "=" * 60)

    return {"top_airlines": top_airlines, "seasonal": seasonal, "class_impact": class_impact}
