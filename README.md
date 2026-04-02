AI-Powered Detailed Diagnostic Report (DDR) Generator
An intelligent building inspection tool that synthesizes visual reports and thermal data to identify hidden structural risks. Built for the Urbanroof Internship Task.

 The Problem & Solution
Property inspections often produce "siloed" data. A visual inspector might miss what a thermal camera sees. This app acts as a Digital Foreman, reading both data streams simultaneously to find contradictions—like a "dry" roof that actually has subsurface moisture.

 Tech Stack
Frontend: Streamlit (Cloud-native deployment)

AI Engine: Llama 3.1 8B Instant via Groq LPU (Optimized for low latency)

PDF Processing: PyMuPDF (MuPDF) for high-fidelity text and image extraction

Report Generation: ReportLab for automated PDF professional formatting

 Key Features
Multimodal Analysis: Processes both textual observations and thermal heat-map images.

Conflict Detection: Specifically engineered to highlight discrepancies between visual and thermal data.

Secure Infrastructure: Implements Streamlit Secrets for encrypted API key management (no hardcoded keys).

High Performance: Powered by Groq's LPU architecture for near-instant report generation.
