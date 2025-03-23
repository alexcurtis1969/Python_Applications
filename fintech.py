import yfinance as yf  # Importing the yfinance library to fetch historical stock data
import pandas as pd  # Importing pandas for data manipulation
import numpy as np  # Importing numpy for numerical operations
import matplotlib.pyplot as plt  # Importing matplotlib to plot graphs
from fpdf import FPDF  # Importing fpdf to generate PDF reports

# Function to fetch stock data
def fetch_data(ticker):
    data = yf.download(ticker, period="1y", interval="1d")  # Download data for the last year with daily intervals
    return data  # Return the stock data

# Function to calculate technical indicators
def calculate_technical_indicators(df):
    # Calculate the Rolling Standard Deviation (volatility measure)
    df['rolling_std'] = df['Close'].rolling(window=20).std()  # Using the last 20 days to calculate standard deviation
    # Calculate Bollinger Bands
    df['UpperBand'] = df['Close'].rolling(window=20).mean() + (df['rolling_std'] * 2)  # Upper band is the average + 2 times the standard deviation
    df['LowerBand'] = df['Close'].rolling(window=20).mean() - (df['rolling_std'] * 2)  # Lower band is the average - 2 times the standard deviation
    
    # Fill missing values with N/A (useful for first 19 rows as they won’t have a full window for rolling calculations)
    df.fillna("N/A", inplace=True)
    
    return df  # Return the DataFrame with calculated indicators

# Function to plot the stock data and Bollinger Bands
def plot_data(df, ticker):
    plt.figure(figsize=(10, 6))  # Set figure size for the plot
    
    # Plot the closing price
    plt.plot(df['Close'], label=f'{ticker} Closing Price', color='blue') 
    
    # Plot the Upper and Lower Bollinger Bands
    plt.plot(df['UpperBand'], label='Upper Bollinger Band', color='red', linestyle='--')
    plt.plot(df['LowerBand'], label='Lower Bollinger Band', color='red', linestyle='--')
    
    # Add labels and title
    plt.title(f'{ticker} Stock Price with Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()  # Add legend to the plot
    
    plt.show()  # Display the plot

# Function to generate a PDF report
def generate_pdf(tickers):
    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title for the PDF report
    pdf.cell(200, 10, txt="Stock Market Data Report", ln=True, align="C")
    
    # Loop through each ticker to fetch and process data
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        df = fetch_data(ticker)  # Fetch stock data
        df = calculate_technical_indicators(df)  # Calculate technical indicators
        
        # Add a title for each stock in the PDF
        pdf.cell(200, 10, txt=f"Stock Data for {ticker}", ln=True, align="L")
        
        # Save the plot of the stock with Bollinger Bands
        plot_data(df, ticker)
        
        # Add some description text to the PDF
        pdf.multi_cell(0, 10, txt=f"Stock data and technical indicators for {ticker} have been fetched.")
    
    # Save the PDF to a file
    pdf.output("fintech_market_data.pdf")
    print("PDF generated successfully: fintech_market_data.pdf")

# Main function to run the analysis
def main():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'BTC-USD', 'ETH-USD']  # List of tickers to analyze
    generate_pdf(tickers)  # Generate PDF report for all tickers

if __name__ == "__main__":
    main()  # Run the main function
