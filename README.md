# Discharge Summary Extraction Agent 

AI-powered system to extract structured clinical information from hospital discharge PDFs using Google Gemini LLM.

---

##  Overview

This project processes multi-page hospital discharge documents and converts them into structured JSON output.  
It uses LLM-based extraction, page classification, and validation layers to ensure accurate and consistent clinical data extraction.

---

##  Features

- Multi-page PDF processing
- Page classification (discharge, lab, medication, nursing, etc.)
- Gemini LLM-based structured extraction
- Evidence-based output (no hallucination)
- Medication extraction and reconciliation
- Conflict detection across pages
- Pending results detection
- Safety validation layer
- Clean merged JSON output

---

##  Architecture

PDF Input  
↓  
Text Extraction (OCR / PDF parser)  
↓  
Page Classification  
↓  
Filtering (remove admin/irrelevant pages)  
↓  
LLM Extraction (Gemini)  
↓  
Pending + Conflict Detection  
↓  
Merge Engine  
↓  
Medication Reconciliation  
↓  
Validation Layer  
↓  
Final Structured JSON Output  

---

##  Project Structure

dscribe-discharge-agent/
│
├── main.py
├── agent.py
│
├── tools/
│   ├── extractor.py
│   ├── page_classifier.py
│   ├── pending_detector.py
│   ├── conflict_checker.py
│   ├── medication_reconciliation.py
│   ├── safety_validator.py
│   ├── trace_logger.py
│
├── .env
├── requirements.txt
└── README.md

---

##  Installation

```bash
git clone https://github.com/your-username/discharge-agent.git
cd discharge-agent

python -m venv .venv
.venv\Scripts\activate   # Windows

pip install -r requirements.txt
