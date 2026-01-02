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
from src.sentiment.youtube_analyzer import YouTubeSentimentAnalyzer
from src.sentiment.visualizer import (
    create_sentiment_pie_chart, 
    create_sentiment_bar_chart,
    create_wordcloud,
    create_confidence_distribution
)
from src.summary.match_summarizer import MatchSummarizer
from src.summary.exporters import PDFExporter, ImageExporter
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


def sentiment_page():
    """Page d'analyse de sentiment YouTube"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Analyse de Sentiment des Supporters</h1>
        <p>Analysez les commentaires YouTube sur la CAN 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    st.info("💡 **Comment utiliser:**  \n"
            "1. Copiez l'URL d'une vidéo YouTube sur la CAN 2025  \n"
            "2. Collez l'URL ci-dessous  \n"
            "3. Cliquez sur 'Analyser'  \n"
            "4. Découvrez le sentiment des supporters (positif, neutre, négatif)")
    
    # Input URL
    url = st.text_input(
        "🔗 URL de la vidéo YouTube",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Exemple: https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    
    # Options avancées
    with st.expander("⚙️ Options avancées"):
        max_comments = st.slider(
            "Nombre maximum de commentaires à analyser",
            min_value=50,
            max_value=1000,
            value=500,
            step=50,
            help="Plus de commentaires = analyse plus précise mais plus lente"
        )
        
        show_confidence = st.checkbox("Afficher la distribution des scores de confiance", value=False)
    
    # Bouton d'analyse
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🔍 Analyser les commentaires", use_container_width=True, type="primary")
    
    # Analyse
    if analyze_button and url:
        try:
            # Initialisation de l'analyseur avec cache
            @st.cache_resource
            def get_analyzer():
                return YouTubeSentimentAnalyzer()
            
            analyzer = get_analyzer()
            
            # Progress bar
            progress_bar = st.progress(0, text="Initialisation...")
            
            # Étape 1: Extraction des commentaires
            progress_bar.progress(20, text="📥 Téléchargement des commentaires...")
            stats = analyzer.analyze_video(url, max_comments=max_comments)
            
            progress_bar.progress(100, text="✅ Analyse terminée!")
            progress_bar.empty()
            
            # Résultats
            st.success(f"✅ {stats['total_comments']} commentaires analysés avec succès!")
            
            # Métriques principales
            st.markdown("### 📈 Résultats Globaux")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "😊 Positif",
                    f"{stats['positive']['count']} commentaires",
                    f"{stats['positive']['percentage']:.1f}%"
                )
            
            with col2:
                st.metric(
                    "😐 Neutre",
                    f"{stats['neutral']['count']} commentaires",
                    f"{stats['neutral']['percentage']:.1f}%"
                )
            
            with col3:
                st.metric(
                    "😢 Négatif",
                    f"{stats['negative']['count']} commentaires",
                    f"{stats['negative']['percentage']:.1f}%"
                )
            
            st.markdown("---")
            
            # Graphiques
            st.markdown("### 📊 Visualisations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique en camembert
                pie_fig = create_sentiment_pie_chart(stats)
                st.plotly_chart(pie_fig, use_container_width=True)
            
            with col2:
                # Graphique en barres
                bar_fig = create_sentiment_bar_chart(stats)
                st.plotly_chart(bar_fig, use_container_width=True)
            
            # Distribution de confiance
            if show_confidence:
                st.markdown("### 📉 Distribution des Scores de Confiance")
                conf_fig = create_confidence_distribution(stats)
                st.plotly_chart(conf_fig, use_container_width=True)
            
            st.markdown("---")
            
            # Top commentaires
            st.markdown("### 💬 Top 5 Commentaires")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 😊 **Commentaires Positifs**")
                if stats['top_positive']:
                    for i, comment in enumerate(stats['top_positive'], 1):
                        with st.container():
                            st.markdown(f"**{i}. {comment['author']}** "
                                      f"_(👍 {comment['likes']} likes)_")
                            st.markdown(f"> {comment['text'][:200]}...")
                            st.caption(f"Confiance: {comment['confidence']:.2%} • {comment.get('time', '')}")
                            st.markdown("---")
                else:
                    st.info("Aucun commentaire positif trouvé")
            
            with col2:
                st.markdown("#### 😢 **Commentaires Négatifs**")
                if stats['top_negative']:
                    for i, comment in enumerate(stats['top_negative'], 1):
                        with st.container():
                            st.markdown(f"**{i}. {comment['author']}** "
                                      f"_(👍 {comment['likes']} likes)_")
                            st.markdown(f"> {comment['text'][:200]}...")
                            st.caption(f"Confiance: {comment['confidence']:.2%} • {comment.get('time', '')}")
                            st.markdown("---")
                else:
                    st.info("Aucun commentaire négatif trouvé")
            
        except ValueError as e:
            st.error(f"❌ Erreur: {str(e)}")
            st.info("Vérifiez que l'URL est valide et que la vidéo contient des commentaires.")
        
        except Exception as e:
            st.error(f"❌ Une erreur s'est produite: {str(e)}")
            st.exception(e)
    
    elif analyze_button and not url:
        st.warning("⚠️ Veuillez entrer une URL YouTube")


def chatbot_page():
    """Page principale du chatbot"""
    
    # Header avec couleurs du Maroc
    st.markdown("""
    <div class="main-header">
        <h1>⚽ Chatbot CAN 2025 - Maroc 🇲🇦</h1>
        <p>Assistant intelligent pour la Coupe d'Afrique des Nations 2025</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">
            🤖 Propulsé par Groq AI • 📚 RAG avec LangChain • 🔍 ChromaDB
        </p>
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

    # Bouton pour réinitialiser la conversation
    st.markdown("---")
    if len(st.session_state.messages) > 1:
        if st.button("🗑️ Nouvelle conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def main():
    """Fonction principale"""
    
    # Sidebar pour navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        page = st.radio(
            "Choisir une page",
            ["💬 Chatbot CAN 2025", "📊 Analyse de Sentiment", "📝 Résumés de Matchs"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Informations
        st.markdown("### ℹ️ À propos")
        st.markdown("""
        **Chatbot CAN 2025 Maroc**
        
        - 🤖 Assistant intelligent CAN 2025
        - 📊 Analyse sentiment supporters
        - ⚡ Powered by Groq LLM
        - 🔍 ChromaDB vectorisation
        
        ---
        
        📅 **CAN 2025 au Maroc**  
        21 Déc 2025 - 18 Jan 2026
        """)
    
    # Afficher la page
    if page == "💬 Chatbot CAN 2025":
        chatbot_page()
    elif page == "📊 Analyse de Sentiment":
        sentiment_page()
    else:
        summary_page()


def summary_page():
    """Page de génération de résumés de matchs"""
    
    st.markdown("""
    <div class="main-header">
        <h1>📝 Résumés Automatiques de Matchs</h1>
        <p>Générez des résumés structurés et exportables à partir d'articles de matchs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialiser le résumeur (avec cache)
    @st.cache_resource
    def init_summarizer():
        try:
            return MatchSummarizer()
        except Exception as e:
            st.error(f"❌ Erreur initialisation du résumeur : {e}")
            return None
    
    summarizer = init_summarizer()
    
    if not summarizer:
        st.warning("⚠️ Le résumeur n'a pas pu être initialisé. Vérifiez votre GROQ_API_KEY.")
        return
    
    # Onglets pour les différents modes
    tab1, tab2, tab3 = st.tabs(["📄 Résumé Simple", "📚 Résumés Multiples", "🔍 Résumés Sauvegardés"])
    
    # TAB 1 : Résumé simple
    with tab1:
        st.markdown("### ✍️ Générer un résumé unique")
        
        # Mode d'entrée
        input_mode = st.radio(
            "Source du texte",
            ["📝 Coller le texte", "🔗 URL d'article"],
            horizontal=True
        )
        
        match_text = ""
        match_title = ""
        
        if input_mode == "📝 Coller le texte":
            match_title = st.text_input("Titre du match (optionnel)", placeholder="Ex: Maroc vs Égypte - Finale CAN 2025")
            match_text = st.text_area(
                "Texte de l'article de match",
                height=250,
                placeholder="Collez ici le texte complet de l'article du match (minimum 100 mots)..."
            )
        else:
            from src.scrapers.real_scraper import RealScraper
            
            url = st.text_input("URL de l'article", placeholder="https://...")
            
            if url and st.button("🔍 Extraire le texte"):
                with st.spinner("Extraction du contenu..."):
                    try:
                        scraper = RealScraper()
                        results = scraper.scrape_url(url)
                        
                        if results and len(results) > 0:
                            result = results[0]
                            match_title = result.get('title', '')
                            match_text = result.get('content', '')
                            
                            st.success(f"✅ Texte extrait : {len(match_text)} caractères")
                            
                            # Afficher un aperçu
                            with st.expander("👁️ Aperçu du texte extrait"):
                                st.write(f"**Titre:** {match_title}")
                                st.write(f"**Contenu:** {match_text[:500]}...")
                        else:
                            st.error("❌ Impossible d'extraire le contenu de cette URL")
                            
                    except Exception as e:
                        st.error(f"❌ Erreur d'extraction : {e}")
        
        # Options de génération
        col1, col2 = st.columns(2)
        
        with col1:
            length = st.selectbox(
                "Longueur du résumé",
                ["short", "medium", "long"],
                format_func=lambda x: {
                    "short": "📏 Court (~50 mots)",
                    "medium": "📐 Moyen (~150 mots)",
                    "long": "📏 Long (~300 mots)"
                }[x],
                index=1
            )
        
        with col2:
            language = st.selectbox(
                "Langue",
                ["fr", "en"],
                format_func=lambda x: "🇫🇷 Français" if x == "fr" else "🇬🇧 English"
            )
        
        # Bouton de génération
        if st.button("✨ Générer le Résumé", type="primary", use_container_width=True):
            if not match_text or len(match_text.split()) < 50:
                st.warning("⚠️ Le texte est trop court. Minimum 50 mots requis.")
            else:
                with st.spinner("🔄 Génération du résumé en cours..."):
                    try:
                        summary = summarizer.generate_summary(match_text, length, language)
                        
                        # Afficher le résumé
                        st.markdown("---")
                        st.markdown("### 📋 Résumé Généré")
                        
                        # Métadonnées
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("📊 Mots", summary['word_count'])
                        with col2:
                            st.metric("📅 Longueur", length.capitalize())
                        with col3:
                            st.metric("🌐 Langue", language.upper())
                        
                        # Résumé dans un container
                        st.markdown(
                            f"""
                            <div style="
                                background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
                                padding: 2rem;
                                border-radius: 15px;
                                border-left: 5px solid #C1272D;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                                margin: 1rem 0;
                            ">
                                {summary['summary'].replace(chr(10), '<br>')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        # Options d'export
                        st.markdown("### 💾 Exporter le résumé")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        # Export PDF
                        with col1:
                            if st.button("📄 Télécharger PDF", use_container_width=True):
                                with st.spinner("Génération du PDF..."):
                                    try:
                                        pdf_exporter = PDFExporter()
                                        
                                        # Créer un dossier exports s'il n'existe pas
                                        os.makedirs("exports", exist_ok=True)
                                        
                                        # Nom de fichier
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                        pdf_path = f"exports/resume_{timestamp}.pdf"
                                        
                                        # Ajouter le titre si disponible
                                        summary['title'] = match_title if match_title else "Résumé de Match"
                                        
                                        pdf_exporter.export_single_summary(summary, pdf_path)
                                        
                                        # Téléchargement
                                        with open(pdf_path, "rb") as f:
                                            st.download_button(
                                                label="⬇️ Cliquez pour télécharger",
                                                data=f.read(),
                                                file_name=f"resume_match_{timestamp}.pdf",
                                                mime="application/pdf",
                                                use_container_width=True
                                            )
                                        
                                        st.success("✅ PDF généré !")
                                        
                                    except Exception as e:
                                        st.error(f"❌ Erreur génération PDF : {e}")
                        
                        # Export Image
                        with col2:
                            if st.button("🖼️ Télécharger Image", use_container_width=True):
                                with st.spinner("Génération de l'image..."):
                                    try:
                                        img_exporter = ImageExporter()
                                        
                                        os.makedirs("exports", exist_ok=True)
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                        img_path = f"exports/card_{timestamp}.png"
                                        
                                        summary['title'] = match_title if match_title else "Résumé de Match"
                                        
                                        img_exporter.create_social_card(summary, img_path)
                                        
                                        # Afficher et télécharger
                                        st.image(img_path, use_column_width=True)
                                        
                                        with open(img_path, "rb") as f:
                                            st.download_button(
                                                label="⬇️ Cliquez pour télécharger",
                                                data=f.read(),
                                                file_name=f"card_match_{timestamp}.png",
                                                mime="image/png",
                                                use_container_width=True
                                            )
                                        
                                        st.success("✅ Image générée !")
                                        
                                    except Exception as e:
                                        st.error(f"❌ Erreur génération image : {e}")
                        
                        # Copier dans le presse-papiers
                        with col3:
                            st.button("📋 Copier le texte", use_container_width=True)
                            st.code(summary['summary'], language=None)
                        
                        # Sauvegarder dans l'historique
                        if 'summaries_history' not in st.session_state:
                            st.session_state.summaries_history = []
                        
                        summary['title'] = match_title if match_title else f"Match {len(st.session_state.summaries_history) + 1}"
                        st.session_state.summaries_history.append(summary)
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la génération : {e}")
                        logger.error(f"Erreur résumé : {e}")
    
    # TAB 2 : Résumés multiples
    with tab2:
        st.markdown("### 📚 Générer plusieurs résumés en batch")
        
        st.info("💡 Collez plusieurs textes d'articles séparés par `---` pour générer des résumés en batch.")
        
        batch_text = st.text_area(
            "Textes des matchs (séparés par ---)",
            height=300,
            placeholder="Article match 1...\n\n---\n\nArticle match 2...\n\n---\n\nArticle match 3..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            batch_length = st.selectbox(
                "Longueur",
                ["short", "medium", "long"],
                format_func=lambda x: {"short": "Court", "medium": "Moyen", "long": "Long"}[x],
                key="batch_length"
            )
        with col2:
            batch_language = st.selectbox("Langue", ["fr", "en"], key="batch_language")
        
        if st.button("✨ Générer tous les résumés", type="primary", use_container_width=True):
            if batch_text:
                # Séparer les textes
                texts = [t.strip() for t in batch_text.split("---") if t.strip()]
                
                if len(texts) == 0:
                    st.warning("⚠️ Aucun texte valide trouvé.")
                else:
                    st.info(f"🔄 Génération de {len(texts)} résumés... (environ {len(texts) * 2} secondes)")
                    
                    # Préparer les textes
                    items = [{"text": text, "title": f"Match {i+1}"} for i, text in enumerate(texts)]
                    
                    # Générer
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    summaries = []
                    for idx, item in enumerate(items):
                        status_text.text(f"Résumé {idx+1}/{len(items)}...")
                        try:
                            summary = summarizer.generate_summary(
                                item['text'],
                                batch_length,
                                batch_language
                            )
                            summary['title'] = item['title']
                            summaries.append(summary)
                        except Exception as e:
                            st.error(f"Erreur pour {item['title']}: {e}")
                        
                        progress_bar.progress((idx + 1) / len(items))
                        
                        # Délai de 2s entre chaque (rate limit)
                        if idx < len(items) - 1:
                            import time
                            time.sleep(2)
                    
                    status_text.text("✅ Terminé !")
                    
                    # Afficher tous les résumés
                    st.markdown("---")
                    st.markdown("### 📋 Résumés Générés")
                    
                    for idx, summary in enumerate(summaries, 1):
                        with st.expander(f"📄 {summary['title']} ({summary['word_count']} mots)"):
                            st.markdown(summary['summary'])
                    
                    # Export PDF compilé
                    if st.button("📄 Télécharger PDF compilé", use_container_width=True):
                        with st.spinner("Génération du PDF compilé..."):
                            try:
                                pdf_exporter = PDFExporter()
                                os.makedirs("exports", exist_ok=True)
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                pdf_path = f"exports/digest_{timestamp}.pdf"
                                
                                pdf_exporter.export_multiple_summaries(
                                    summaries,
                                    pdf_path,
                                    title=f"Résumés CAN 2025 - {len(summaries)} Matchs"
                                )
                                
                                with open(pdf_path, "rb") as f:
                                    st.download_button(
                                        label="⬇️ Télécharger le digest PDF",
                                        data=f.read(),
                                        file_name=f"digest_matchs_{timestamp}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                
                                st.success(f"✅ PDF avec {len(summaries)} résumés créé !")
                                
                            except Exception as e:
                                st.error(f"❌ Erreur : {e}")
    
    # TAB 3 : Historique
    with tab3:
        st.markdown("### 🔍 Résumés sauvegardés dans cette session")
        
        if 'summaries_history' not in st.session_state or len(st.session_state.summaries_history) == 0:
            st.info("📭 Aucun résumé généré dans cette session pour le moment.")
        else:
            st.success(f"✅ {len(st.session_state.summaries_history)} résumé(s) en mémoire")
            
            for idx, summary in enumerate(st.session_state.summaries_history, 1):
                with st.expander(f"📄 {summary.get('title', f'Résumé {idx}')} - {summary.get('word_count', 0)} mots"):
                    st.markdown(f"**Généré le:** {summary.get('generated_at', 'N/A')[:19]}")
                    st.markdown(f"**Longueur:** {summary.get('length', 'N/A').capitalize()}")
                    st.markdown(f"**Langue:** {summary.get('language', 'N/A').upper()}")
                    st.markdown("---")
                    st.markdown(summary.get('summary', ''))
            
            # Bouton pour exporter tout l'historique
            if st.button("📄 Exporter tout l'historique en PDF", use_container_width=True):
                with st.spinner("Génération du PDF..."):
                    try:
                        pdf_exporter = PDFExporter()
                        os.makedirs("exports", exist_ok=True)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        pdf_path = f"exports/historique_{timestamp}.pdf"
                        
                        pdf_exporter.export_multiple_summaries(
                            st.session_state.summaries_history,
                            pdf_path,
                            title="Historique des Résumés - CAN 2025"
                        )
                        
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Télécharger l'historique PDF",
                                data=f.read(),
                                file_name=f"historique_{timestamp}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        st.success("✅ PDF de l'historique créé !")
                        
                    except Exception as e:
                        st.error(f"❌ Erreur : {e}")
            
            # Bouton pour vider l'historique
            if st.button("🗑️ Vider l'historique", use_container_width=True):
                st.session_state.summaries_history = []
                st.rerun()


if __name__ == "__main__":
    main()
