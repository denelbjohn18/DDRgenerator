# AI-Powered DDR Generator

A full-stack application that ingests Inspection and Thermal report PDFs, leverages Gemini 1.5 Flash to intelligently extract and merge details (including images), and generates a professional Detailed Diagnostic Report (DDR) as a downloadable PDF.

## Setup Instructions

1. **Clone and Enter Directory**
   \`\`\`bash
   git clone <your-repository-url>
   cd DDRgenerator
   \`\`\`

2. **Setup Virtual Environment (Recommended)**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install Dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Environment Variables**
   - Open the `.env` file.
   - Insert your Google API Key: `GOOGLE_API_KEY="your_api_key_here"`

5. **Run the Application**
   \`\`\`bash
   streamlit run app.py
   \`\`\`
# DDRgenerator
