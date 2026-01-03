"""
Module de vectorisation pour le Chatbot CAN 2025
Transforme les documents JSON en embeddings et les stocke dans ChromaDB
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from .config import RAGConfig

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VectorizerCAN2025:
    """Classe pour vectoriser et stocker les documents CAN 2025"""
    
    def __init__(self, config: RAGConfig = None):
        """
        Initialiser le vectorizer
        
        Args:
            config: Configuration RAG (utilise RAGConfig par défaut)
        """
        self.config = config or RAGConfig
        self.embeddings = None
        self.vectorstore = None
        
        # Valider la configuration
        errors = self.config.validate()
        if errors:
            for error in errors:
                logger.error(error)
            raise ValueError("Configuration invalide. Vérifiez les erreurs ci-dessus.")
        
        logger.info("✅ VectorizerCAN2025 initialisé")
    
    def _initialize_embeddings(self):
        """Initialiser le modèle d'embeddings HuggingFace (gratuit et local)"""
        if self.embeddings is None:
            logger.info(f"🔄 Initialisation des embeddings : {self.config.EMBEDDING_MODEL}")
            logger.info("📥 Téléchargement du modèle (première fois seulement)...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.config.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},  # Utilise CPU (pas besoin de GPU)
                encode_kwargs={'normalize_embeddings': True}  # Normalisation pour meilleure performance
            )
            logger.info("✅ Embeddings initialisés (100% gratuit!)")
    
    def load_documents(self) -> List[Document]:
        """
        Charger les documents depuis le fichier JSON combiné
        
        Returns:
            Liste de documents LangChain
        """
        logger.info(f"📂 Chargement des documents depuis : {self.config.COMBINED_DATASET}")
        
        try:
            with open(self.config.COMBINED_DATASET, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            documents = []
            for i, doc in enumerate(data['documents']):
                # Gérer différents formats de documents
                # Format 1: {text, metadata: {id, category, ...}}
                # Format 2: {id, text, metadata: {category, ...}}
                
                text = doc.get('text', '')
                metadata = doc.get('metadata', {})
                
                # Récupérer l'ID (peut être dans metadata ou à la racine)
                doc_id = doc.get('id') or metadata.get('id') or f"doc_{i}"
                
                # Créer un Document LangChain
                langchain_doc = Document(
                    page_content=text,
                    metadata={
                        'id': doc_id,
                        'category': metadata.get('category', 'unknown'),
                        'source': metadata.get('source', 'unknown'),
                        'date': metadata.get('date', ''),
                        'keywords': ', '.join(metadata.get('keywords', [])) if isinstance(metadata.get('keywords', []), list) else metadata.get('keywords', ''),
                        'title': metadata.get('title', ''),
                        # Ajouter les métadonnées spécifiques selon la catégorie
                        **{k: v for k, v in metadata.items() 
                           if k not in ['id', 'category', 'source', 'date', 'keywords', 'title'] and isinstance(v, (str, int, float, bool))}
                    }
                )
                documents.append(langchain_doc)
            
            logger.info(f"✅ {len(documents)} documents chargés")
            return documents
            
        except FileNotFoundError:
            logger.error(f"❌ Fichier introuvable : {self.config.COMBINED_DATASET}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erreur de parsing JSON : {e}")
            raise
    
    def create_vectorstore(self, documents: List[Document] = None) -> Chroma:
        """
        Créer ou charger le vectorstore ChromaDB
        
        Args:
            documents: Liste de documents à vectoriser (si None, charge depuis JSON)
        
        Returns:
            Vectorstore Chroma
        """
        # Initialiser les embeddings
        self._initialize_embeddings()
        
        # Charger les documents si non fournis
        if documents is None:
            documents = self.load_documents()
        
        # Créer le répertoire ChromaDB si nécessaire
        self.config.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🔄 Création du vectorstore ChromaDB : {self.config.CHROMA_DB_DIR}")
        logger.info(f"📊 Vectorisation de {len(documents)} documents...")
        
        try:
            # Créer le vectorstore avec ChromaDB
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=str(self.config.CHROMA_DB_DIR),
                collection_name=self.config.COLLECTION_NAME,
                collection_metadata=self.config.COLLECTION_METADATA
            )
            
            logger.info("✅ Vectorstore créé et persisté avec succès")
            logger.info(f"📁 Emplacement : {self.config.CHROMA_DB_DIR}")
            
            return self.vectorstore
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la création du vectorstore : {e}")
            raise
    
    def load_vectorstore(self) -> Chroma:
        """
        Charger un vectorstore existant
        
        Returns:
            Vectorstore Chroma
        """
        self._initialize_embeddings()
        
        if not self.config.CHROMA_DB_DIR.exists():
            logger.error(f"❌ Vectorstore introuvable : {self.config.CHROMA_DB_DIR}")
            raise FileNotFoundError("Vectorstore n'existe pas. Exécutez create_vectorstore() d'abord.")
        
        logger.info(f"📂 Chargement du vectorstore existant : {self.config.CHROMA_DB_DIR}")
        
        try:
            self.vectorstore = Chroma(
                persist_directory=str(self.config.CHROMA_DB_DIR),
                embedding_function=self.embeddings,
                collection_name=self.config.COLLECTION_NAME
            )
            
            # Vérifier le nombre de documents
            collection = self.vectorstore._collection
            count = collection.count()
            logger.info(f"✅ Vectorstore chargé : {count} documents")
            
            return self.vectorstore
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du vectorstore : {e}")
            raise
    
    def test_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Tester la recherche sémantique
        
        Args:
            query: Question de recherche
            k: Nombre de résultats à retourner
        
        Returns:
            Liste de résultats avec contenu et métadonnées
        """
        if self.vectorstore is None:
            logger.warning("⚠️  Vectorstore non initialisé, tentative de chargement...")
            self.load_vectorstore()
        
        logger.info(f"🔍 Recherche : '{query}'")
        
        # Recherche avec scores de similarité
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        formatted_results = []
        for i, (doc, score) in enumerate(results, 1):
            result = {
                'rank': i,
                'score': round(score, 4),
                'content': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                'metadata': doc.metadata
            }
            formatted_results.append(result)
            
            logger.info(f"\n📄 Résultat #{i} (score: {score:.4f})")
            logger.info(f"   Catégorie : {doc.metadata.get('category', 'N/A')}")
            logger.info(f"   Source    : {doc.metadata.get('source', 'N/A')}")
            logger.info(f"   Contenu   : {result['content'][:100]}...")
        
        return formatted_results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtenir les statistiques du vectorstore
        
        Returns:
            Dictionnaire avec les statistiques
        """
        if self.vectorstore is None:
            self.load_vectorstore()
        
        collection = self.vectorstore._collection
        count = collection.count()
        
        # Compter par catégorie
        all_docs = collection.get(include=['metadatas'])
        categories = {}
        for metadata in all_docs['metadatas']:
            cat = metadata.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        stats = {
            'total_documents': count,
            'categories': categories,
            'collection_name': self.config.COLLECTION_NAME,
            'embedding_model': self.config.EMBEDDING_MODEL,
            'persist_directory': str(self.config.CHROMA_DB_DIR)
        }
        
        logger.info("\n📊 STATISTIQUES VECTORSTORE")
        logger.info("=" * 50)
        logger.info(f"Total documents : {stats['total_documents']}")
        logger.info(f"Modèle embeddings : {stats['embedding_model']}")
        logger.info(f"\nRépartition par catégorie :")
        for cat, count in stats['categories'].items():
            logger.info(f"  - {cat}: {count} documents")
        logger.info("=" * 50)
        
        return stats


