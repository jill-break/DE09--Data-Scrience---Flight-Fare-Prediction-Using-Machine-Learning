"""
Data validation module using Pandera for schema validation.
"""

import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class FlightDataValidator:
    """Validates Flight Price Dataset against expected schema."""

    def __init__(self):
        """Initialize the validator with schema definition."""
        self.schema = self._define_schema()

    def _define_schema(self) -> DataFrameSchema:
        """
        Define the expected schema for the Flight Price Dataset.

        Returns:
            DataFrameSchema for validation
        """
        return DataFrameSchema(
            {
                "Airline": Column(
                    str,
                    checks=[
                        Check.str_length(min_value=3, max_value=100),
                        Check(lambda s: ~s.isna(), error="Airline cannot be null"),
                    ],
                    nullable=False,
                ),
                "Source": Column(
                    str,
                    checks=[
                        Check.str_length(min_value=2, max_value=5),
                        Check(lambda s: s.str.isupper(), error="Source should be uppercase"),
                    ],
                    nullable=False,
                ),
                "Source Name": Column(str, nullable=False),
                "Destination": Column(
                    str,
                    checks=[
                        Check.str_length(min_value=2, max_value=5),
                        Check(lambda s: s.str.isupper(), error="Destination should be uppercase"),
                    ],
                    nullable=False,
                ),
                "Destination Name": Column(str, nullable=False),
                "Departure Date & Time": Column(str, nullable=False),
                "Arrival Date & Time": Column(str, nullable=False),
                "Duration (hrs)": Column(
                    float,
                    checks=[
                        Check.greater_than(0),
                        Check.less_than(50, error="Duration too long"),
                    ],
                    nullable=False,
                ),
                "Stopovers": Column(str, nullable=False),
                "Aircraft Type": Column(str, nullable=True),
                "Class": Column(
                    str,
                    checks=[
                        Check.isin(["Economy", "Business", "First"]),
                    ],
                    nullable=False,
                ),
                "Booking Source": Column(str, nullable=False),
                "Base Fare (BDT)": Column(
                    float,
                    checks=[
                        Check.greater_than(0, error="Base fare must be positive"),
                        Check.less_than(1000000),
                    ],
                    nullable=False,
                ),
                "Tax & Surcharge (BDT)": Column(
                    float,
                    checks=[
                        Check.greater_than_or_equal_to(0),
                        Check.less_than(500000),
                    ],
                    nullable=False,
                ),
                "Total Fare (BDT)": Column(
                    float,
                    checks=[
                        Check.greater_than(0, error="Total fare must be positive"),
                        Check.less_than(1500000),
                    ],
                    nullable=False,
                ),
                "Seasonality": Column(str, nullable=False),
                "Days Before Departure": Column(
                    int,
                    checks=[
                        Check.greater_than_or_equal_to(0),
                        Check.less_than(365),
                    ],
                    nullable=False,
                ),
            },
            strict=False,  # Allow additional columns during exploration
        )

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate the dataframe against the schema.

        Args:
            df: DataFrame to validate

        Returns:
            Dictionary with validation results
        """
        results = {
            "is_valid": False,
            "errors": [],
            "warnings": [],
            "stats": {},
        }

        try:
            # Attempt validation
            _validated_df = self.schema.validate(df, lazy=True)  # noqa: F841
            results["is_valid"] = True
            logger.info("✅ Schema validation passed")

        except pa.errors.SchemaErrors as e:
            results["errors"] = e.failure_cases.to_dict("records")
            logger.error(f"❌ Schema validation failed with {len(e.failure_cases)} errors")

        # Additional business rule checks
        business_warnings = self._check_business_rules(df)
        warnings_list = results["warnings"]
        if isinstance(warnings_list, list):
            warnings_list.extend(business_warnings)

        # Calculate statistics
        results["stats"] = self._calculate_stats(df)

        return results

    def _check_business_rules(self, df: pd.DataFrame) -> list:
        """
        Check additional business rules not covered by schema.

        Args:
            df: DataFrame to check

        Returns:
            List of warnings
        """
        warnings = []

        # Check if Total Fare = Base Fare + Tax & Surcharge (within tolerance)
        if all(
            col in df.columns
            for col in ["Base Fare (BDT)", "Tax & Surcharge (BDT)", "Total Fare (BDT)"]
        ):
            calculated_total = df["Base Fare (BDT)"] + df["Tax & Surcharge (BDT)"]
            diff = abs(calculated_total - df["Total Fare (BDT)"])
            mismatches = (diff > 1.0).sum()  # Allow 1 BDT tolerance for rounding

            if mismatches > 0:
                warnings.append(
                    {
                        "rule": "Total Fare Calculation",
                        "message": f"{mismatches} rows have Total Fare != Base Fare + Tax",
                        "severity": "warning",
                    }
                )

        # Check for duplicate flights
        duplicate_cols = ["Airline", "Source", "Destination", "Departure Date & Time"]
        if all(col in df.columns for col in duplicate_cols):
            duplicates = df.duplicated(subset=duplicate_cols).sum()
            if duplicates > 0:
                warnings.append(
                    {
                        "rule": "Duplicate Flights",
                        "message": f"{duplicates} potential duplicate flight records found",
                        "severity": "info",
                    }
                )

        # Check for unusual fare patterns
        if "Total Fare (BDT)" in df.columns:
            median_fare = df["Total Fare (BDT)"].median()
            outliers = (
                (df["Total Fare (BDT)"] > median_fare * 10)
                | (df["Total Fare (BDT)"] < median_fare * 0.1)
            ).sum()
            if outliers > 0:
                warnings.append(
                    {
                        "rule": "Fare Outliers",
                        "message": f"{outliers} rows with extreme fares (10x or 0.1x median)",
                        "severity": "info",
                    }
                )

        return warnings

    def _calculate_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate summary statistics for the dataset.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary of statistics
        """
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": df.duplicated().sum(),
        }

        if "Total Fare (BDT)" in df.columns:
            stats["fare_stats"] = {
                "mean": float(df["Total Fare (BDT)"].mean()),
                "median": float(df["Total Fare (BDT)"].median()),
                "min": float(df["Total Fare (BDT)"].min()),
                "max": float(df["Total Fare (BDT)"].max()),
                "std": float(df["Total Fare (BDT)"].std()),
            }

        return stats


