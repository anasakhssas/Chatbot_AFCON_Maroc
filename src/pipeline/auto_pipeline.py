"""
Pipeline automatisé pour l'application Streamlit
Vérifie et exécute le pipeline ETL si nécessaire
"""

import logging
from pathlib import Path
from typing import Tuple, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class AutoPipeline:
    """Gestionnaire de pipeline automatisé pour l'application"""
    
    def __init__(self):
        """Initialiser le pipeline automatisé"""
        from ..rag.config import RAGConfig
        self.config = RAGConfig
        
    def check_data_status(self) -> Dict[str, Any]:
        """
        Vérifier l'état des données
        
        Returns:
            Dictionnaire avec le statut de chaque étape
        """
        status = {
            'raw_data_exists': False,
            'transformed_data_exists': False,
            'vectorstore_exists': False,
            'needs_extraction': False,
            'needs_transformation': False,
            'needs_vectorization': False,
            'ready': False
        }
        
        # Vérifier les données brutes
        raw_dir = self.config.DATA_DIR / "raw"
        if raw_dir.exists() and any(raw_dir.glob("*.json")):
            status['raw_data_exists'] = True
        
        # Vérifier les données transformées
        if self.config.COMBINED_DATASET.exists():
            status['transformed_data_exists'] = True
        
        # Vérifier le vectorstore
        if self.config.CHROMA_DB_DIR.exists():
            chroma_files = list(self.config.CHROMA_DB_DIR.glob("**/*"))
            if len(chroma_files) > 0:
                status['vectorstore_exists'] = True
        
        # Déterminer les actions nécessaires
        if not status['raw_data_exists']:
            status['needs_extraction'] = True
        
        if not status['transformed_data_exists']:
            status['needs_transformation'] = True
        
        if not status['vectorstore_exists']:
            status['needs_vectorization'] = True
        
        # Prêt si tout existe
        status['ready'] = (
            status['raw_data_exists'] and 
            status['transformed_data_exists'] and 
            status['vectorstore_exists']
        )
        
        return status
    
    def run_extraction(self) -> bool:
        """
        Exécuter l'extraction des données
        
        Returns:
            True si réussi, False sinon
        """
        logger.info("📥 Extraction des données...")
        try:
            from ..pipeline.demo_scraper import save_demo_data
            raw_data_path = save_demo_data()
            logger.info(f"✅ Extraction réussie: {raw_data_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            return False
    
    def run_transformation(self) -> bool:
        """
        Exécuter la transformation des données
        
        Returns:
            True si réussi, False sinon
        """
        logger.info("🔄 Transformation des données pour RAG...")
        try:
            from ..pipeline.transform import DataTransformer
            transformer = DataTransformer()
            
            # Transformer tous les fichiers
            transformed_files = transformer.transform_all_files()
            
            if not transformed_files:
                logger.warning("⚠️ Aucun fichier transformé")
                return False
            
            # Créer le dataset combiné
            combined_path = transformer.create_combined_dataset()
            
            if combined_path:
                stats = transformer.get_statistics()
                logger.info(f"✅ Transformation réussie: {stats['total_documents']} documents")
                return True
            else:
                logger.error("❌ Échec de création du dataset combiné")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de la transformation: {e}")
            return False
    
    def run_vectorization(self) -> bool:
        """
        Exécuter la vectorisation (création de ChromaDB)
        
        Returns:
            True si réussi, False sinon
        """
        logger.info("🔍 Vectorisation et création de ChromaDB...")
        try:
            from ..rag.vectorizer import VectorizerCAN2025
            vectorizer = VectorizerCAN2025()
            vectorizer.create_vectorstore()
            logger.info("✅ Vectorisation réussie")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de la vectorisation: {e}")
            return False
    
    def ensure_ready(self, force_refresh: bool = False) -> Tuple[bool, str]:
        """
        S'assurer que toutes les données sont prêtes
        Exécute automatiquement les étapes manquantes
        
        Args:
            force_refresh: Si True, force la régénération complète
        
        Returns:
            Tuple (succès: bool, message: str)
        """
        logger.info("🚀 Vérification du pipeline de données...")
        
        # Vérifier l'état actuel
        status = self.check_data_status()
        
        if status['ready'] and not force_refresh:
            logger.info("✅ Toutes les données sont prêtes")
            return True, "Données prêtes"
        
        steps_completed = []
        steps_failed = []
        
        # Étape 1: Extraction
        if status['needs_extraction'] or force_refresh:
            logger.info("📥 Étape 1/3: Extraction des données...")
            if self.run_extraction():
                steps_completed.append("Extraction")
            else:
                steps_failed.append("Extraction")
                return False, "Échec de l'extraction des données"
        else:
            logger.info("✓ Données brutes déjà présentes")
        
        # Étape 2: Transformation
        if status['needs_transformation'] or force_refresh:
            logger.info("🔄 Étape 2/3: Transformation des données...")
            if self.run_transformation():
                steps_completed.append("Transformation")
            else:
                steps_failed.append("Transformation")
                return False, "Échec de la transformation des données"
        else:
            logger.info("✓ Données transformées déjà présentes")
        
        # Étape 3: Vectorisation
        if status['needs_vectorization'] or force_refresh:
            logger.info("🔍 Étape 3/3: Vectorisation (ChromaDB)...")
            if self.run_vectorization():
                steps_completed.append("Vectorisation")
            else:
                steps_failed.append("Vectorisation")
                return False, "Échec de la vectorisation"
        else:
            logger.info("✓ ChromaDB déjà créée")
        
        # Résumé
        if steps_completed:
            message = f"Pipeline complété: {', '.join(steps_completed)}"
            logger.info(f"✅ {message}")
        else:
            message = "Toutes les données étaient déjà présentes"
            logger.info(f"✅ {message}")
        
        if steps_failed:
            message = f"Échecs: {', '.join(steps_failed)}"
            logger.error(f"❌ {message}")
            return False, message
        
        return True, message
    
    def get_status_message(self) -> str:
        """
        Obtenir un message d'état lisible
        
        Returns:
            Message décrivant l'état du pipeline
        """
        status = self.check_data_status()
        
        if status['ready']:
            return "✅ Pipeline prêt - Toutes les données sont chargées"
        
        messages = []
        if status['needs_extraction']:
            messages.append("❌ Extraction requise")
        if status['needs_transformation']:
            messages.append("❌ Transformation requise")
        if status['needs_vectorization']:
            messages.append("❌ Vectorisation requise")
        
        return " | ".join(messages) if messages else "⚠️ État inconnu"
