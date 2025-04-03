import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime, timedelta

# --- Configuration ---
pdf_filename = 'claims_analysis.pdf'
high_bill_threshold = 4000
date_format_str = '%Y-%m-%d'
trend_analysis_duration = 365

# --- Load Data ---
try:
    df = pd.read_csv('claims_data.csv')
    print("Data loaded successfully!")
    print(f"Number of rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")
except FileNotFoundError:
    print("Error: claims_data.csv not found. Please ensure the file is in the correct directory.")
    exit()
except Exception as e:
    print(f"An error occurred while loading the data: {e}")
    exit()

# Convert 'Claim_Date' to datetime if it's not already
if 'Claim_Date' in df.columns and df['Claim_Date'].dtype == 'object':
    df['Claim_Date'] = pd.to_datetime(df['Claim_Date'])

# --- PDF Generation ---
print("Attempting to initialize PDF generation...")
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
print("SimpleDocTemplate initialized.")
styles = getSampleStyleSheet()
print("Styles retrieved.")
story = []
print("Story list initialized.")

# Title
title = "Claims Data Analysis Report"
story.append(Paragraph(title, styles['h1']))
story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
story.append(Paragraph("---", styles['Normal']))

# --- Numerical Data (Head of DataFrame) ---
story.append(Paragraph("**Overview of the Data (First 10 Rows):**", styles['h2']))
data_head = df.head(10).values.tolist()
if data_head:
    table_head = Table([df.columns.tolist()] + data_head)
    table_head.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table_head)
else:
    story.append(Paragraph("No data to display.", styles['Normal']))
story.append(Paragraph("---", styles['Normal']))

# --- Key Metrics (Table) ---
story.append(Paragraph("**Key Metrics:**", styles['h2']))

# Calculate Metrics
if not df.empty:
    df['Payment_Rate'] = df['Paid_Amount'] / df['Billed_Amount']
    average_payment_rate_by_provider = df.groupby('Insurance_Provider')['Payment_Rate'].mean().round(3)
    total_billed_paid_by_provider = df.groupby('Insurance_Provider')[['Billed_Amount', 'Paid_Amount']].sum().round(2)
    average_age_by_claim_type = df.groupby('Claim_Type')['Patient_Age'].mean().round(1)

    metrics_data = [
        ["Metric", "Value"],
        ["Average Payment Rate by Provider", ""],
    ]
    for provider, rate in average_payment_rate_by_provider.items():
        metrics_data.append([f"  - {provider}", f"{rate}"])
    metrics_data.append(["Total Billed and Paid by Provider", ""])
    for provider, totals in total_billed_paid_by_provider.iterrows():
        metrics_data.append([f"  - {provider}", f"Billed: {totals['Billed_Amount']}, Paid: {totals['Paid_Amount']}"])
    metrics_data.append(["Average Patient Age by Claim Type", ""])
    for claim_type, age in average_age_by_claim_type.items():
        metrics_data.append([f"  - {claim_type}", f"{age}"])

    table_metrics = Table(metrics_data)
    table_metrics.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(table_metrics)
else:
    story.append(Paragraph("No data available to calculate key metrics.", styles['Normal']))
story.append(Paragraph("---", styles['Normal']))

