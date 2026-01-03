"""
Script pour mettre à jour le vectorstore ChromaDB après enrichissement
Recrée la base vectorielle avec les nouvelles données
"""

import logging
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.rag.vectorizer import VectorizerCAN2025
from src.rag.config import RAGConfig

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def update_vectorstore():
    """Mettre à jour le vectorstore avec les nouvelles données"""
    print("\n" + "=" * 70)
    print("🚀 MISE À JOUR DU VECTORSTORE ChromaDB")
    print("=" * 70 + "\n")
    
    try:
        # Initialiser le vectorizer
        logger.info("🔧 Initialisation du vectorizer...")
        vectorizer = VectorizerCAN2025()
        
        # Vérifier que le fichier combiné existe
        if not RAGConfig.COMBINED_DATASET.exists():
            logger.error(f"❌ Fichier combiné introuvable : {RAGConfig.COMBINED_DATASET}")
            logger.error("   Exécutez d'abord : python src/pipeline/enrich_database.py")
            return False
        
        # Charger les documents
        logger.info("📂 Chargement des documents depuis le fichier combiné...")
        documents = vectorizer.load_documents()
        logger.info(f"✅ {len(documents)} documents chargés")
        
        # Sauvegarder l'ancien vectorstore si il existe
        if RAGConfig.CHROMA_DB_DIR.exists():
            logger.info("⚠️  Un vectorstore existe déjà")
            response = input("   Voulez-vous le remplacer ? (o/N) : ")
            if response.lower() != 'o':
                logger.info("❌ Opération annulée")
                return False
            
            # Créer un backup
            import shutil
            from datetime import datetime
            backup_dir = RAGConfig.CHROMA_DB_DIR.parent / f"chroma_db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info(f"💾 Création d'un backup : {backup_dir.name}")
            shutil.copytree(RAGConfig.CHROMA_DB_DIR, backup_dir)
            
            # Supprimer l'ancien
            logger.info("🗑️  Suppression de l'ancien vectorstore...")
            shutil.rmtree(RAGConfig.CHROMA_DB_DIR)
        
        # Créer le nouveau vectorstore
        logger.info("\n🔄 Création du nouveau vectorstore...")
        logger.info("   ⏳ Cela peut prendre quelques minutes...")
        vectorizer.create_vectorstore(documents)
        
        # Tester la recherche
        logger.info("\n🔍 Test de recherche sémantique...")
        test_queries = [
            "Quand commence la CAN 2025 ?",
            "Qui est Achraf Hakimi ?",
            "Combien de titres a l'Égypte ?",
            "Quels sont les stades de la CAN 2025 ?"
        ]
        
        for query in test_queries:
            logger.info(f"\n   Question : {query}")
            results = vectorizer.test_search(query, k=2)
            logger.info(f"   ✅ {len(results)} résultats trouvés")
        
        # Statistiques finales
        logger.info("\n" + "=" * 70)
        logger.info("📊 STATISTIQUES DU VECTORSTORE :")
        stats = vectorizer.get_stats()
        logger.info(f"   • Nombre de documents : {stats['total_documents']}")
        logger.info(f"   • Taille sur disque : {stats['size_mb']:.2f} MB")
        logger.info(f"   • Emplacement : {RAGConfig.CHROMA_DB_DIR}")
        logger.info("=" * 70)
        
        print("\n✅ VECTORSTORE MIS À JOUR AVEC SUCCÈS!")
        print("   Vous pouvez maintenant utiliser le chatbot avec les nouvelles données.\n")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ ERREUR : {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Point d'entrée principal"""
    success = update_vectorstore()
    
    if success:
        print("\n" + "=" * 70)
        print("🎯 PROCHAINES ÉTAPES :")
        print("   1. Testez le chatbot : streamlit run src/app.py")
        print("   2. Posez des questions sur la CAN 2025, les joueurs, l'historique")
        print("   3. Vérifiez que les nouvelles informations sont bien présentes")
        print("=" * 70 + "\n")
        sys.exit(0)
    else:
        print("\n❌ La mise à jour a échoué. Vérifiez les erreurs ci-dessus.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
