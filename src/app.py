"""
Interface Web Streamlit pour le Chatbot CAN 2025
"""

import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

from src.rag.chatbot import ChatbotCAN2025
from src.rag.config import RAGConfig
import logging

# Configuration de la page
st.set_page_config(
    page_title="Chatbot CAN 2025 Maroc",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé amélioré
st.markdown("""
<style>
    /* Variables de couleurs Maroc */
    :root {
        --maroc-red: #C1272D;
        --maroc-green: #006233;
        --maroc-gold: #FFD700;
    }
    
    /* Header principal */
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #C1272D 0%, #006233 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideDown 0.5s ease-out;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    
    /* Messages de chat */
    .stChatMessage {
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        animation: fadeIn 0.3s ease-in;
    }
    
    /* Expanders pour les sources */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: 600;
        color: #006233;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #e9ecef;
    }
    
    /* Boutons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Métriques */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: #C1272D;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Input de chat */
    .stChatInputContainer {
        border-top: 2px solid #006233;
        padding-top: 1rem;
    }
    
    /* Badges et tags */
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-match {
        background-color: #C1272D;
        color: white;
    }
    
    .badge-news {
        background-color: #006233;
        color: white;
    }
    
    .badge-stats {
        background-color: #FFD700;
        color: #333;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Loading spinner personnalisé */
    .stSpinner > div {
        border-top-color: #C1272D !important;
    }
    
    /* Footer stats */
    .footer-stats {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Amélioration des codes */
    code {
        background-color: #f8f9fa;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        color: #C1272D;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_resource
def init_chatbot():
    """Initialise le chatbot (cached pour ne pas recharger à chaque interaction)"""
    try:
        # Étape 1: Vérifier et exécuter le pipeline ETL si nécessaire
        from src.pipeline.auto_pipeline import AutoPipeline
        
        with st.spinner("🔄 Vérification du pipeline de données..."):
            pipeline = AutoPipeline()
            success, message = pipeline.ensure_ready(force_refresh=False)
            
            if not success:
                st.error(f"❌ Échec du pipeline: {message}")
                return None
            
            st.success(f"✅ {message}")
        
        # Étape 2: Initialiser le chatbot
        with st.spinner("🤖 Initialisation du chatbot RAG..."):
            chatbot = ChatbotCAN2025()
            return chatbot
            
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation : {str(e)}")
        logger.exception("Erreur détaillée:")
        return None


def display_sources(sources):
    """Affiche les sources de manière élégante et moderne dans un expander"""
    if sources:
        with st.expander(f"📚 Voir les {len(sources)} sources utilisées", expanded=False):
            for i, source in enumerate(sources, 1):
                # Gérer à la fois les objets Document et les dictionnaires
                if isinstance(source, dict):
                    metadata = source
                    title = metadata.get('title', 'Document')
                    category = metadata.get('category', 'N/A')
                    date = metadata.get('date', 'N/A')
                    source_name = metadata.get('source', 'N/A')
                    content = metadata.get('excerpt', '')
                else:
                    # C'est un objet Document
                    metadata = source.metadata
                    title = metadata.get('title', 'Document')
                    category = metadata.get('category', 'N/A')
                    date = metadata.get('date', 'N/A')
                    source_name = metadata.get('source', 'N/A')
                    content = source.page_content
                
                # Badge de catégorie coloré
                category_class = "badge-match" if "match" in category.lower() else \
                               "badge-stats" if "stat" in category.lower() else "badge-news"
                
                # Séparateur entre sources
                if i > 1:
                    st.markdown("---")
                
                # En-tête de la source
                st.markdown(f"**📄 Source {i}:** {title}")
                st.markdown(f'<span class="category-badge {category_class}">{category.upper()}</span>', 
                          unsafe_allow_html=True)
                
                # Informations en colonnes
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"📅 {date}")
                with col2:
                    st.caption(f"🌐 {source_name}")
                with col3:
                    st.caption(f"🔢 Rang: {i}/3")
                
                # Contenu avec limitation
                preview = content[:400] + "..." if len(content) > 400 else content
                st.info(preview)


def main():
    # Header amélioré avec émojis animés
    st.markdown("""
    <div class="main-header">
        <h1>⚽ Chatbot CAN 2025 - Maroc 🇲🇦</h1>
        <p>Assistant intelligent pour la Coupe d'Afrique des Nations 2025</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">
            🤖 Propulsé par Groq AI • 📚 RAG avec LangChain • 🔍 ChromaDB
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar améliorée
    with st.sidebar:
        # Logo et titre
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Flag_of_Morocco.svg/320px-Flag_of_Morocco.svg.png", 
                     width=80)
        with col2:
            st.markdown("### CAN 2025")
            st.caption("Chatbot IA")
        
        st.markdown("---")
        
        # Section À propos avec icônes
        st.markdown("## 🤖 Technologie")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <div style="margin: 0.5rem 0;">
                <strong>🧠 LLM:</strong> Groq (llama-3.3-70b)<br>
                <small style="color: #666;">Ultra-rapide, 100% gratuit</small>
            </div>
            <div style="margin: 0.5rem 0;">
                <strong>📚 RAG:</strong> LangChain + ChromaDB<br>
                <small style="color: #666;">Recherche sémantique avancée</small>
            </div>
            <div style="margin: 0.5rem 0;">
                <strong>🔍 Embeddings:</strong> HuggingFace<br>
                <small style="color: #666;">Multilingue (FR/AR/EN)</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistiques en temps réel
        st.markdown("## 📊 Statistiques")
        config = RAGConfig()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents", "20", delta="Actif", delta_color="normal")
        with col2:
            st.metric("Sources", "3", delta="Par réponse", delta_color="off")
        
        st.metric("Modèle LLM", config.LLM_MODEL.split('-')[0].upper())
        st.progress(100, text="✅ Système opérationnel")
        
        st.markdown("---")
        
        # Actions du pipeline
        st.markdown("## 🔄 Actions")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            refresh_button = st.button("🔄 Rafraîchir", use_container_width=True, type="primary")
        with col2:
            if st.button("ℹ️", use_container_width=True):
                st.info("Régénère les données : extraction → transformation → vectorisation")
        
        if refresh_button:
            from src.pipeline.auto_pipeline import AutoPipeline
            with st.spinner("🔄 Régénération complète..."):
                pipeline = AutoPipeline()
                success, message = pipeline.ensure_ready(force_refresh=True)
                if success:
                    st.success(f"✅ {message}")
                    st.cache_resource.clear()
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        st.markdown("---")
        
        # Questions prédéfinies avec catégories
        st.markdown("### 💡 Questions rapides")
        
        # Onglets pour catégories
        tab1, tab2, tab3 = st.tabs(["⚽ Matchs", "🏆 Stats", "📰 Actu"])
        
        with tab1:
            questions_matchs = [
                "Qui a marqué pour le Maroc ?",
                "Résultat Égypte vs Zimbabwe",
                "Prochain match du Maroc"
            ]
            for q in questions_matchs:
                if st.button(q, key=f"match_{q}", use_container_width=True):
                    st.session_state.example_question = q
        
        with tab2:
            questions_stats = [
                "Meilleur buteur du tournoi",
                "Classement Groupe E",
                "Statistiques Riyad Mahrez"
            ]
            for q in questions_stats:
                if st.button(q, key=f"stat_{q}", use_container_width=True):
                    st.session_state.example_question = q
        
        with tab3:
            questions_actu = [
                "Équipes en huitièmes",
                "Arbitres du tournoi",
                "Lieu et dates CAN 2025"
            ]
            for q in questions_actu:
                if st.button(q, key=f"actu_{q}", use_container_width=True):
                    st.session_state.example_question = q
        
        st.markdown("---")
        
        # Aide rapide
        with st.expander("❓ Aide"):
            st.markdown("""
            **Comment utiliser :**
            1. Tapez votre question en français
            2. Le chatbot recherche dans 20 documents
            3. Réponse générée avec sources
            
            **Exemples de questions :**
            - "Score du match X contre Y"
            - "Qui est le meilleur buteur ?"
            - "Quand joue le Maroc ?"
            """)
        
        # Footer avec crédits
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #666;">
            <p>Développé avec ❤️</p>
            <p>© 2025 CAN Maroc</p>
        </div>
        """, unsafe_allow_html=True)

    # Initialisation du chatbot
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = init_chatbot()
    
    if st.session_state.chatbot is None:
        st.error("❌ Impossible d'initialiser le chatbot. Vérifiez votre configuration.")
        st.info("💡 Vérifiez que le fichier `.env` contient votre `GROQ_API_KEY`")
        st.stop()

    # Initialisation de l'historique
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Message de bienvenue
        st.session_state.messages.append({
            "role": "assistant",
            "content": """👋 Bienvenue ! Je suis votre assistant IA pour la CAN 2025 au Maroc.

**Je peux vous renseigner sur :**
- ⚽ Résultats des matchs et buteurs
- 📊 Statistiques et classements
- 📅 Calendrier et prochains matchs
- 🏆 Informations sur le tournoi

**Posez-moi n'importe quelle question !** 👇""",
            "avatar": "🤖"
        })

    # Affichage de l'historique avec style amélioré
    for message in st.session_state.messages:
        avatar = message.get("avatar", "👤" if message["role"] == "user" else "🤖")
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if message.get("sources"):
                display_sources(message["sources"])

    # Gestion de la question d'exemple ou input utilisateur
    if "example_question" in st.session_state:
        user_input = st.session_state.example_question
        del st.session_state.example_question
    else:
        user_input = st.chat_input("💬 Posez votre question sur la CAN 2025...", key="chat_input")

    # Traitement de la question
    if user_input:
        # Affichage du message utilisateur
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "avatar": "👤"
        })
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # Génération de la réponse avec spinner personnalisé
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🔍 Recherche dans la base de données..."):
                try:
                    # Appel au chatbot
                    result = st.session_state.chatbot.ask(user_input)
                    
                    # Affichage de la réponse
                    st.markdown(result["answer"])
                    
                    # Affichage des sources
                    if result.get("sources"):
                        display_sources(result["sources"])
                    
                    # Sauvegarde dans l'historique
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result.get("sources"),
                        "avatar": "🤖"
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Erreur : {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Erreur chatbot: {e}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Désolé, une erreur s'est produite. Veuillez réessayer.",
                        "avatar": "🤖"
                    })

    # Footer avec statistiques avancées
    st.markdown("---")
    st.markdown('<div class="footer-stats">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        num_conversations = (len(st.session_state.messages) - 1) // 2  # -1 pour le message de bienvenue
        st.markdown("### 💬")
        st.markdown(f"**{num_conversations}** conversations")
    
    with col2:
        st.markdown("### ⚡")
        st.markdown("**Groq AI** • Gratuit")
    
    with col3:
        st.markdown("### 📊")
        st.markdown("**20** documents RAG")
    
    with col4:
        from datetime import datetime
        st.markdown("### 📅")
        st.markdown(f"**{datetime.now().strftime('%d/%m/%Y')}**")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bouton pour réinitialiser la conversation
    if len(st.session_state.messages) > 1:
        if st.button("🗑️ Nouvelle conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
