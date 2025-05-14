import os
from io import BytesIO
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Ensure matplotlib is imported
from fpdf import FPDF

# Example data for cost optimization
data = {
    "Service": ["Service1", "Service2", "Service3"],
    "Cost": [1000, 2000, 1500],
    "Department": ["Dept A", "Dept B", "Dept C"],
}

df = pd.DataFrame(data)

# Function to generate a bar plot
def generate_cost_plot(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Service", y="Cost", data=df, palette="Blues_d")
    ax.set_title("Service Cost Breakdown")
    return fig

# Function to generate the FinOps report
def generate_finops_report():
    # Generate the plot
    fig = generate_cost_plot(df)

    # Save the plot to a BytesIO stream
    img_stream = BytesIO()
    plt.savefig(img_stream, format='PNG')
    img_stream.seek(0)

    # Create the PDF for the report
    pdf = FPDF()
    pdf.add_page()

    # Add some text to the report
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="FinOps Cost Optimization Report", ln=True, align='C')
    pdf.ln(10)  # Add a line break

    # Save the image temporarily to a file
    temp_img_path = "temp_image.png"
    with open(temp_img_path, "wb") as f:
        f.write(img_stream.read())

    # Add the image to the PDF
    pdf.image(temp_img_path, x=10, y=pdf.get_y(), w=180)
    
    # Clean up the temporary image file
    os.remove(temp_img_path)

    # Add some more details (this can be extended)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Cost optimization suggestions:", ln=True, align='L')
    pdf.cell(200, 10, txt="1. Review underutilized services in Service2.", ln=True, align='L')
    pdf.cell(200, 10, txt="2. Consolidate Service1 and Service3 for cost reduction.", ln=True, align='L')

    # Save the PDF to file
    pdf.output("finops_report.pdf")
    print("FinOps report has been generated and saved as finops_report.pdf")

# Run the report generation
generate_finops_report()
