import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import medical_parser
from vector_db import get_vector_db  # Importing our vector database engine

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Configure page settings
st.set_page_config(page_title="MediRAG AI", page_icon="🩺", layout="centered")

st.title("🩺 MediRAG - Medical Report Analyzer")
st.write("Upload your medical lab report (PDF) for an AI summary, OR ask a general medical question below.")

# Initialize Vector Database (ChromaDB)
vector_db = get_vector_db()

# ---------------------------------------------------------
# SESSION MEMORY STATE
# ---------------------------------------------------------
if 'report_text' not in st.session_state:
    st.session_state.report_text = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""

if groq_api_key:
    # Initialize Groq Client
    client = Groq(api_key=groq_api_key)

    # ---------------------------------------------------------
    # SETTINGS: LANGUAGE SELECTOR
    # ---------------------------------------------------------
    st.markdown("### ⚙️ Settings")
    selected_language = st.selectbox(
        "Choose Output Language:",
        ("English", "Hindi", "Hinglish")
    )
    st.markdown("---")

    # ---------------------------------------------------------
    # PART 1: FILE UPLOAD & ANALYSIS (RAG Enhanced)
    # ---------------------------------------------------------
    st.markdown("### 📄 Analyze Medical Report")
    uploaded_file = st.file_uploader("Upload Lab Report (PDF)", type=["pdf"])

    if uploaded_file is not None:
        st.success(f"✅ File '{uploaded_file.name}' successfully uploaded!")

        if st.button("Analyze Medical Report"):
            with st.spinner("Extracting data and retrieving RAG medical context... Please wait."):
                try:
                    extracted_text = medical_parser.extract_text_from_pdf(uploaded_file)

                    if "Error" in extracted_text:
                        st.error(extracted_text)
                    else:
                        optimized_text = extracted_text[:15000]

                        # RAG STEP: Retrieve relevant medical knowledge from ChromaDB based on report text
                        rag_context = vector_db.search_medical_context(optimized_text, n_results=2)

                        if selected_language == "Hindi":
                            lang_instruction = "STRICT INSTRUCTION: The entire response MUST be in pure Hindi language written in Devanagari script."
                        elif selected_language == "Hinglish":
                            lang_instruction = "STRICT INSTRUCTION: The entire response MUST be in Hinglish (a mix of Hindi and English written in Latin script)."
                        else:
                            lang_instruction = "STRICT INSTRUCTION: The entire response MUST be in professional medical English."

                        ai_prompt = f"""
                        You are an expert medical AI assistant utilizing a Retrieval-Augmented Generation (RAG) framework. 
                        I am providing you with extracted text from a patient's lab report and retrieved standard medical guidelines from the database.

                        {lang_instruction}

                        Please analyze the report using the provided medical context and give:
                        1. A simple summary of the report.
                        2. Any abnormal values (highlighted and explained).
                        3. Basic lifestyle/diet recommendations based on standard medical guidelines.

                        Retrieved Medical Knowledge (RAG Context):
                        {rag_context}

                        Patient Lab Report Text:
                        {optimized_text}
                        """

                        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are a highly intelligent and professional RAG-powered medical assistant."
                                },
                                {
                                    "role": "user",
                                    "content": ai_prompt,
                                }
                            ],
                            model="openai/gpt-oss-20b",
                        )

                        ai_text = chat_completion.choices[0].message.content

                        st.session_state.summary = ai_text
                        st.session_state.report_text = optimized_text
                        st.rerun()

                except Exception as e:
                    st.error(f"System Error: {e}")

    # SHOW REPORT SUMMARY & REPORT SPECIFIC Q&A (RAG Enhanced)
    if st.session_state.summary != "":
        st.markdown("### 📊 AI Analysis Report (RAG Powered)")
        st.write(st.session_state.summary)

        st.markdown("---")

        st.markdown("### 💬 Ask Questions About Your Report")
        user_question = st.text_input("Ask any question related to your uploaded report:")

        if st.button("Ask Question (Report)"):
            if user_question:
                with st.spinner("Searching vector database and generating answer..."):
                    try:
                        # RAG STEP: Search vector database using the user's specific question
                        rag_qa_context = vector_db.search_medical_context(user_question, n_results=2)

                        qa_prompt = f"""
                        You are a helpful and expert medical AI assistant using a RAG architecture. 
                        Use the retrieved medical guidelines and the patient's report text to answer the user's question accurately.

                        Answer in the same language the user asked the question.
                        Add a disclaimer that you are an AI and they should consult a doctor.

                        Retrieved Medical Guidelines:
                        {rag_qa_context}

                        User Question: {user_question}
                        Medical Report Text: {st.session_state.report_text}
                        """

                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "You are a medical RAG assistant."},
                                {"role": "user", "content": qa_prompt}
                            ],
                            model="openai/gpt-oss-20b",
                        )

                        answer = chat_completion.choices[0].message.content
                        st.success("✅ **AI Answer (Powered by ChromaDB RAG):**")
                        st.info(answer)
                    except Exception as e:
                        st.error(f"System Error: {e}")

    st.markdown("---")

    # ---------------------------------------------------------
    # PART 2: GENERAL MEDICAL CHAT (RAG Enhanced)
    # ---------------------------------------------------------
    st.markdown("### 🧠 General Medical Query")
    general_question = st.text_input("Ask a general medical question (e.g., What are the symptoms of Dengue?):")

    if st.button("Ask General Question"):
        if general_question:
            with st.spinner("Searching knowledge base..."):
                try:
                    # RAG STEP: Search vector DB for general query
                    rag_general_context = vector_db.search_medical_context(general_question, n_results=2)

                    if selected_language == "Hindi":
                        gen_lang = "Reply in pure Hindi."
                    elif selected_language == "Hinglish":
                        gen_lang = "Reply in Hinglish (Latin script)."
                    else:
                        gen_lang = "Reply in professional English."

                    gen_prompt = f"""
                    You are a helpful medical assistant using a RAG knowledge base. Answer the user's general medical question using the provided context and your expertise.
                    {gen_lang}
                    Include a disclaimer that you are an AI and they should consult a real doctor for serious issues.

                    Retrieved Knowledge Base Context:
                    {rag_general_context}

                    Question: {general_question}
                    """

                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a medical RAG assistant."},
                            {"role": "user", "content": gen_prompt}
                        ],
                        model="openai/gpt-oss-20b",
                    )

                    answer = chat_completion.choices[0].message.content
                    st.success("✅ **AI General Answer (RAG Powered):**")
                    st.info(answer)

                except Exception as e:
                    st.error(f"System Error: {e}")
        else:
            st.warning("Please type a question first.")
else:
    st.error("Authentication Error: GROQ_API_KEY missing. Please check your .env configuration.")
