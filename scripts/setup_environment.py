"""
Setup script for installing dependencies and configuring the development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """
    Run a shell command and handle errors.

    Args:
        command: Command to run as list
        description: Description of what the command does

    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, shell=True)
        print(result.stdout)
        print(f"{description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def setup_environment():
    """Set up the development environment."""
    project_root = Path(__file__).parent.parent

    print("\n" + "=" * 60)
    print("Flight Fare Prediction - Development Environment Setup")
    print("=" * 60)

    # Step 1: Check Python version
    python_version = sys.version_info
    print(
        f"\n✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}"
    )

    if python_version < (3, 10):
        print("Python 3.10 or higher is required")
        sys.exit(1)

    # Step 2: Upgrade pip
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")

    # Step 3: Install dependencies
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        run_command(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            "Installing dependencies from requirements.txt",
        )
    else:
        print(f"requirements.txt not found at {requirements_file}")
        sys.exit(1)

    # Step 4: Install pre-commit hooks
    run_command(["pre-commit", "install"], "Installing pre-commit hooks")

    # Step 5: Initialize DVC
    dvc_dir = project_root / ".dvc"
    if not dvc_dir.exists():
        run_command(["dvc", "init"], "Initializing DVC")
    else:
        print("\n✓ DVC already initialized")

    # Step 6: Set up local DVC remote
    dvc_cache = project_root / ".dvc" / "cache"
    run_command(
        ["dvc", "remote", "add", "-d", "local", str(dvc_cache), "-f"],
        "Configuring local DVC remote",
    )

    # Step 7: Create .env file if it doesn't exist
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"

    if not env_file.exists() and env_example.exists():
        import shutil

        shutil.copy(env_example, env_file)
        print("\n✓ Created .env file from .env.example")
        print("⚠️  Please update .env with your Kaggle credentials")
    elif env_file.exists():
        print("\n✓ .env file already exists")

    # Step 8: Summary
    print("\n" + "=" * 60)
    print("🎉 Environment Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update .env file with your Kaggle credentials")
    print("   - Visit https://www.kaggle.com/settings/account")
    print("   - Create New API Token")
    print("   - Update KAGGLE_USERNAME and KAGGLE_KEY in .env")
    print("\n2. Download the dataset:")
    print("   python src/data/ingestion.py")
    print("\n3. Start exploring:")
    print("   jupyter notebook notebooks/01_data_exploration.ipynb")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    setup_environment()
