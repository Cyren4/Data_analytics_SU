# Financial Analysis of S&P 500 Assets

This project analyzes the performance of assets comprising the S&P 500 index, a leading indicator of the US stock market.  The application leverages Streamlit to provide an interactive dashboard visualizing key financial indicators and allowing users to filter data by date and asset. A word cloud is also generated from a related academic paper to visualize key terms.

## Project Overview

The goal is to provide a comprehensive analysis of S&P 500 assets, encompassing data exploration, visualization, and text mining.  The analysis focuses on daily price movements, trading volume, and volatility, and explores the relationship between these indicators.

The project uses data from Kaggle ([https://www.kaggle.com/datasets/hanseopark/sp-500-stocks-value-with-financial-statement](https://www.kaggle.com/datasets/hanseopark/sp-500-stocks-value-with-financial-statement)) and incorporates a PDF for text analysis using NLP techniques.

## Features

* **Interactive Data Exploration:** Users can select specific assets and date ranges to filter data.
* **Visualizations:** The application provides several charts:
    * Line charts showing the evolution of closing prices over time.
    * Bar charts illustrating daily trading volume.
    * Scatter plots depicting the relationship between daily high and low prices.
    * Box plots comparing the daily performance (percentage change) of selected assets.
    * Line plots illustrating daily price range.
* **Descriptive Statistics:** Provides summary statistics (mean, standard deviation, etc.) of the dataset.
* **Word Cloud:** Generates a word cloud from a provided PDF document highlighting key terms related to the topic.
* **Data Cleaning and Preprocessing:** Handles missing values and preprocesses the text data for analysis.

## Data

The data used is a cleaned version of the original dataset found on Kaggle.  This includes the creation of new variables.  The cleaned CSV is provided in the `clean-data` folder. The original data (various formats) can also be found in the `Data` folder.

## Setup

1. **Install Requirements:**  Install the necessary Python libraries using `pip install -r requirements.txt`.
2. **Run the application:** Execute the `SP500_app.py` file using `streamlit run SP500_app.py`.

## File Structure

```
├── Data/                     # Original data files (JSON, numbers, etc.)
│   ├── FS_sp500_Value.json
│   └── FS_sp500_Value.numbers
├── data_process.ipynb        # Jupyter Notebook for initial data exploration and cleaning 
├── README.md                 # This file
├── README_fr.md                 # This file in french
├── SP500_app.py              # Main Streamlit application script
├── articles/                 # Folder containing articles about this topic
│   └── S&P 500 volatility, volatility regimes, and ECONOMIC UNCERTAINTY.pdf
├── clean-data/              # Cleaned data files
│   ├── FS_sp500_Value_cleaned.csv
│   └── FS_sp500_Value_cleaned.json
└── requirements.txt          # List of required Python packages
```

## Contributors

- Salma Lahbati
- Cyrena Ramdani
- Yoav Cohen


This project is a student project fulfilling the requirements of a Data Management, Data Viz, and Text Mining course.  It aims to demonstrate skills in data handling, visualization, and natural language processing.