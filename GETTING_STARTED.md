# Getting Started - Dataset Download

## Step 1: Set Up Kaggle Credentials

You need Kaggle API credentials to download the dataset.

### Option A: Quick Setup (Recommended)

1. **Get your Kaggle API token:**
   - Go to https://www.kaggle.com/settings/account
   - Scroll to "API" section
   - Click "Create New API Token"
   - This downloads `kaggle.json` to your Downloads folder

2. **Run the setup helper:**
   ```bash
   .\venv\Scripts\activate
   python scripts/setup_kaggle.py
   ```

   Follow the prompts to automatically configure your credentials.

### Option B: Manual Setup

1. **Download kaggle.json** (see Option A, step 1)

2. **Create .kaggle directory:**
   ```bash
   mkdir %USERPROFILE%\.kaggle
   ```

3. **Move kaggle.json:**
   ```bash
   move Downloads\kaggle.json %USERPROFILE%\.kaggle\kaggle.json
   ```

## Step 2: Download the Dataset

Once Kaggle credentials are configured:

```bash
.\venv\Scripts\activate
python src/data/ingestion.py
```

**Expected Output:**
```
✅ Data successfully downloaded to: data/01-raw/Flight_Price_Dataset_of_Bangladesh.csv
```

## Step 3: Verify Installation

Check that everything is set up correctly:

```bash
.\venv\Scripts\activate
python -c "import pandas; import sklearn; import xgboost; import mlflow; print('✅ All imports successful!')"
```

## Next Steps

After successful dataset download:

1. **Explore the data:**
   ```bash
   jupyter notebook notebooks/01_data_exploration.ipynb
   ```

2. **Review the project structure:**
   - Check `data/01-raw/` for the downloaded dataset
   - Review `README.md` for comprehensive documentation
   - See `implementation_plan.md` for the full roadmap

## Troubleshooting

### Kaggle API Error
- **Problem**: "Could not find kaggle.json"
- **Solution**: Ensure kaggle.json is in `%USERPROFILE%\.kaggle\`

### Dataset Not Found
- **Problem**: Dataset download fails
- **Solution**:
  1. Visit https://www.kaggle.com/datasets/farhanaaktermukarrima/flight-price-dataset-of-bangladesh
  2. Click "Download" to accept terms (just once)
  3. Run `python src/data/ingestion.py` again

### Import Errors
- **Problem**: Module not found
- **Solution**: Ensure virtual environment is activated: `.\venv\Scripts\activate`

## Summary

✅ Virtual environment created
✅ Dependencies installed (40+ packages)
✅ Pre-commit hooks configured
✅ DVC initialized
✅ Environment file created (.env)
⏳ **Next: Set up Kaggle credentials and download dataset**
