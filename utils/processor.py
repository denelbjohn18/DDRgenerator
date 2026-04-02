import os
import json
import time
import streamlit as st
from groq import Groq


def analyze_reports(inspection_text, thermal_text, image_paths, api_key):
    """
    Sends extracted report data to Groq (Llama 3.1) for structured JSON analysis.
    Includes timeout handling and retry logic so the UI never hangs.
    """
    # --- API Key Resolution (env → passed arg) ---
    resolved_key = None

    # 1. Environment variable (works for both local .env and Streamlit Cloud)
    env_val = os.getenv("GROQ_API_KEY")
    if env_val:
        resolved_key = env_val.replace('"', '').strip()

    # 2. Passed argument fallback
    if not resolved_key and api_key:
        resolved_key = str(api_key).replace('"', '').strip()

    if not resolved_key:
        raise ValueError(
            "No Groq API key found. "
            "Set GROQ_API_KEY in Streamlit secrets or your .env file."
        )

    # --- Client & Model Setup ---
    client = Groq(api_key=resolved_key)
    model_name = "llama-3.1-8b-instant"

    # --- Build the prompt ---
    prompt = f"""
You are provided with text extracted from two building reports:
1. **Inspection Report**
2. **Thermal Report**

You are also given a list of image file paths extracted from these reports.

Your task is to merge the data from both reports logically into a clear, professional
Detailed Diagnostic Report (DDR).

**CRITICAL BUSINESS RULES:**
- Merge data from both reports logically.
- Do NOT invent facts; use "Not Available" if information is missing.
- Explicitly mention any conflicts between the Inspection and Thermal data
  (e.g., if one says an issue exists and the other says it doesn't).
- Use simple, client-friendly language. Avoid unnecessary technical jargon.
- You MUST assign the `Image_Path` to each observation that matches the most
  relevant image based on the context of the observation and the image filename.
- If no image clearly matches the observation, set `Image_Path` to `null`.

Your response MUST be valid JSON strictly following this schema (no markdown fences):
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

**IMAGE PATHS AVAILABLE:**
{', '.join(image_paths) if image_paths else 'None'}
"""

    system_message = (
        "You are a Senior Building Diagnostic Expert. "
        "Your task is to analyze visual inspection text and thermal image data "
        "to identify structural conflicts and safety risks."
    )

    print(f"[DDR] Sending request to Groq ({model_name}) with {len(image_paths)} image refs...")

    # --- Retry logic (up to 3 attempts with exponential back-off) ---
    max_retries = 3
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[DDR] Attempt {attempt}/{max_retries}...")
            chat_completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=4096,
                response_format={"type": "json_object"},
            )

            raw_text = chat_completion.choices[0].message.content
            # Strip any accidental markdown fences
            response_text = raw_text.replace("```json", "").replace("```", "").strip()
            result = json.loads(response_text)
            print(f"[DDR] Successfully received and parsed response on attempt {attempt}.")
            return result

        except json.JSONDecodeError as e:
            raise Exception(
                f"Failed to parse Groq response as JSON: {e}\n"
                f"Raw Response: {raw_text}"
            )
        except Exception as e:
            last_error = e
            print(f"[DDR] Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                wait_time = 2 ** attempt  # 2s, 4s
                print(f"[DDR] Retrying in {wait_time}s...")
                time.sleep(wait_time)

    raise Exception(
        f"Groq API failed after {max_retries} attempts. Last error: {last_error}"
    )
