"""
Data ingestion module for downloading and validating the Flight Price Dataset.
"""

import os
import logging
from pathlib import Path
from typing import Optional
import hashlib

logger = logging.getLogger(__name__)


class DataIngestion:
    """Handles data download and initial validation from Kaggle."""

    def __init__(self, data_dir: str = "data/01-raw"):
        """
        Initialize data ingestion.

        Args:
            data_dir: Directory to store raw data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.dataset_name = "farhanaaktermukarrima/flight-price-dataset-of-bangladesh"
        self.expected_filename = "Flight_Price_Dataset_of_Bangladesh.csv"

    def download_from_kaggle(self) -> Path:
        """
        Download dataset from Kaggle using the Kaggle API.

        Returns:
            Path to the downloaded file

        Raises:
            Exception: If Kaggle credentials are not configured or download fails
        """
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi

            logger.info("Initializing Kaggle API...")
            api = KaggleApi()
            api.authenticate()

            # Check if file already exists
            target_file = self.data_dir / self.expected_filename
            if target_file.exists():
                logger.info(f"Dataset already exists at {target_file}")
                return target_file

            logger.info(f"Downloading dataset: {self.dataset_name}")
            api.dataset_download_files(
                self.dataset_name, path=str(self.data_dir), unzip=True
            )

            if not target_file.exists():
                raise FileNotFoundError(
                    f"Expected file {self.expected_filename} not found after download"
                )

            logger.info(f"Dataset downloaded successfully to {target_file}")
            return target_file

        except Exception as e:
            logger.error(f"Failed to download dataset: {str(e)}")
            raise

    def calculate_file_hash(self, filepath: Path) -> str:
        """
        Calculate SHA256 hash of a file for integrity checking.

        Args:
            filepath: Path to the file

        Returns:
            Hex string of the file hash
        """
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def validate_file(self, filepath: Path) -> dict:
        """
        Perform basic validation on the downloaded file.

        Args:
            filepath: Path to the file to validate

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "file_exists": filepath.exists(),
            "file_size_mb": 0.0,
            "file_hash": None,
            "is_readable": False,
        }

        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            return validation_results

        # File size
        file_size = filepath.stat().st_size
        validation_results["file_size_mb"] = round(file_size / (1024 * 1024), 2)
        logger.info(f"File size: {validation_results['file_size_mb']} MB")

        # File hash
        validation_results["file_hash"] = self.calculate_file_hash(filepath)
        logger.info(f"File hash: {validation_results['file_hash']}")

        # Check if file is readable
        try:
            import pandas as pd

            df = pd.read_csv(filepath, nrows=5)
            validation_results["is_readable"] = True
            logger.info(f"File is readable. Sample shape: {df.shape}")
        except Exception as e:
            logger.error(f"File is not readable: {str(e)}")

        return validation_results

    def run(self) -> Path:
        """
        Run the complete data ingestion pipeline.

        Returns:
            Path to the validated data file
        """
        logger.info("Starting data ingestion pipeline...")

        # Download data
        data_path = self.download_from_kaggle()

        # Validate data
        validation_results = self.validate_file(data_path)

        if not validation_results["is_readable"]:
            raise ValueError("Downloaded file failed validation")

        logger.info("Data ingestion completed successfully")
        logger.info(f"Data location: {data_path}")
        logger.info(f"Validation results: {validation_results}")

        return data_path


def main():
    """Main entry point for data ingestion."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ingestion = DataIngestion()

    try:
        data_path = ingestion.run()
        print(f"\n✅ Data successfully downloaded to: {data_path}")
    except Exception as e:
        print(f"\n❌ Data ingestion failed: {str(e)}")
        print("\nPlease ensure:")
        print("1. Kaggle API credentials are configured (~/.kaggle/kaggle.json)")
        print("2. You have accepted the dataset terms on Kaggle website")
        print("3. Internet connection is available")
        raise


if __name__ == "__main__":
    main()
