import os
import json
from PIL import Image
import google.generativeai as genai
import streamlit as st

# 1. Explicitly pull the key from Streamlit Secrets
# 2. Configure WITHOUT any api_version or ClientOptions
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Initialize the model using the stable production string
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def analyze_reports(inspection_text, thermal_text, image_paths, api_key):
    """
    Sends extracted data to Gemini to generate structured JSON.
    """
    # Enforce JSON output during generation
    generation_config = {
        "response_mime_type": "application/json",
        "temperature": 0.2,
    }
    
    prompt = f"""
    You are a Senior AI Application Engineer acting as an expert Diagnostic Report Analyst.
    You are provided with text extracted from two reports:
    1. Inspection Report
    2. Thermal Report
    
    You are also provided with a set of images extracted from these reports.
    
    Your task is to merge the data from both reports logically into a clear, professional Detailed Diagnostic Report (DDR).
    
    **CRITICAL BUSINESS RULES:**
    - Merge data from both reports logically.
    - Do NOT invent facts; use "Not Available" if information is missing.
    - Explicitly mention any conflicts between the Inspection and Thermal data (e.g., if one says an issue exists and the other says it doesn't).
    - Use simple, client-friendly language. Avoid unnecessary technical jargon.
    - Below, you will see a list of provided images with their paths. You MUST assign the `Image_Path` to each observation that matches the most relevant image based on the context of the image and the observation. 
    - If no image securely matches the observation, set `Image_Path` to `null`.
    
    Here is the schema your JSON response MUST strictly follow:
    {{
      "Property_Issue_Summary": "string",
      "Area_wise_Observations": [
        {{
          "Area": "string",
          "Observation": "string",
          "Image_Path": "string or null"
        }}
      ],
      "Probable_Root_Cause": "string",
      "Severity_Assessment": {{
        "Level": "Low/Medium/High/Critical",
        "Reasoning": "string"
      }},
      "Recommended_Actions": ["string", "string"],
      "Additional_Notes": "string",
      "Missing_or_Unclear_Information": "string"
    }}
    
    ### DATA INPUT ###
    **INSPECTION REPORT TEXT:**
    {inspection_text}
    
    **THERMAL REPORT TEXT:**
    {thermal_text}
    
    **IMAGES AVAILABLE:**
    {', '.join(image_paths)}
    """
    
    # We construct the multimodal content block
    content = [prompt]
    
    # Add image objects directly
    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            # Add context for the model so it knows the identifier of the image
            content.append(f"Image associated with path: {img_path}")
            content.append(img)
        except Exception as e:
            print(f"Skipping generation for image {img_path}: {e}")
            
    response = model.generate_content(content, generation_config=generation_config)
    
    # Clean possible markdown wrap from the response, strictly parse JSON
    try:
        response_text = response.text.replace("```json", "").replace("```", "")
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Gemini response as JSON: {e}\nRaw Response: {response.text}")
