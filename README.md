# MediRAG 🏥
**An AI-Powered Clinical Report Analyzer using Retrieval-Augmented Generation (RAG).**

### 🚀 Built for IBM Z Datathon 2026
**Team:** Backbench Coders

### 💡 The Problem We Are Solving
Patients often struggle to understand complex pathology reports (like CBC or LFT). Uploading these reports to public AI models creates massive data privacy risks (PHI leakage), and standard LLMs often hallucinate medical facts. 

### 🛡️ Our Solution
MediRAG is a secure, hallucination-free application that extracts text from medical PDFs and uses a strictly controlled RAG pipeline to answer patient queries based ONLY on verified medical guidelines. 

### 🛠️ Core Tech Stack
- **Frontend & Backend:** Streamlit (Native Python)
- **AI Inference Engine:** Groq API (gpt-oss-20b)
- **Embeddings:** Sentence-Transformers (all-MiniLM-L6-v2)
- **Vector Database:** Custom Pure Python In-Memory Vector Search (Scikit-Learn)
- **Cloud Infrastructure:** IBM Ecosystem Ready 

---
*(Note: Full source code, deployment scripts, and modular files will be pushed during the active coding phase of the Datathon.)*
