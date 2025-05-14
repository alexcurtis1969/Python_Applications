def export_pdf(df, bar_chart, pie_chart):
    pdf_path = "cloudsavr_cost_optimization_report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "CloudSavr Cost Optimization Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    # Executive Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 110, "Executive Summary & Recommendations")
    c.setFont("Helvetica", 10)

    summary = [
        "CloudSavr's AWS portfolio reveals a significant opportunity for cost optimization, with a potential monthly savings of $287,185.93—representing a 20% reduction in overall spend.",
        "• EC2 & RDS Rightsizing and Reserved Instances: By optimizing resource allocation and committing to Reserved Instances, we can secure $38,658.25 in predictable monthly savings, ensuring more efficient and cost-effective cloud operations.",
        "• S3 Intelligent Tiering & Lifecycle Policies: Implementing data lifecycle management through Intelligent Tiering will drive substantial cost reductions, yielding approximately $39,765.88 in savings per month.",
        "• Automated Scheduling & Idle Resource Decommissioning: By enabling start/stop automation and decommissioning underused EBS volumes, we can unlock $28,718.59 in low-risk, easy-to-execute savings, reducing unnecessary cloud expenditure.",
        "• Redshift & DynamoDB Optimization: Pausing underutilized Redshift clusters and optimizing DynamoDB capacity will contribute to a sustainable, long-term reduction in spend while enhancing operational efficiency across departments."
    ]

    y = height - 140
    for line in summary:
        wrapped_lines = wrap(line, width=90)  # Wrap the text at 90 characters
        for wrapped_line in wrapped_lines:
            c.drawString(50, y, wrapped_line)
            y -= 12
            if y < 50:
                c.showPage()
                y = height - 50
        # Add extra space between bullets
        y -= 10  # Space between bullet points

    # Total savings
    total_savings = df["monthly_savings"].sum()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 40, f"Estimated Monthly Savings: ${total_savings:,.2f}")

    # Charts
    c.drawImage(bar_chart, 50, y - 250, width=500, height=200)
    c.drawImage(pie_chart, 100, y - 450, width=300, height=200)

    c.showPage()

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Detailed Recommendations")
    c.setFont("Helvetica", 10)

    y = height - 80
    for _, row in df.iterrows():
        line = f"- [{row['platform']}] {row['service']} in {row['region']} → {row['action']} → Save ${row['monthly_savings']:.2f}/mo (Risk: {row['risk']})"
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return pdf_path
