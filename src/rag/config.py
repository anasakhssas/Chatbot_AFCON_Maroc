"""
Configuration pour le système RAG du Chatbot CAN 2025
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

class RAGConfig:
    """Configuration centralisée pour le RAG"""
    
    # Chemins
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    TRANSFORMED_DIR = DATA_DIR / "transformed"
    COMBINED_DATASET = TRANSFORMED_DIR / "combined_dataset.json"
    CHROMA_DB_DIR = BASE_DIR / "chroma_db"
    
    # Groq Configuration (API GRATUITE!)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Modèle LLM Groq (ultra-rapide et gratuit)
    LLM_MODEL = "llama-3.3-70b-versatile"  # Nouveau modèle (Jan 2025) - Alternatives: mixtral-8x7b-32768, llama-3.1-8b-instant
    LLM_TEMPERATURE = 0.0  # Pour des réponses plus précises
    
    # Embeddings Open Source (100% gratuit, fonctionne en local)
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"  # Support français
    # Alternative: "sentence-transformers/all-MiniLM-L6-v2" (plus rapide, anglais)
    
    # ChromaDB Configuration
    COLLECTION_NAME = "can2025_news"
    COLLECTION_METADATA = {
        "description": "CAN 2025 Morocco - News, matches, and statistics",
        "language": "fr",
        "tournament": "Africa Cup of Nations 2025"
    }
    
    # RAG Parameters
    CHUNK_SIZE = 1000  # Taille des chunks pour le découpage de texte
    CHUNK_OVERLAP = 200  # Chevauchement entre chunks
    TOP_K_RESULTS = 3  # Nombre de documents à récupérer
    MAX_TOKENS = 500  # Tokens maximum pour la réponse
    
    # Prompt Template
    SYSTEM_PROMPT = """Tu es un assistant expert sur la Coupe d'Afrique des Nations (CAN) 2025 organisée au Maroc.

Ton rôle :
- Répondre aux questions sur les matchs, équipes, joueurs et statistiques de la CAN 2025
- Utiliser UNIQUEMENT les informations fournies dans le contexte
- Si l'information n'est pas dans le contexte, dire "Je n'ai pas cette information dans ma base de données"
- Répondre en français de manière claire et concise
- Citer les sources quand c'est pertinent (date, équipes, score)

Contexte disponible :
{context}

Question : {question}

Réponse :"""
    
    QUERY_PROMPT = """Réponds à la question suivante en utilisant UNIQUEMENT le contexte fourni.
Si tu ne trouves pas la réponse dans le contexte, dis-le clairement.

Contexte :
{context}

Question : {question}

Réponse :"""
    
    @classmethod
    def validate(cls):
        """Valider la configuration"""
        errors = []
        
        if not cls.GROQ_API_KEY:
            errors.append("❌ GROQ_API_KEY n'est pas définie dans les variables d'environnement")
            errors.append("   👉 Obtenir gratuitement sur : https://console.groq.com/keys")
        
        if not cls.COMBINED_DATASET.exists():
            errors.append(f"❌ Dataset combiné introuvable : {cls.COMBINED_DATASET}")
        
        return errors
    
    @classmethod
    def print_config(cls):
        """Afficher la configuration actuelle"""
        print("\n" + "="*60)
        print("⚙️  CONFIGURATION RAG - CAN 2025 CHATBOT")
        print("="*60)
        print(f"\n📂 Chemins :")
        print(f"   Dataset        : {cls.COMBINED_DATASET}")
        print(f"\n🤖 Modèles :")
        print(f"   Embeddings     : {cls.EMBEDDING_MODEL}")
        print(f"   LLM (Groq)     : {cls.LLM_MODEL}")
        print(f"   Température    : {cls.LLM_TEMPERATURE}")
        print(f"\n🔍 Paramètres RAG :")
        print(f"   Top K résultats: {cls.TOP_K_RESULTS}")
        print(f"   Max tokens     : {cls.MAX_TOKENS}")
        print(f"   Chunk size     : {cls.CHUNK_SIZE}")
        print(f"\n🔑 API Key :")
        if cls.GROQ_API_KEY:
            print(f"   Groq (GRATUIT) : {'*' * 10}{cls.GROQ_API_KEY[-4:]}")
        else:
            print(f"   Groq           : ❌ Non configurée")
            print(f"   👉 Obtenir sur : https://console.groq.com/keys")
            print(f"   OpenAI         : ❌ Non configurée")
        print("="*60 + "\n")