def validate_raw_data(filepath: str) -> Dict[str, Any]:
    """
    Main function to validate raw flight data.

    Args:
        filepath: Path to the CSV file

    Returns:
        Validation results dictionary
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger.info(f"Loading data from {filepath}")
    df = pd.read_csv(filepath)

    logger.info(f"Dataset shape: {df.shape}")

    validator = FlightDataValidator()
    results = validator.validate(df)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 Data Validation Report")
    print("=" * 60)

    print(f"\n✅ Valid: {results['is_valid']}")
    print(f"📈 Total Rows: {results['stats']['total_rows']:,}")
    print(f"📊 Total Columns: {results['stats']['total_columns']}")

    if results["errors"]:
        print(f"\n❌ Errors: {len(results['errors'])}")
        for error in results["errors"][:5]:  # Show first 5
            print(f"   - {error}")

    if results["warnings"]:
        print(f"\n⚠️  Warnings: {len(results['warnings'])}")
        for warning in results["warnings"]:
            print(f"   - {warning['message']}")

    if "fare_stats" in results["stats"]:
        print("\n💰 Fare Statistics (BDT):")
        for key, value in results["stats"]["fare_stats"].items():
            print(f"   {key.capitalize()}: {value:,.2f}")

    print("\n" + "=" * 60)

    return results


if __name__ == "__main__":
    results = validate_raw_data("data/01-raw/Flight_Price_Dataset_of_Bangladesh.csv")
