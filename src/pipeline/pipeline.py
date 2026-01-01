"""Complete ETL pipeline: Extract -> Transform -> Load"""
import logging
from pathlib import Path
from .demo_scraper import save_demo_data
from .transform import DataTransformer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_complete_pipeline():
    """
    Run the complete ETL pipeline:
    1. Extract: Generate/scrape news data
    2. Transform: Prepare data for RAG
    3. Ready for Load: Data is ready for vector database
    """
    print("=" * 80)
    print("🚀 PIPELINE COMPLET CAN 2025 - Extract → Transform → Ready for RAG")
    print("=" * 80)
    
    # Step 1: Extract (Demo Data)
    print("\n📥 ÉTAPE 1: EXTRACTION DES DONNÉES")
    print("-" * 80)
    try:
        raw_data_path = save_demo_data()
        print(f"✅ Extraction réussie: {raw_data_path}")
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return
    
    # Step 2: Transform
    print("\n🔄 ÉTAPE 2: TRANSFORMATION POUR RAG")
    print("-" * 80)
    try:
        transformer = DataTransformer()
        transformed_files = transformer.transform_all_files()
        
        if transformed_files:
            print(f"✅ {len(transformed_files)} fichier(s) transformé(s)")
            
            # Create combined dataset
            combined_path = transformer.create_combined_dataset()
            
            if combined_path:
                # Show statistics
                stats = transformer.get_statistics()
                print("\n📊 STATISTIQUES FINALES:")
                print(f"  • Fichiers bruts: {stats['raw_files']}")
                print(f"  • Fichiers transformés: {stats['transformed_files']}")
                print(f"  • Total documents: {stats['total_documents']}")
                
                if stats['categories']:
                    print("\n  📑 Répartition par catégorie:")
                    for cat, count in stats['categories'].items():
                        print(f"    - {cat}: {count} documents")
                
                if stats['sources']:
                    print("\n  📰 Répartition par source:")
                    for src, count in stats['sources'].items():
                        print(f"    - {src}: {count} documents")
                
                print(f"\n✅ Dataset combiné créé: {combined_path}")
        else:
            print("⚠️ Aucune transformation effectuée")
    except Exception as e:
        print(f"❌ Erreur lors de la transformation: {e}")
        return
    
    # Step 3: Ready for RAG
    print("\n✅ ÉTAPE 3: DONNÉES PRÊTES POUR LE RAG")
    print("-" * 80)
    print("Les données transformées sont maintenant prêtes pour:")
    print("  • Vectorisation (embeddings)")
    print("  • Stockage dans ChromaDB")
    print("  • Utilisation avec LangChain/LlamaIndex")
    print("  • Requêtes du chatbot RAG")
    
    print("\n" + "=" * 80)
    print("🎉 PIPELINE TERMINÉ AVEC SUCCÈS!")
    print("=" * 80)
    print(f"\n📂 Données disponibles:")
    print(f"  • Brutes: data/daily_fetch/")
    print(f"  • Transformées: data/transformed/")
    print(f"  • Dataset combiné: data/transformed/combined_dataset.json")
    print("\n🚀 Prochaine étape: Implémenter le système RAG avec ChromaDB")


if __name__ == "__main__":
    run_complete_pipeline()
