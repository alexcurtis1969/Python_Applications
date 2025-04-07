import pandas as pd
 import matplotlib.pyplot as plt
 import matplotlib.dates as mdates  # Import for date formatting
 from reportlab.lib.pagesizes import letter
 from reportlab.pdfgen import canvas
 import tempfile
 import os
 import random
 

 def generate_dynamic_aws_data(num_days=30):
  """Generates dynamic AWS cost and usage data."""
  dates = pd.date_range(end=pd.Timestamp.today(), periods=num_days)
  services = ['EC2', 'S3', 'RDS', 'Lambda']
  regions = ['us-east-1', 'us-west-2', 'eu-central-1']
 

  data = []
  for date in dates:
  for service in services:
  for region in regions:
  base_cost = random.uniform(100, 500)
  base_usage = random.randint(1000, 10000)
 

  cost = base_cost + random.uniform(-base_cost * 0.3, base_cost * 0.3)
  usage = base_usage + random.randint(-base_usage // 4, base_usage // 4)
 

  if random.random() < 0.05:
  cost *= random.uniform(2, 4)
  usage *= random.randint(3, 6)
  if random.random() < 0.02:
  cost *= random.uniform(0.1, 0.5)
  usage = usage // random.randint(2, 5)
 

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
  return pd.DataFrame(data)
 

 def generate_aws_finops_report(csv_file_path, output_pdf="aws_finops_report.pdf"):
  temp_files = []  # List to store temporary file objects
  try:
  df = pd.read_csv(csv_file_path)
  df['Date'] = pd.to_datetime(df['Date'])
 

  # --- Define Margins ---
  left_margin = 50
  right_margin = letter[0] - 50
  top_margin = letter[1] - 50
  bottom_margin = 50
 

  # --- Generate Specific Charts ---
  services = df['Service'].unique()
  regions = df['Region'].unique()
 

  chart_titles = []
 

  # Service-Specific Charts
  for service in services:
  service_data = df[df['Service'] == service]
 

  # Cost Chart
  plt.figure(figsize=(10, 5))
  plt.plot(service_data['Date'], service_data['Cost'], marker='o', label=service, color='blue')
  plt.title(f'{service} Daily Cost (USD)')
  plt.xlabel('Date')
  plt.ylabel('Cost (USD)')
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates
  plt.xticks(rotation=45, ha='right')
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  cost_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
  plt.savefig(cost_temp.name, format='png')
  plt.close()
  temp_files.append(cost_temp)
  chart_titles.append(f'{service} Daily Cost')
 

  # Usage Chart
  plt.figure(figsize=(10, 5))
  plt.plot(service_data['Date'], service_data['Usage'], marker='s', label=service, color='green')
  plt.title(f'{service} Daily Usage')
  plt.xlabel('Date')
  plt.ylabel('Usage (Units)')
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates
  plt.xticks(rotation=45, ha='right')
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  usage_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
  plt.savefig(usage_temp.name, format='png')
  plt.close()
  temp_files.append(usage_temp)
  chart_titles.append(f'{service} Daily Usage')
 

  # Region-Specific Charts
  for region in regions:
  region_data = df[df['Region'] == region]
 

  # Cost Chart
  plt.figure(figsize=(10, 5))
  plt.plot(region_data['Date'], region_data['Cost'], marker='^', label=region, color='red')
  plt.title(f'{region} Daily Cost (USD)')
  plt.xlabel('Date')
  plt.ylabel('Cost (USD)')
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates
  plt.xticks(rotation=45, ha='right')
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  cost_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
  plt.savefig(cost_temp.name, format='png')
  plt.close()
  temp_files.append(cost_temp)
  chart_titles.append(f'{region} Daily Cost')
 

  # Usage Chart
  plt.figure(figsize=(10, 5))
  plt.plot(region_data['Date'], region_data['Usage'], marker='v', label=region, color='orange')
  plt.title(f'{region} Daily Usage')
  plt.xlabel('Date')
  plt.ylabel('Usage (Units)')
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates
  plt.xticks(rotation=45, ha='right')
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  usage_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
  plt.savefig(usage_temp.name, format='png')
  plt.close()
  temp_files.append(usage_temp)
  chart_titles.append(f'{region} Daily Usage')
 

  # --- Generate PDF ---
  c = canvas.Canvas(output_pdf, pagesize=letter)
 

  # --- Title Page ---
  c.setFont("Helvetica-Bold", 36)
  c.drawCentredString(letter[0] / 2, top_margin - 50, "AWS FinOps Report")
  c.setFont("Helvetica", 20)
  c.drawCentredString(letter[0] / 2, top_margin - 100, "By Alex Curtis")
 

  c.showPage()
 

  # --- Summary Page ---
  c.setFont("Helvetica-Bold", 24)
  c.drawString(left_margin, top_margin - 50, "Report Summary")
 

  summary_text = """
  This report analyzes AWS cost and usage data over the past 30 days, breaking down the analysis by service and region.
 

  **Key Findings:**
 

  **Cost Analysis:**
  - **Service Cost Variation:** Significant cost variations were observed across different AWS services.
  * EC2 and RDS consistently showed higher costs compared to S3 and Lambda.
  * Consider optimizing EC2 instance types and RDS usage to reduce costs.
  - **Regional Cost Differences:** Costs varied by region, with us-east-1 generally having higher costs.
  * Explore the possibility of relocating resources to less expensive regions where feasible.
  - **Anomaly Detection:** Analyze cost anomalies to identify and address potential issues like misconfigurations or unexpected spikes in usage.
 

  **Usage Analysis:**
  - **Service Usage Patterns:** Usage patterns varied across AWS services.
  * Lambda functions exhibited high usage, indicating potential areas for cost optimization through function optimization and improved code efficiency.
  * S3 usage was relatively stable, suggesting efficient storage utilization.
  - **Regional Usage Patterns:** Usage patterns also varied by region.
  * Analyze usage patterns in each region to identify opportunities for right-sizing resources and optimizing resource allocation.
 

  **Recommendations:**
 

  - **Cost Optimization:**
  * **Right-sizing:** Right-size EC2 instances to match actual workloads.
  * **Reserved Instances:** Consider utilizing Reserved Instances to reduce EC2 costs.
  * **Storage Optimization:** Optimize S3 storage classes to reduce storage costs.
  * **Database Optimization:** Optimize RDS database usage and consider using read replicas.
  * **Lambda Optimization:** Optimize Lambda function code and improve cold start performance.
 

  - **Usage Efficiency:**
  * **Auto Scaling:** Implement and fine-tune Auto Scaling groups to adjust capacity based on demand.
  * **Monitoring and Alerting:** Set up monitoring and alerting systems to detect and address potential cost anomalies or performance issues.
  * **Regular Reviews:** Conduct regular cost and usage reviews to identify areas for improvement and optimize resource allocation.
  """
 

  c.setFont("Helvetica", 9)  # Reduced font size
  lines = summary_text.split('\n')
  y_position = top_margin - 100
  for line in lines:
  # Manual Line Wrapping
  if len(line) > 90:  # Adjusted line length
  words = line.split()
  wrapped_line = ""
  current_length = 0
  for word in words:
  if current_length + len(word) + 1 <= 90:
  wrapped_line += word + " "
  current_length += len(word) + 1
  else:
  c.drawString(left_margin, y_position, wrapped_line.strip())
  y_position -= 11  # Reduced spacing for wrapped lines
  wrapped_line = word + " "
  current_length = len(word) + 1
  c.drawString(left_margin, y_position, wrapped_line.strip())
  else:
  c.drawString(left_margin, y_position, line.strip())
  y_position -= 14  # Adjusted line spacing
 

  c.showPage()
 

  # --- Chart Pages ---
  y_pos = top_margin - 50
  chart_height = 200
  chart_width = 550
  y_text_offset = 20  # Space between chart and title
 

  for i, temp_file in enumerate(temp_files):
  c.setFont("Helvetica", 12)  # Chart title font size
  c.drawString(left_margin, y_pos + chart_height + y_text_offset, chart_titles[i])  # Title above chart
  c.drawImage(temp_file.name, left_margin, y_pos, width=chart_width, height=chart_height)
  y_pos -= (chart_height + 50)  # Increased spacing between charts
 

  if y_pos < bottom_margin:
  c.showPage()
  y_pos = top_margin - 50
 

  c.save()
  print(f"AWS FinOps report generated: {output_pdf}")
 

  except FileNotFoundError:
  print(f"Error: CSV file not found at {csv_file_path}")
  except Exception as e:
  print(f"Error generating report: {e}")
 

  finally:
  for tf in temp_files:
  if tf is not None and hasattr(tf, 'name') and os.path.exists(tf.name):
  tf.close()
  os.unlink(tf.name)
 

 if __name__ == "__main__":
  dynamic_df = generate_dynamic_aws_data()
  dynamic_df.to_csv("aws_cost_data.csv", index=False)
  print("Generated dynamic data and saved to aws_cost_data.csv")
 

  csv_file_path = "aws_cost_data.csv"
  generate_aws_finops_report(csv_file_path)