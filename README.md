# Toll Booth Management System

This Python script simulates a basic toll booth management system. It allows you to process toll transactions, generate daily reports, and provides sample data generation for testing.

## Features

* **Toll Processing:** Records vehicle IDs, vehicle types, timestamps, and toll amounts.
* **Variable Toll Rates:** Supports varying toll rates based on vehicle type (extensible).
* **Daily Reports:** Generates daily toll collection reports, including transaction details and total collected amounts.
* **Sample Data Generation:** Creates random toll transactions for testing purposes.
* **Historical Reporting:** Generate reports for past dates.

## Getting Started

### Prerequisites

* Python 3.6 or later

### Usage

1.  **Save the Code:** Save the Python code as `toll_booth.py`.
2.  **Run the Script:** Execute the script from your terminal:

    ```bash
    python toll_booth.py
    ```

3.  **Output:** The script will output the processed toll messages and daily toll reports to the console.

### Code Structure

* **`TollBooth` Class:**
    * `__init__(self, booth_id, toll_rate)`: Initializes a toll booth with an ID and toll rate.
    * `process_toll(self, vehicle_id, vehicle_type, timestamp=None)`: Processes a toll transaction.
    * `generate_daily_report(self, date=None)`: Generates a daily toll collection report.
* **`generate_sample_data(booth, num_transactions=20)` Function:** Generates sample toll transactions for a given booth.

### Example

```python
# Create toll booths
booth1 = TollBooth(booth_id="Booth A", toll_rate=5.00)
booth2 = TollBooth(booth_id="Booth B", toll_rate=5.00)

# Generate sample data
generate_sample_data(booth1, num_transactions=30)
generate_sample_data(booth2, num_transactions=25)

# Generate daily reports
booth1.generate_daily_report()
booth2.generate_daily_report()

# Generate a report for yesterday
yesterday = datetime.date.today() - datetime.timedelta(days=1)
booth1.generate_daily_report(date=yesterday)