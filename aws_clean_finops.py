import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os
import random

# --- Data Generation Function ---
def generate_dynamic_aws_data(num_days=30):
    """Generates synthetic AWS cost and usage data for the last `num_days` days."""
    dates = pd.date_range(end=pd.Timestamp.today(), periods=num_days)
    services = ['EC2', 'S3', 'RDS', 'Lambda']
    regions = ['us-east-1', 'us-west-2', 'eu-central-1']
    
    data = []
    for date in dates:
        for service in services:
            for region in regions:
                # Base simulated cost and usage
                base_cost = random.uniform(100, 500)
                base_usage = random.randint(1000, 10000)

                # Add variation to simulate realistic fluctuation
                cost = base_cost + random.uniform(-base_cost * 0.3, base_cost * 0.3)
                usage = base_usage + random.randint(-base_usage // 4, base_usage // 4)

                # Simulate rare anomalies or spikes
                if random.random() < 0.05:
                    cost *= random.uniform(2, 4)
                    usage *= random.randint(3, 6)
                if random.random() < 0.02:
                    cost *= random.uniform(0.1, 0.5)
                    usage = usage // random.randint(2, 5)

                # Append the record
                data.append({
                    'Date': date,
                    'Service': service,
                    'Region': region,
                    'ResourceGroup': f'rg-{service}-{region}',
                    'Cost': cost,
                    'Currency': 'USD',
                    'Usage': usage,
                    'Unit': 'Various'
                })

    return pd.DataFrame(data)  # Return as a pandas DataFrame


# --- Report Generation Function ---
def generate_aws_finops_report(csv_file_path, output_pdf="aws_finops_report.pdf"):
    temp_files = []  # Track temp chart images for cleanup
    try:
        # Load the CSV data
        df = pd.read_csv(csv_file_path)
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' to datetime

        # --- Layout Settings ---
        left_margin = 50
        right_margin = letter[0] - 50
        top_margin = letter[1] - 50
        bottom_margin = 50

        # Get unique services and regions for grouping
        services = df['Service'].unique()
        regions = df['Region'].unique()

        chart_titles = []  # Keep titles for each chart for later use

        # --- Charts by Service ---
        for service in services:
            service_data = df[df['Service'] == service]

            # Cost over time chart
            plt.figure(figsize=(10, 5))
            plt.plot(service_data['Date'], service_data['Cost'], marker='o', label=service, color='blue')
            plt.title(f'{service} Daily Cost (USD)')
            plt.xlabel('Date')
            plt.ylabel('Cost (USD)')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45, ha='right')
            plt.grid(True)
            plt.tight_layout()
            cost_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            plt.savefig(cost_temp.name)
            plt.close()
            temp_files.append(cost_temp)
            chart_titles.append(f'{service} Daily Cost')

            # Usage over time chart
            plt.figure(figsize=(10, 5))
            plt.plot(service_data['Date'], service_data['Usage'], marker='s', label=service, color='green')
            plt.title(f'{service} Daily Usage')
            plt.xlabel('Date')
            plt.ylabel('Usage (Units)')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45, ha='right')
            plt.grid(True)
            plt.tight_layout()
            usage_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            plt.savefig(usage_temp.name)
            plt.close()
            temp_files.append(usage_temp)
            chart_titles.append(f'{service} Daily Usage')

        # --- Charts by Region ---
        for region in regions:
            region_data = df[df['Region'] == region]

            # Region cost
            plt.figure(figsize=(10, 5))
            plt.plot(region_data['Date'], region_data['Cost'], marker='^', label=region, color='red')
            plt.title(f'{region} Daily Cost (USD)')
            plt.xlabel('Date')
            plt.ylabel('Cost (USD)')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45, ha='right')
            plt.grid(True)
            plt.tight_layout()
            cost_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            plt.savefig(cost_temp.name)
            plt.close()
            temp_files.append(cost_temp)
            chart_titles.append(f'{region} Daily Cost')

            # Region usage
            plt.figure(figsize=(10, 5))
            plt.plot(region_data['Date'], region_data['Usage'], marker='v', label=region, color='orange')
            plt.title(f'{region} Daily Usage')
            plt.xlabel('Date')
            plt.ylabel('Usage (Units)')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45, ha='right')
            plt.grid(True)
            plt.tight_layout()
            usage_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            plt.savefig(usage_temp.name)
            plt.close()
            temp_files.append(usage_temp)
            chart_titles.append(f'{region} Daily Usage')

        # --- Start Building PDF ---
        c = canvas.Canvas(output_pdf, pagesize=letter)

        # --- Title Page ---
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(letter[0] / 2, top_margin - 50, "AWS FinOps Report")
        c.setFont("Helvetica", 20)
        c.drawCentredString(letter[0] / 2, top_margin - 100, "By Alex Curtis")
        c.showPage()  # Move to next page

        # --- Summary Page ---
        c.setFont("Helvetica-Bold", 24)
        c.drawString(left_margin, top_margin - 50, "Report Summary")

        summary_text = """# Summary text placeholder - Replace with insights, high-level cost breakdowns, and findings."""
        c.setFont("Helvetica", 9)
        lines = summary_text.split('\n')
        y_position = top_margin - 100

        for line in lines:
            # Wrap long lines manually
            if len(line) > 90:
                words = line.split()
                wrapped_line = ""
                current_length = 0
                for word in words:
                    if current_length + len(word) + 1 <= 90:
                        wrapped_line += word + " "
                        current_length += len(word) + 1
                    else:
                        c.drawString(left_margin, y_position, wrapped_line.strip())
                        y_position -= 11
                        wrapped_line = word + " "
                        current_length = len(word) + 1
                c.drawString(left_margin, y_position, wrapped_line.strip())
            else:
                c.drawString(left_margin, y_position, line.strip())
            y_position -= 14

        c.showPage()  # Move to chart pages

        # --- Charts with Titles ---
        y_pos = top_margin - 50
        chart_height = 200
        chart_width = 550
        y_text_offset = 20

        for i, temp_file in enumerate(temp_files):
            c.setFont("Helvetica", 12)
            c.drawString(left_margin, y_pos + chart_height + y_text_offset, chart_titles[i])
            c.drawImage(temp_file.name, left_margin, y_pos, width=chart_width, height=chart_height)
            y_pos -= (chart_height + 50)

            # New page if running low on space
            if y_pos < bottom_margin:
                c.showPage()
                y_pos = top_margin - 50

        c.save()  # Finalize PDF
        print(f"AWS FinOps report generated: {output_pdf}")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"Error generating report: {e}")
    finally:
        # Clean up temporary files
        for tf in temp_files:
            if tf is not None and hasattr(tf, 'name') and os.path.exists(tf.name):
                tf.close()
                os.unlink(tf.name)


# --- Main Script ---
if __name__ == "__main__":
    # Generate mock AWS cost/usage data and save it
    dynamic_df = generate_dynamic_aws_data()
    dynamic_df.to_csv("aws_cost_data.csv", index=False)
    print("Generated dynamic data and saved to aws_cost_data.csv")

    # Generate the report using that data
    csv_file_path = "aws_cost_data.csv"
    generate_aws_finops_report(csv_file_path)
