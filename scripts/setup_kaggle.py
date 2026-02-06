"""
Helper script to set up Kaggle credentials.
"""

import os
import json
from pathlib import Path


def setup_kaggle_credentials():
    """Interactive setup for Kaggle credentials."""
    print("\n" + "=" * 60)
    print("🔑 Kaggle API Credentials Setup")
    print("=" * 60)

    print("\nTo download the dataset, you need Kaggle API credentials.")
    print("\nSteps to get your credentials:")
    print("1. Go to https://www.kaggle.com/settings/account")
    print("2. Scroll to 'API' section")
    print("3. Click 'Create New API Token'")
    print("4. This will download 'kaggle.json'")

    kaggle_dir = Path.home() / ".kaggle"
    kaggle_file = kaggle_dir / "kaggle.json"

    # Check if credentials already exist
    if kaggle_file.exists():
        print(f"\n✓ Kaggle credentials already configured at: {kaggle_file}")
        try:
            with open(kaggle_file, "r") as f:
                creds = json.load(f)
                username = creds.get("username", "***")
                print(f"  Username: {username}")
            return True
        except Exception as e:
            print(f"⚠️  Error reading credentials: {e}")

    print(f"\n❌ Kaggle credentials not found at: {kaggle_file}")
    print("\nPlease choose an option:")
    print("1. I have already downloaded kaggle.json - help me set it up")
    print("2. I need to download kaggle.json first")
    print("3. Skip for now")

    choice = input("\nYour choice (1/2/3): ").strip()

    if choice == "1":
        setup_from_file()
    elif choice == "2":
        print("\nPlease:")
        print("1. Visit https://www.kaggle.com/settings/account")
        print("2. Download 'kaggle.json'")
        print("3. Run this script again")
        return False
    else:
        print("\n⚠️  Skipping Kaggle setup. You'll need to configure it later.")
        return False

    return True


def setup_from_file():
    """Set up credentials from existing kaggle.json file."""
    print("\nWhere is your kaggle.json file located?")
    print("(Enter full path, or press Enter for Downloads folder)")

    user_path = input("Path: ").strip()

    if not user_path:
        # Default to Downloads
        downloads = Path.home() / "Downloads" / "kaggle.json"
        if downloads.exists():
            user_path = str(downloads)
            print(f"✓ Found kaggle.json in Downloads")
        else:
            print(f"❌ kaggle.json not found in Downloads")
            return False

    source_file = Path(user_path)

    if not source_file.exists():
        print(f"❌ File not found: {source_file}")
        return False

    # Create .kaggle directory
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_dir.mkdir(exist_ok=True)

    # Copy file
    dest_file = kaggle_dir / "kaggle.json"

    import shutil
    shutil.copy(source_file, dest_file)

    # Set permissions (important for Linux/Mac)
    if os.name != "nt":  # Not Windows
        os.chmod(dest_file, 0o600)

    print(f"\n✅ Kaggle credentials installed successfully!")
    print(f"   Location: {dest_file}")

    # Validate
    try:
        with open(dest_file, "r") as f:
            creds = json.load(f)
            username = creds.get("username", "???")
            print(f"   Username: {username}")
    except Exception as e:
        print(f"⚠️  Warning: Could not validate credentials: {e}")

    return True


def main():
    """Main entry point."""
    setup_kaggle_credentials()
    print("\n" + "=" * 60)
    print("Next step: Run data ingestion")
    print("  python src/data/ingestion.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
