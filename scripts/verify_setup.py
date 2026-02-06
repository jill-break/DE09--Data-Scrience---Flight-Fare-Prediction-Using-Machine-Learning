"""
Verify that the development environment is properly set up.
"""

import sys
from pathlib import Path


def verify_python_version():
    """Check Python version."""
    print("\n🐍 Python Version:")
    version = sys.version_info
    print(f"   {version.major}.{version.minor}.{version.micro}")

    if version < (3, 10):
        print("   ❌ Python 3.10+ required")
        return False
    print("   ✅ Version OK")
    return True


def verify_imports():
    """Check all critical imports."""
    print("\n📦 Package Imports:")

    packages = [
        ("pandas", "Data manipulation"),
        ("numpy", "Numerical computing"),
        ("sklearn", "Machine learning"),
        ("xgboost", "Gradient boosting"),
        ("mlflow", "Experiment tracking"),
        ("dvc", "Data version control"),
        ("fastapi", "API framework"),
        ("matplotlib", "Visualization"),
        ("plotly", "Interactive plots"),
        ("pytest", "Testing"),
    ]

    failed = []
    for package, description in packages:
        try:
            __import__(package)
            print(f"   ✅ {package:<15} - {description}")
        except ImportError as e:
            print(f"   ❌ {package:<15} - FAILED: {e}")
            failed.append(package)

    return len(failed) == 0


def verify_directories():
    """Check project structure."""
    print("\n📁 Project Structure:")

    required_dirs = [
        "data/01-raw",
        "data/02-preprocessed",
        "data/03-features",
        "data/04-predictions",
        "src/data",
        "src/pipelines",
        "notebooks",
        "test",
        "config",
        "scripts",
    ]

    project_root = Path.cwd()
    missing = []

    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} - MISSING")
            missing.append(dir_path)

    return len(missing) == 0


def verify_config_files():
    """Check configuration files."""
    print("\n⚙️  Configuration Files:")

    required_files = [
        "requirements.txt",
        ".pre-commit-config.yaml",
        "pyproject.toml",
        ".env.example",
        ".env",
        ".gitignore",
        "README.md",
    ]

    project_root = Path.cwd()
    missing = []

    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ⚠️  {file_path} - MISSING")
            missing.append(file_path)

    return len(missing) == 0


def verify_kaggle_credentials():
    """Check Kaggle credentials."""
    print("\n🔑 Kaggle Credentials:")

    kaggle_path = Path.home() / ".kaggle" / "kaggle.json"

    if kaggle_path.exists():
        print(f"   ✅ Found at {kaggle_path}")
        try:
            import json

            with open(kaggle_path) as f:
                creds = json.load(f)
                if "username" in creds and "key" in creds:
                    print(f"   ✅ Username: {creds['username']}")
                    return True
                else:
                    print("   ❌ Invalid credentials format")
                    return False
        except Exception as e:
            print(f"   ❌ Error reading: {e}")
            return False
    else:
        print(f"   ⚠️  Not found at {kaggle_path}")
        print("   ℹ️  Run: python scripts/setup_kaggle.py")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("🔍 Flight Fare Prediction - Environment Verification")
    print("=" * 60)

    checks = [
        ("Python Version", verify_python_version),
        ("Package Imports", verify_imports),
        ("Project Structure", verify_directories),
        ("Configuration Files", verify_config_files),
        ("Kaggle Credentials", verify_kaggle_credentials),
    ]

    results = {}
    for name, check_func in checks:
        results[name] = check_func()

    # Summary
    print("\n" + "=" * 60)
    print("📊 Verification Summary")
    print("=" * 60)

    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status:<10} - {name}")

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 Environment is fully configured!")
        print("\nNext steps:")
        print("1. Download dataset: python src/data/ingestion.py")
        print("2. Start exploring: jupyter notebook notebooks/01_data_exploration.ipynb")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        if not results["Kaggle Credentials"]:
            print("\n💡 Tip: Run 'python scripts/setup_kaggle.py' to set up Kaggle")

    print("=" * 60 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
