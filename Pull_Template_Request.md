
### Pull Request Title:
Add Market Data Analysis with Rolling Standard Deviation and Bollinger Bands

---

### Description:
This PR adds a Python script that fetches market data for multiple tickers (AAPL, MSFT, GOOGL, BTC-USD, ETH-USD) from Yahoo Finance, calculates the rolling standard deviation, and generates Bollinger Bands for price volatility analysis. The script also generates a PDF report with the stock data, technical indicators, and plots for better visualization of market trends.

---

### Changes Made:
- Added functionality to fetch market data using the `yfinance` library.
- Implemented the calculation of rolling standard deviation and Bollinger Bands for each ticker.
- Included functionality to generate a PDF report that summarizes the data, technical indicators, and charts.
- Added proper error handling for missing data and invalid tickers.
- Updated the `requirements.txt` to include necessary dependencies.

---

### How to Test:
1. Clone this repository and navigate to the project folder.
2. Install the dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script `fintech.py` using Python:
   ```bash
   python fintech.py
   ```
4. Ensure the script successfully generates the `fintech_market_data.pdf` file in the project directory.
5. Verify that the PDF contains the correct stock data, rolling standard deviation values, Bollinger Bands, and plots for each ticker.

---

### Checklist:
- [ ] **Code Fetches Data**: Confirm that the script fetches market data for the specified tickers (AAPL, MSFT, GOOGL, BTC-USD, ETH-USD) from Yahoo Finance.
- [ ] **Rolling Standard Deviation**: Ensure the rolling standard deviation is calculated correctly for each stock and cryptocurrency.
- [ ] **Bollinger Bands**: Verify that the upper and lower Bollinger Bands are calculated and plotted on the stock price charts.
- [ ] **PDF Report Generation**: Check that the script generates a PDF report with the stock data, technical indicators, and plots.
- [ ] **Error Handling**: Make sure error handling works for cases such as missing data or invalid tickers.
- [ ] **Dependency Installation**: Confirm that the `requirements.txt` file is updated and all necessary dependencies (like `yfinance`, `pandas`, `numpy`, `matplotlib`, `fpdf`) are listed.
- [ ] **Script Run Test**: Run the script and verify that the PDF is generated without errors.
- [ ] **Readme File**: Ensure the README.md file includes clear instructions for installing dependencies, running the script, and expected outputs.
- [ ] **Code Formatting**: Double-check that the code follows the proper style guide and is well-commented for clarity.

---

### Related Issues:
- # (If there's an associated issue, add it here)

---

### Additional Notes:
- The `auto_adjust=True` warning in the `yfinance` library is addressed by the default setting in the latest version of the library.
- Make sure the required libraries (like `pandas`, `numpy`, `yfinance`, `matplotlib`, and `fpdf`) are installed before running the script.
