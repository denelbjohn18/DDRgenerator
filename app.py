import streamlit as st
import os
import json
from dotenv import load_dotenv

from utils.extractor import process_uploaded_file, extract_content
from utils.processor import analyze_reports
from utils.generator import create_pdf_report

# Ensure we find the .env file in the exact same folder as app.py
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=env_path, override=True)

st.set_page_config(page_title="AI-POWERED DDR GENERATOR", layout="wide")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key missing! Please ensure GOOGLE_API_KEY is set in your .env file.")
    st.stop()

st.sidebar.header("Upload Reports")
inspection_file = st.sidebar.file_uploader("Upload Inspection Report", type=['pdf'])
thermal_file = st.sidebar.file_uploader("Upload Thermal Report", type=['pdf'])

st.title("AI-POWERED DDR GENERATOR")

if "json_result" not in st.session_state:
    st.session_state.json_result = None

if st.button("Process Reports"):
    if not inspection_file or not thermal_file:
        st.error("Please upload both the Inspection Report and Thermal Report.")
    else:
        # Create fresh directories
        os.makedirs("temp_pdfs", exist_ok=True)
        os.makedirs("temp_images", exist_ok=True)
        
        with st.spinner("Processing documents (Extracting text and images from uploaded PDFs)..."):
            insp_path = process_uploaded_file(inspection_file)
            therm_path = process_uploaded_file(thermal_file)
            
            insp_text, insp_images = extract_content(insp_path, "temp_images")
            therm_text, therm_images = extract_content(therm_path, "temp_images")
            
            all_images = insp_images + therm_images
            
        with st.spinner("Analyzing data with Generative AI... this may take some time."):
            try:
                result = analyze_reports(insp_text, therm_text, all_images, api_key)
                st.session_state.json_result = result
                st.success("Analysis complete!")
            except Exception as e:
                st.error(f"Error during AI analysis: {e}")

if st.session_state.json_result:
    st.subheader("Preview Generated Data (JSON)")
    st.write("You can freely edit the JSON data below. The downloaded PDF report natively reflects these changes.")
    
    editable_json_str = st.text_area(
        "Edit JSON Data before PDF Generation", 
        value=json.dumps(st.session_state.json_result, indent=2), 
        height=400
    )
    
    if st.button("Generate and Download Final DDR"):
        try:
            final_json = json.loads(editable_json_str)
            pdf_path = create_pdf_report(final_json)
            
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF Report",
                    data=f.read(),
                    file_name="Detailed_Diagnostic_Report.pdf",
                    mime="application/pdf"
                )
            st.success("Report generated successfully! Click download above.")
        except json.JSONDecodeError:
            st.error("Invalid JSON format in the text area. Please correct it to generate the report.")
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
