# MediRAG: An AI-Powered Clinical Report Analyzer using RAG

**Team Name:** Backbench Coders

**Built for IBM Z Datathon 2026**  
**Event Code:** SSF2026  
**Track/Theme:** AI Secured: Innovation Without Exposure  

## 📌 Project Overview
Healthcare language barriers and complex medical terminology often prevent patients from fully understanding their lab reports. **MediRAG** is a highly secure, Multilingual Medical Report Analyzer and Health Assistant. It allows users to upload medical reports and instantly receive simplified, highlighted summaries in their preferred language (English, Hindi, or Hinglish). 

With a strong focus on **Data Privacy**, MediRAG processes all sensitive patient data completely in-memory on the **IBM LinuxONE** environment, ensuring zero data retention and zero AI hallucinations.

## ✨ Key Features
- **Highly Secure Processing:** Built for the IBM Z / LinuxONE ecosystem. No patient files are permanently stored.
- **Multilingual Support:** Breaks the language barrier. Patients can select their preferred language before analysis.
- **Instant Report Summarization:** Automatically highlights abnormal (high/low) lab values.
- **Dedicated Report Chatbox:** Ask specific questions related to the uploaded pathology report.
- **General Health Assistant:** A separate, secure chatbox for everyday health queries based on verified medical guidelines.

## 🛠️ Technology Stack
- **Frontend & App Framework:** Python, Streamlit
- **AI & RAG Pipeline:** Retrieval-Augmented Generation (RAG), ChromaDB, Groq API (for high-speed AI inference)
- **Infrastructure & Deployment:** IBM LinuxONE Community Cloud (Ubuntu 24.04 Virtual Server)

## 🚀 How to Run the Project

### 1. Running on IBM LinuxONE (Live Deployment)
This project is officially deployed on an IBM LinuxONE virtual server.
- **Access the Live App:** `http://148.100.112.38:8501`

**Deployment Steps on Server:**
```bash
# Clone the repository
git clone https://github.com/lakshay-shukla/MediRAG-IBM-Z-Datathon.git
cd MediRAG-IBM-Z-Datathon

# Set up virtual environment
python3 -m venv medienv
source medienv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 -m streamlit run app.py
```

### 2. Running Locally (For Testing)
```bash
git clone https://github.com/lakshay-shukla/MediRAG-IBM-Z-Datathon.git
cd MediRAG-IBM-Z-Datathon
pip install -r requirements.txt
streamlit run app.py
```

## 👥 Team Members (Backbench Coders)
- **Lakshay Shukla** - Team Leader | Backend & RAG Architect
- **Vaishali Chauhan** - Frontend Dev | Report Analysis Module
- **Shikha Chauhan** - Cloud & UI Dev | General Chat & Deployment
- **Prachi Diwakar** - Data Engineer | Parser Logic Specialist

---
*Disclaimer: This project is developed solely for the IBM Z Datathon 2026. The AI advice provided should not replace professional medical consultation.*
