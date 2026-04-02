from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

def create_pdf_report(json_data, output_path="Final_DDR_Report.pdf"):
    """
    Takes structured JSON data and builds a PDF report using ReportLab.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Title']
    story.append(Paragraph("Detailed Diagnostic Report", title_style))
    story.append(Spacer(1, 12))

    # Summary
    h2_style = styles['Heading2']
    normal_style = styles['Normal']
    
    story.append(Paragraph("Property Issue Summary", h2_style))
    story.append(Paragraph(json_data.get("Property_Issue_Summary", "Not Available"), normal_style))
    story.append(Spacer(1, 12))

    # Observations
    story.append(Paragraph("Area-wise Observations", h2_style))
    for obs in json_data.get("Area_wise_Observations", []):
        story.append(Paragraph(f"<b>Area:</b> {obs.get('Area', 'Unknown')}", normal_style))
        story.append(Paragraph(f"<b>Observation:</b> {obs.get('Observation', 'Not Available')}", normal_style))
        
        img_path = obs.get("Image_Path")
        if img_path and str(img_path).lower() != "null":
            if os.path.exists(img_path):
                # Calculate simple scale (max width 400 points to keep it visible but fitting)
                try:
                    # Creating the reportlab image
                    # For a safer layout scale, we provide max width and let height auto calculated if PIL used
                    # But Reportlab image takes absolute. 288 points = 4 inches width.
                    img = RLImage(img_path, width=288, height=216)
                    img.hAlign = 'CENTER'
                    story.append(Spacer(1, 6))
                    story.append(img)
                except Exception as e:
                    story.append(Paragraph(f"<i>Error loading image: {e}</i>", normal_style))
            else:
                story.append(Paragraph("<i>Image Not Available (File not found on server)</i>", normal_style))
        else:
            story.append(Paragraph("<i>Image Not Available</i>", normal_style))
        story.append(Spacer(1, 12))

    # Subsections
    story.append(Paragraph("Probable Root Cause", h2_style))
    story.append(Paragraph(json_data.get("Probable_Root_Cause", "Not Available"), normal_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Severity Assessment", h2_style))
    severity = json_data.get("Severity_Assessment", {})
    story.append(Paragraph(f"<b>Level:</b> {severity.get('Level', 'Not Available')}", normal_style))
    story.append(Paragraph(f"<b>Reasoning:</b> {severity.get('Reasoning', 'Not Available')}", normal_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Recommended Actions", h2_style))
    for act in json_data.get("Recommended_Actions", []):
        story.append(Paragraph(f"• {act}", normal_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Additional Notes", h2_style))
    story.append(Paragraph(json_data.get("Additional_Notes", "Not Available"), normal_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Missing or Unclear Information", h2_style))
    story.append(Paragraph(json_data.get("Missing_or_Unclear_Information", "Not Available"), normal_style))
    story.append(Spacer(1, 12))

    doc.build(story)
    return output_path
