# Fintech Market Data Analysis

This project fetches historical stock and cryptocurrency data, calculates technical indicators (such as the Rolling Standard Deviation and Bollinger Bands), visualizes the data in charts, and generates a PDF report with the analysis results.

## Features

- Fetch stock data from Yahoo Finance for various tickers (e.g., Apple, Microsoft, Google, Bitcoin, Ethereum).
- Calculate technical indicators like Rolling Standard Deviation and Bollinger Bands.
- Plot stock price along with Bollinger Bands.
- Generate a PDF report summarizing the stock data and technical analysis.
  
## Requirements

- Python 3.x
- Libraries:
  - `yfinance`: To fetch historical stock data from Yahoo Finance.
  - `pandas`: For data manipulation.
  - `numpy`: For numerical operations.
  - `matplotlib`: For plotting charts.
  - `fpdf`: To generate PDF reports.

You can install the necessary libraries by running:

```bash
pip install yfinance pandas numpy matplotlib fpdf
