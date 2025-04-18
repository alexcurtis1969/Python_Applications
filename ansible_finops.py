import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from datetime import date
import numpy as np

# Define file names
CSV_FILE = "finops_monthly_report.csv"
OUTPUT_PDF = "FinOps_Report.pdf"
CHART_DEPARTMENT_FILE = "finops_cost_by_department.png"
CHART_SERVICE_FILE = "finops_cost_by_service.png"
REPORT_PREPARED_BY = "Alex Curtis"
REPORT_PREPARED_FOR = "Life is Full of Beaches Corporation"

sns.set(style="whitegrid")


# === Data Generation ===
def generate_finops_data(num_rows=20):
    """Generates a DataFrame with sample FinOps data."""

    departments = [
        "Engineering",
        "Marketing",
        "Sales",
        "Finance",
        "HR",
        "Data Science",
        "Product",
    ]
    data = []
    for _ in range(num_rows):
        department = np.random.choice(departments)
        ec2_cost = np.random.uniform(500, 10000)
        s3_cost = np.random.uniform(100, 2000)
        rds_cost = np.random.uniform(200, 5000)
        total_cost = ec2_cost + s3_cost + rds_cost
        data.append(
            {
                "Department": department,
                "EC2 Monthly Cost ($)": ec2_cost,
                "S3 Cost ($)": s3_cost,
                "RDS Monthly Cost ($)": rds_cost,
                "Total Monthly Cost ($)": total_cost,
            }
        )
    return pd.DataFrame(data)


# Generate and save data
df = generate_finops_data()
df.to_csv(CSV_FILE, index=False)

# === Grouping and Summary ===
# Print the columns to debug
print(df.columns)

dept_summary = (
    df.groupby("Department")[
        [
            "EC2 Monthly Cost ($)",
            "S3 Cost ($)",
            "RDS Monthly Cost ($)",  # Ensure this matches exactly!
            "Total Monthly Cost ($)",
        ]
    ]
    .sum()
    .sort_values("Total Monthly Cost ($)", ascending=False)
    .round(2)
)

cost_contribution = (
    df[["EC2 Monthly Cost ($)", "S3 Cost ($)", "RDS Monthly Cost ($)"]]  # And here!
    .sum()
    .sort_values(ascending=False)
    .round(2)
)


# === Charts ===
def create_cost_by_department_chart(dept_summary, output_file):
    """Creates and saves a bar chart of total monthly cloud cost by department."""
    plt.figure(figsize=(12, 6))
    sns.barplot(
        x=dept_summary.index,
        y=dept_summary["Total Monthly Cost ($)"],
        hue=dept_summary.index,
        palette="viridis",
        dodge=False,
        legend=False,
    )
    plt.title("Total Monthly Cloud Cost by Department")
    plt.ylabel("Cost (USD)")
    plt.xlabel("Department")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def create_cost_by_service_chart(cost_contribution, output_file):
    """Creates and saves a bar chart of total cloud cost contribution by service."""
    plt.figure(figsize=(8, 5))
    sns.barplot(
        x=cost_contribution.index,
        y=cost_contribution.values,
        hue=cost_contribution.index,
        palette="coolwarm",
        dodge=False,
        legend=False,
    )
    plt.title("Total Cloud Cost Contribution by Service")
    plt.ylabel("Cost (USD)")
    plt.xlabel("Service")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


create_cost_by_department_chart(dept_summary, CHART_DEPARTMENT_FILE)
create_cost_by_service_chart(cost_contribution, CHART_SERVICE_FILE)


# === PDF Generation ===
pdf = FPDF()

# Title Page
pdf.add_page()
pdf.set_font("Arial", "B", 24)
pdf.ln(50)
pdf.cell(0, 10, "Monthly FinOps Cost Report", ln=True, align="C")

pdf.set_font("Arial", "", 16)
pdf.ln(10)
pdf.cell(0, 10, f"Prepared by: {REPORT_PREPARED_BY}", ln=True, align="C")
pdf.cell(0, 10, f"Prepared for: {REPORT_PREPARED_FOR}", ln=True, align="C")

pdf.ln(40)  # Added extra spacing for image

pdf.cell(0, 10, f"Date: {date.today()}", ln=True, align="C")

# Main Content - Page 2
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Monthly FinOps Cloud Cost Report", ln=True, align="C")
pdf.ln(10)

pdf.set_font("Arial", "", 12)
introduction_text = (
    "This FinOps report provides a detailed breakdown of our monthly cloud infrastructure costs. "
    "It is designed to give you a clear understanding of where our cloud spending is going, "
    "categorized by both the department responsible and the specific cloud service utilized (EC2 for compute, "
    "S3 for storage, and RDS for databases). By analyzing this data, we can identify key areas for potential "
    "optimization and ensure we're using our cloud resources efficiently."
)
pdf.multi_cell(0, 10, introduction_text)
pdf.ln(5)

# Chart 1 (on Page 2)
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Cloud Cost by Department", ln=True)
pdf.image(CHART_DEPARTMENT_FILE, w=180)
pdf.ln(10)

# Chart 2 (Moved to Page 3)
pdf.add_page()
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Cloud Cost Contribution by Service", ln=True)
pdf.image(CHART_SERVICE_FILE, w=150)
pdf.ln(10)

# Table Output (Page 4)
pdf.add_page()


def create_department_summary_section(pdf, dept_summary):
    """Adds a simplified department summary with fixed-width alignment and shading."""
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Department Summary (USD)", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 10)
    header_text = f"{'Department':<20} {'EC2 Cost':>14} {'S3 Cost':>14} {'RDS Cost':>14} {'Total Cost':>14}"
    pdf.cell(0, 8, header_text, ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 10)
    fill = False
    for index, row in dept_summary.iterrows():
        if fill:
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(0, 8, "", 0, 1, "L", 1)
            pdf.set_xy(pdf.get_x(), pdf.get_y() - 8)

        row_text = (
            f"{index:<20} ${row['EC2 Monthly Cost ($)']:>13.2f}  ${row['S3 Cost ($)']:>13.2f}  "
            f"${row['RDS Monthly Cost ($)']:>13.2f}  ${row['Total Monthly Cost ($)']:>13.2f}"
        )
        pdf.cell(0, 8, row_text, ln=True)
        fill = not fill


create_department_summary_section(pdf, dept_summary)


# Conclusion (Page 5)
pdf.add_page()
pdf.ln(10)
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Conclusion", ln=True)
pdf.set_font("Arial", "", 12)
conclusion_text = (
    "Our analysis reveals that EC2 instances represent the most significant portion of our cloud expenditure, "
    "indicating the high cost of compute resources. Following EC2, S3 storage and RDS database services also "
    "contribute substantially to overall costs. Notably, the Engineering and Data Science departments exhibit "
    "the highest spending, likely due to their intensive use of compute resources for development and data processing. "
    "These findings underscore the importance of optimizing EC2 usage and closely monitoring resource allocation "
    "within these departments. Furthermore, promoting cost awareness and accountability across all teams can "
    "lead to more efficient cloud resource management and significant cost savings."
)
pdf.multi_cell(0, 10, conclusion_text)

# Save PDF
try:
    pdf.output(OUTPUT_PDF)
    print(f"PDF report '{OUTPUT_PDF}' generated successfully.")
except Exception as e:
    print(f"An error occurred while generating the PDF: {e}")