def main():
    """Fonction principale pour tester le vectorizer"""
    print("\n🚀 VECTORISATION CAN 2025 - DÉBUT\n")
    
    # Afficher la configuration
    RAGConfig.print_config()
    
    # Créer le vectorizer
    vectorizer = VectorizerCAN2025()
    
    # Créer le vectorstore
    print("🔄 Étape 1: Création du vectorstore...")
    vectorstore = vectorizer.create_vectorstore()
    
    # Afficher les statistiques
    print("\n🔄 Étape 2: Statistiques du vectorstore...")
    stats = vectorizer.get_stats()
    
    # Tests de recherche
    print("\n🔄 Étape 3: Tests de recherche sémantique...")
    
    test_queries = [
        "Qui a marqué pour le Maroc ?",
        "Quel est le meilleur buteur ?",
        "Résultat du match Égypte Zimbabwe"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"❓ Question : {query}")
        print('='*60)
        results = vectorizer.test_search(query, k=2)
    
    print("\n✅ VECTORISATION TERMINÉE AVEC SUCCÈS!\n")
    print(f"📁 Vectorstore sauvegardé dans : {RAGConfig.CHROMA_DB_DIR}")
    print(f"📊 {stats['total_documents']} documents indexés\n")


if __name__ == "__main__":
    main()
