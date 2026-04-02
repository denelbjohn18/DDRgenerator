# AI-Powered Detailed Diagnostic Report (DDR) Generator

An advanced full-stack application designed to automate the synthesis of property inspection data. This system ingests separate **Visual Inspection** and **Infrared Thermal** PDF reports, leverages **Gemini 1.5 Flash** to identify data conflicts and hidden issues, and generates a professional, consolidated **Detailed Diagnostic Report (DDR)**.

## Key Features

* **Multimodal Data Extraction:** Automatically extracts text and embedded thermal images from PDF documents using `PyMuPDF`.
* **Intelligent Synthesis:** Uses LLM logic to compare visual observations against thermal data (e.g., detecting sub-surface moisture where a visual check saw "no issues").
* **Automated PDF Generation:** Programmatically builds a structured, high-quality DDR including mapped images, severity assessments, and root cause analysis.
* **Modern Web UI:** A clean, dark-themed Streamlit interface for seamless file uploads and report processing.

## Tech Stack

* **Language:** Python 3.9+
* **AI Model:** Google Gemini 1.5 Flash
* **Frontend:** Streamlit
* **PDF Processing:** PyMuPDF (fitz) & ReportLab
* **Environment Management:** Python-dotenv

