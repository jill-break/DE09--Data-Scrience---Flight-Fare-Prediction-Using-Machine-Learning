"""
Visualization utilities for Flight Fare Prediction EDA.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from typing import Optional


def plot_target_distribution(df: pd.DataFrame, column: str = "Total Fare (BDT)") -> None:
    """
    Plot distribution of target variable.

    Args:
        df: DataFrame containing the data
        column: Name of the column to plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # Histogram
    axes[0].hist(df[column], bins=50, edgecolor="black", alpha=0.7)
    axes[0].set_xlabel(column, fontsize=12)
    axes[0].set_ylabel("Frequency", fontsize=12)
    axes[0].set_title(f"Distribution of {column}", fontsize=14, fontweight="bold")
    axes[0].grid(alpha=0.3)

    # Box plot
    axes[1].boxplot(df[column], vert=True)
    axes[1].set_ylabel(column, fontsize=12)
    axes[1].set_title(f"{column} Box Plot", fontsize=14, fontweight="bold")
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    print(f"\n{column} Statistics:")
    print(f"Mean:   {df[column].mean():>12,.2f} BDT")
    print(f"Median: {df[column].median():>12,.2f} BDT")
    print(f"Min:    {df[column].min():>12,.2f} BDT")
    print(f"Max:    {df[column].max():>12,.2f} BDT")
    print(f"Std:    {df[column].std():>12,.2f} BDT")


def plot_average_fare_by_category(
    df: pd.DataFrame,
    category_col: str,
    fare_col: str = "Total Fare (BDT)",
    title: Optional[str] = None,
) -> pd.DataFrame:
    """
    Plot average fare by category using Plotly.

    Args:
        df: DataFrame containing the data
        category_col: Column to group by
        fare_col: Fare column name
        title: Plot title (optional)

    Returns:
        DataFrame with aggregated results
    """
    fare_stats = (
        df.groupby(category_col)[fare_col]
        .agg(["mean", "median", "count"])
        .sort_values("mean", ascending=False)
    )

    title = title or f"Average Fare by {category_col}"

    fig = px.bar(
        fare_stats.reset_index(),
        x=category_col,
        y="mean",
        title=title,
        labels={"mean": f"Average {fare_col}", category_col: category_col},
        text="mean",
    )
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(height=500)
    fig.show()

    return fare_stats


def plot_correlation_heatmap(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Plot correlation heatmap for numerical features.

    Args:
        df: DataFrame containing the data
        columns: List of column names to include

    Returns:
        Correlation matrix
    """
    correlation_matrix = df[columns].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"label": "Correlation Coefficient"},
    )
    plt.title("Correlation Heatmap - Numerical Features", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.show()

    return correlation_matrix


def plot_booking_lead_time(df: pd.DataFrame, column: str = "Days Before Departure") -> None:
    """
    Plot booking lead time distribution.

    Args:
        df: DataFrame containing the data
        column: Column name for lead time
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.hist(df[column], bins=50, edgecolor="black", alpha=0.7)
    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Booking Lead Time", fontsize=14, fontweight="bold")
    ax.grid(alpha=0.3)
    plt.show()

    print("\nBooking Lead Time Statistics:")
    print(f"Mean:   {df[column].mean():.2f} days")
    print(f"Median: {df[column].median():.2f} days")
    print(f"Min:    {df[column].min()} days")
    print(f"Max:    {df[column].max()} days")


def plot_scatter_with_trend(
    df: pd.DataFrame, x_col: str, y_col: str, sample_size: int = 5000, title: Optional[str] = None
) -> None:
    """
    Plot scatter plot with trend line.

    Args:
        df: DataFrame containing the data
        x_col: X-axis column name
        y_col: Y-axis column name
        sample_size: Number of points to sample for performance
        title: Plot title (optional)
    """
    title = title or f"{y_col} vs {x_col}"

    fig = px.scatter(
        df.sample(min(sample_size, len(df))),
        x=x_col,
        y=y_col,
        opacity=0.5,
        title=title,
        trendline="lowess",
    )
    fig.update_layout(height=500)
    fig.show()
