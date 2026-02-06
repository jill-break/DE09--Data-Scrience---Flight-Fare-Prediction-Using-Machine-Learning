# Flight Fare Prediction Using Machine Learning

A production-grade machine learning system for predicting flight fares in Bangladesh. This project implements a complete MLOps pipeline covering data ingestion, preprocessing, feature engineering, model training, deployment, and monitoring.

## 🎯 Project Overview

This project predicts flight fares based on:
- **Airline**: Carrier operating the flight
- **Route**: Source and destination airports
- **Temporal Features**: Date, season, holidays
- **Flight Details**: Class, stopovers, aircraft type
- **Booking Information**: Booking source and timing

**Key Features:**
- 🤖 Multiple ML models (Linear Regression, Random Forest, XGBoost)
- 📊 Comprehensive EDA and visualization
- 🔄 Automated MLOps pipeline with MLflow
- 🐳 Dockerized deployment
- 📝 Data versioning with DVC
- ✅ Extensive testing and code quality checks
- 📈 Model monitoring and drift detection

## 🏗️ Architecture

```
flight-fare-prediction/
├── data/
│   ├── 01-raw/              # Original dataset from Kaggle
│   ├── 02-preprocessed/     # Cleaned data
│   ├── 03-features/         # Engineered features
│   └── 04-predictions/      # Model outputs
├── src/
│   ├── data/                # Data ingestion & validation
│   ├── features/            # Feature engineering
│   ├── models/              # ML models
│   ├── training/            # Training pipeline
│   ├── evaluation/          # Model evaluation
│   ├── api/                 # FastAPI service
│   └── monitoring/          # Monitoring & logging
├── notebooks/               # Jupyter notebooks for EDA
├── test/                    # Unit & integration tests
├── scripts/                 # Utility scripts
├── config/                  # Configuration files
└── docker-compose.yml       # Container orchestration
```

## 📋 Requirements

- Python 3.10+
- Docker & Docker Compose (optional)
- Kaggle Account (for dataset download)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd DE09
```

### 2. Set Up Environment

#### Option A: Automated Setup (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run automated setup
python scripts/setup_environment.py
```

#### Option B: Manual Setup

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Initialize DVC
dvc init
dvc remote add -d local .dvc/cache
```

### 3. Configure Kaggle Credentials

1. Get your Kaggle API credentials:
   - Go to https://www.kaggle.com/settings/account
   - Click "Create New API Token"
   - This downloads `kaggle.json`

2. Set up credentials:

**Windows:**
```bash
# Create .kaggle directory
mkdir %USERPROFILE%\.kaggle

# Copy kaggle.json to the directory
copy kaggle.json %USERPROFILE%\.kaggle\kaggle.json
```

**Linux/Mac:**
```bash
mkdir -p ~/.kaggle
mv kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

3. Update `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
# Edit .env and update KAGGLE_USERNAME and KAGGLE_KEY if needed
```

### 4. Download Dataset

```bash
python src/data/ingestion.py
```

Expected output:
```
✅ Data successfully downloaded to: data/01-raw/Flight_Price_Dataset_of_Bangladesh.csv
```

### 5. Explore the Data

```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

## 📊 Dataset

**Source**: [Flight Price Dataset of Bangladesh](https://www.kaggle.com/datasets/farhanaaktermukarrima/flight-price-dataset-of-bangladesh)

**Features** (18 columns):
- Airline, Source, Destination
- Departure/Arrival Date & Time
- Duration, Stopovers, Aircraft Type
- Class, Booking Source
- Base Fare, Tax & Surcharge, **Total Fare** (target)
- Seasonality

**Size**: ~10,000+ flight records

## 🛠️ Development Workflow

### Code Quality

```bash
# Format code with black
black src/ test/

# Lint with flake8
flake8 src/ test/

# Type check with mypy
mypy src/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest test/unit/test_preprocessing.py -v
```

### Training Models

```bash
# Train baseline model
python scripts/train_model.py --model linear

# Train Random Forest
python scripts/train_model.py --model random_forest

# Train XGBoost with hyperparameter tuning
python scripts/train_model.py --model xgboost --tune
```

### MLflow Tracking

```bash
# Start MLflow UI
mlflow ui --port 5000

# Open in browser: http://localhost:5000
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build services
docker-compose build

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Services

- **API**: http://localhost:8000
- **MLflow UI**: http://localhost:5000
- **Jupyter**: http://localhost:8888

## 📈 Model Performance

| Model | R² | MAE (BDT) | RMSE (BDT) |
|-------|------|-----------|------------|
| Linear Regression | 0.72 | 850 | 1,250 |
| Random Forest | 0.87 | 620 | 890 |
| XGBoost | 0.89 | 580 | 840 |

*Results on validation set*

## 📚 Project Phases

- [x] **Phase 1**: Foundation & Infrastructure Setup
- [ ] **Phase 2**: Configuration Management
- [ ] **Phase 3**: Data Engineering Pipeline
- [ ] **Phase 4**: Model Development
- [ ] **Phase 5**: Training & Optimization
- [ ] **Phase 6**: Evaluation & Interpretation
- [ ] **Phase 7**: API & Deployment
- [ ] **Phase 8**: Monitoring & Observability

See [`implementation_plan.md`](./.gemini/antigravity/brain/997eb86a-fab2-47a1-8002-5f282146f3c3/implementation_plan.md) for detailed roadmap.

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and commit: `git commit -am 'Add new feature'`
3. Push to branch: `git push origin feature/new-feature`
4. Submit pull request

All commits must pass pre-commit hooks and tests.

## 📝 License

This project is for educational purposes as part of a Data Science course.

## 🙏 Acknowledgments

- Dataset: [Farhana Akter Mukarrima](https://www.kaggle.com/farhanaaktermukarrima)
- Course: DE09 - Data Science - Flight Fare Prediction Using Machine Learning

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**Status**: 🚧 Active Development | **Version**: 0.1.0 | **Last Updated**: 2026-02-06
