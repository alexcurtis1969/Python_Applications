# EC2 Cost Analysis Web Application

This Flask-based web application analyzes EC2 cost data from a CSV file, generates visualizations, and stores both the analysis results and visualizations in an AWS S3 bucket.

## Features

-   **Data Analysis:** Analyzes EC2 cost data to provide insights into costs, instance usage, and potential savings.
-   **Visualization:** Generates visualizations using Matplotlib and Seaborn to display analysis results.
-   **AWS S3 Integration:** Stores and retrieves analysis results and visualizations from an AWS S3 bucket.
-   **Web Interface:** Provides a simple web interface for running the analysis and downloading results.
-   **Password Protection:** Basic password protection for accessing the application.

## Prerequisites

-   Python 3.6+
-   AWS account with configured credentials
-   `ec2_data.csv` file containing EC2 cost data

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure AWS Credentials:**

    Ensure you have configured your AWS credentials either through environment variables or the AWS CLI.

5.  **Place your `ec2_data.csv` file in the same directory as `app.py`.**

6.  **Set the password:**

    Modify the `PASSWORD_HASH` and `SALT` variables in `app.py` with your desired password.

    ```python
    import hashlib
    import secrets

    PASSWORD_HASH = hashlib.sha256("your_strong_password".encode()).hexdigest()
    SALT = secrets.token_hex(16)
    PASSWORD_HASH = hashlib.sha256((PASSWORD_HASH + SALT).encode()).hexdigest()
    ```

## Usage

1.  **Run the Flask application:**

    ```bash
    python app.py
    ```

2.  **Access the application in your web browser:**

    Open your browser and navigate to `http://127.0.0.1:5000/`.

3.  **Login:**

    Enter the password you set in `app.py`.

4.  **Run the analysis:**

    Click the link or navigate to `http://127.0.0.1:5000/run_analysis` to start the analysis.

5.  **Download results:**

    Click the download link or navigate to `http://127.0.0.1:5000/download` to download the analysis results as a CSV file.

6.  **View visualizations:**

    The visualizations will be uploaded to the S3 bucket. You can access them through the web interface (if implemented) or directly from your S3 bucket.

## AWS S3 Configuration

-   The application creates an S3 bucket named `alexas-ec2-cost-analysis-bucket` in the `us-east-1` region (or the specified region).
-   The analysis results are stored in the bucket as `ec2_analysis.csv`.
-   Visualizations are stored in the `visualizations/` folder within the bucket.

## Dependencies

-   Flask
-   Pandas
-   Matplotlib
-   Seaborn
-   Boto3
-   Requests

## Notes

-   Ensure your AWS credentials have the necessary permissions to create and access S3 buckets.
-   The application uses basic password protection. For production environments, consider using more robust authentication and authorization mechanisms.
-   The application assumes the `ec2_data.csv` file has specific column names. If your data has different column names, you may need to modify the analysis functions.
-   The visualisations are saved to the local directory, and then uploaded to S3. They are not served directly from the local machine.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs or feature requests.

## License

This project is licensed under the MIT License.