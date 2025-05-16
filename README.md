# 🏡 Immotop.lu Real Estate Price Prediction

This project involves **scraping**, **preprocessing**, **visualization**, and **machine learning modeling** to predict housing rental prices from listings on [immotop.lu](https://www.immotop.lu). The goal is to estimate the price of a new advertisement based on its features using real-world data.

---

 ✅ Table of Contents

- [Overview](#overview)
- [Data Collection](#data-collection)
- [Data Preprocessing](#data-preprocessing)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Modeling](#modeling)
- [Usage](#usage)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [License](#license)

---

✅ Overview

Rental property prices in Luxembourg can vary greatly based on factors like location, size, amenities, and more. This project automates the process of:

- Scraping real-time rental data from Immotop.lu
- Extracting and cleaning relevant features
- Visualizing patterns and trends
- Predicting rental prices using machine learning

---

✅ Data Collection

We used **Selenium** to scrape multiple pages from immotop.lu, handling:

- Pagination
- Lazy-loaded content
- Key features including:  
  - Title  
  - Location  
  - Surface area  
  - Number of rooms  
  - Floor (if available)  
  - Availability  
  - Price  
  - Link to the ad

---

✅ Data Preprocessing

Key steps:

- Extracted numeric values (e.g., price, surface)
- Removed outliers and extreme values
- Encoded categorical variables (like city names)
- Normalized and scaled the data

---

## 📊 Exploratory Data Analysis (EDA)

We created interactive and static visualizations to understand:

- Price distribution
- Correlation between features
- Price per m² trends by region
- Heatmaps and scatter plots

---

✅ Modeling

We trained a **regression model** to predict rental prices:

- **Algorithms tested:** Linear Regression, Random Forest, XGBoost
- **Evaluation metrics:** MAE, RMSE, R²
- **Hyperparameter tuning:** GridSearchCV or manual testing
- Best model exported for predictions on new ads

---

✅ Usage

```bash
# Clone the repository
git clone https://github.com/yourusername/immotop-price-predictor.git
cd immotop-price-predictor

# Install dependencies
pip install -r requirements.txt

# Run scraper
python scraper.py

# Run preprocessing and modeling
python main.py
