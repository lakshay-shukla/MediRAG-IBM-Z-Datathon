import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class MedicalVectorDB:
    def __init__(self):
        """
        Initialize lightweight Pure Python Vector Search using SentenceTransformers & Scikit-Learn.
        """
        # Load a fast and efficient local embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Foundational medical knowledge base
        self.documents = [
            "Anemia or low hemoglobin indicates a deficiency of red blood cells or iron. Recommended diet includes iron-rich foods like spinach, beetroot, pomegranates, dates, apples, and vitamin C to enhance absorption.",
            "High blood sugar (hyperglycemia) or diabetes requires strict carbohydrate control, avoiding refined sugars, regular physical exercise, and incorporating fiber-rich green leafy vegetables, whole grains, and protein.",
            "High cholesterol (dyslipidemia) management involves reducing saturated fats, avoiding fried or junk foods, increasing omega-3 fatty acids (fish, walnuts, flaxseeds), oats, and regular cardio exercise.",
            "White Blood Cell (WBC) count abnormalities: High WBC usually indicates an active bacterial or viral infection or inflammation. Low WBC can suggest a weak immune system or bone marrow suppression.",
            "Platelet count (thrombocytopenia): Low platelets can lead to bruising or bleeding risks (common in dengue or viral infections). Hydration, papaya leaf extract, and medical supervision are recommended."
        ]

        # Pre-compute embeddings for documents in memory
        self.doc_embeddings = self.model.encode(self.documents)

    def search_medical_context(self, query: str, n_results: int = 2):
        """
        Computes cosine similarity between user query and medical documents to retrieve best context.
        """
        try:
            # Encode incoming query text
            query_embedding = self.model.encode([query])

            # Calculate cosine similarity
            similarities = cosine_similarity(query_embedding, self.doc_embeddings)[0]

            # Get top N matching document indices
            top_indices = np.argsort(similarities)[::-1][:n_results]

            retrieved_docs = [self.documents[i] for i in top_indices]
            return "\n".join(retrieved_docs)
        except Exception as e:
            return f"Error retrieving medical context: {str(e)}"


# PRO-FIX: Yeh decorator model ko cache (memory) me lock kar dega taaki app fast chale
@st.cache_resource
def get_vector_db():
    return MedicalVectorDB()