# --- High-Billed Claims (Table) ---
story.append(Paragraph("**Top 5 High Bills:**", styles['h2']))
high_bill_claims = df[df['Billed_Amount'] > high_bill_threshold].head().values.tolist()
print(f"Number of high-billed claims found: {len(high_bill_claims)}")
if high_bill_claims:
    print("High-billed claims data:")
    print(high_bill_claims)

    def abbreviate_cell(cell_value):
        if isinstance(cell_value, str) and len(cell_value) > 10:
            return cell_value[:10] + "..."
        return cell_value

    desired_columns = ['Claim_ID', 'Claim_Date', 'Billed_Amount', 'Claim_Type']
    try:
        column_indices = [df.columns.get_loc(col) for col in desired_columns]

        def format_date(date_value):
            if isinstance(date_value, pd.Timestamp):
                return date_value.strftime('%Y-%m-%d')
            return date_value

        table_data = [[format_date(row[i]) if i == 1 else row[i] for i in column_indices] for row in high_bill_claims]
        table_data = [desired_columns] + table_data

        abbreviated_table_data = [
            table_data[0]
        ] + [
            [abbreviate_cell(cell) for cell in row]
            for row in table_data[1:]
        ]

        table_high_bill = Table(abbreviated_table_data,
                                colWidths=[1.0*inch, 1.2*inch, 0.8*inch, 1.0*inch])

        table_high_bill.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8)
        ]))
        story.append(table_high_bill)
    except KeyError as e:
        story.append(Paragraph(f"Error: Column '{e}' not found in the data.", styles['Normal']))
    except Exception as e:
        story.append(Paragraph(f"An error occurred while creating the high-billed claims table: {e}", styles['Normal']))
else:
    story.append(Paragraph("No high-billed claims found.", styles['Normal']))
story.append(Paragraph("---", styles['Normal']))

# --- Trend Analysis (Graph - Number of Claims Over Time - 1 Year) ---
print("\n--- Starting Trend Analysis (1 Year) ---")
if 'Claim_Date' in df.columns:
    print("Claim_Date column found.")
    try:
        one_year_ago = datetime.now() - timedelta(days=trend_analysis_duration)
        df_last_year = df[df['Claim_Date'] >= one_year_ago]

        if not df_last_year.empty:
            claims_over_time = df_last_year.set_index('Claim_Date').resample('M')['Claim_ID'].count()
            plt.figure(figsize=(10, 5))
            plt.plot(claims_over_time.index, claims_over_time.values, marker='o')
            plt.title('Number of Claims Over Time (Last 1 Year - Monthly)')
            plt.xlabel('Month')
            plt.ylabel('Number of Claims')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('claims_over_time_1year.png')
            print("Trend plot (1 year) created and saved as claims_over_time_1year.png.")

            story.append(Paragraph("**Trend Analysis: Number of Claims Over Time (Last 1 Year - Monthly)**", styles['h2']))
            try:
                from reportlab.platypus import Image
                img = Image('claims_over_time_1year.png', width=500, height=300)
                story.append(img)
                print("Trend graph (1 year) added to the story.")
            except ImportError:
                print("Error: reportlab.platypus.Image not found.")
                story.append(Paragraph("Error: reportlab.platypus.Image not found.", styles['Normal']))
            except Exception as e:
                print(f"Error adding trend graph (1 year) image: {e}")
                story.append(Paragraph(f"Error adding trend graph (1 year) image: {e}", styles['Normal']))
            plt.close()
            print("Trend plot (1 year) closed.")
        else:
            story.append(Paragraph("**Trend Analysis (Last 1 Year - Monthly):**", styles['h2']))
            story.append(Paragraph("Not enough data for the last year to generate the trend graph.", styles['Normal']))

    except ImportError:
        print("Matplotlib not found.")
        story.append(Paragraph("**Trend Analysis (Last 1 Year - Monthly):**", styles['h2']))
        story.append(Paragraph("Matplotlib not found. Cannot generate the trend graph.", styles['Normal']))
    except Exception as e:
        print(f"Error during trend analysis (1 year): {e}")
        story.append(Paragraph(f"Error during trend analysis (1 year): {e}", styles['Normal']))

else:
    print("Warning: 'Claim_Date' column not found, trend analysis graph (1 year) not generated.")
    story.append(Paragraph("Warning: 'Claim_Date' column not found, trend analysis graph (1 year) not generated.", styles['Normal']))

# --- Save the PDF ---
print("\nAttempting to build the PDF...")
try:
    doc.build(story)
    print(f"\nPDF report '{pdf_filename}' generated successfully in the current directory.")
    print(f"PDF creation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
except Exception as e:
    print(f"\nError generating PDF: {e}")
    print(f"Detailed error: {e}")

print("\n--- End of Processing ---")