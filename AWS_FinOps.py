import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os

def generate_dynamic_aws_data(num_days=30):
    # (Your dynamic data generation function remains the same)
    # ...

def generate_recommendation_data():
    """Generates sample recommendation data."""
    recommendations = {
        'Cost Optimization': {
            'EC2 Instance Sizing': 1500,
            'Unused EBS Volumes': 800,
            'Reserved Instances': 2000,
            'S3 Storage Classes': 1200,
        },
        'Usage Efficiency': {
            'Lambda Function Optimization': 500,
            'RDS Read Replicas': 300,
            'Auto Scaling Policies': 700,
            'S3 Lifecycle Policies': 400,
        },
    }
    return recommendations

def generate_aws_finops_report(csv_file_path, output_pdf="aws_finops_report.pdf"):
    try:
        df = pd.read_csv(csv_file_path)
        df['Date'] = pd.to_datetime(df['Date'])

        # --- Generate Charts ---
        # (Your chart generation code remains the same)
        # ...

        # --- Generate PDF ---
        c = canvas.Canvas(output_pdf, pagesize=letter)

        # --- Title Page ---
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(letter[0] / 2, letter[1] - 100, "AWS FinOps Report")
        c.setFont("Helvetica", 20)
        c.drawCentredString(letter[0] / 2, letter[1] - 150, "By Alex Curtis")

        c.showPage()

        # --- Summary Page ---
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, letter[1] - 100, "Report Summary")

        summary_text = """
        This report analyzes AWS cost and usage data over the past 30 days. 
        Key findings include:
        - Significant fluctuations in daily costs due to anomalies.
        - Varying usage patterns across different AWS services and regions.

        Recommendations:
        - Implement EC2 instance sizing to save approximately $1500.
        - Optimize Lambda functions to improve usage efficiency by 500 units.
        - Utilize reserved instances to reduce costs by $2000.
        """
        c.setFont("Helvetica", 12)
        lines = summary_text.split('\n')
        y_position = letter[1] - 150
        for line in lines:
            c.drawString(50, y_position, line.strip())
            y_position -= 15  # Adjust spacing between lines

        c.showPage()

        # --- Chart Pages ---
        c.drawImage(cost_service_time_temp.name, 50, 600, width=500, height=150)
        c.drawString(50, 580, "Daily Cost by Service")

        c.drawImage(usage_service_time_temp.name, 50, 450, width=500, height=150)
        c.drawString(50, 430, "Daily Usage by Service")

        c.drawImage(cost_region_time_temp.name, 50, 300, width=500, height=150)
        c.drawString(50, 280, "Daily Cost by Region")

        c.drawImage(usage_region_time_temp.name, 50, 150, width=500, height=150)
        c.drawString(50, 130, "Daily Usage by Region")

        c.showPage()

        c.drawImage(cost_opt_temp.name, 50, 600, width=500, height=150)
        c.drawString(50, 580, "Cost Optimization Recommendations")

        c.drawImage(usage_eff_temp.name, 50, 450, width=500, height=150)
        c.drawString(50, 430, "Usage Efficiency Recommendations")

        c.save()
        print(f"AWS FinOps report generated: {output_pdf}")

        # --- Clean up temp files ---
        temp_files = [cost_service_time_temp, usage_service_time_temp, cost_region_time_temp, usage_region_time_temp, cost_opt_temp, usage_eff_temp]
        for tf in temp_files:
            tf.close()
            os.unlink(tf.name)

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    dynamic_df = generate_dynamic_aws_data()
    dynamic_df.to_csv("aws_cost_data.csv", index=False)
    print("Generated dynamic data and saved to aws_cost_data.csv")

    csv_file_path = "aws_cost_data.csv"
    generate_aws_finops_report(csv_file_path)