"""
Script pour enrichir la base de données ChromaDB avec de nouvelles informations
Fusionne les fichiers JSON d'enrichissement avec les données existantes
"""

import json
import logging
from pathlib import Path
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseEnricher:
    """Classe pour enrichir la base de données avec de nouveaux documents"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.enrichment_dir = self.project_root / "data" / "enrichment"
        self.transformed_dir = self.project_root / "data" / "transformed"
        self.combined_file = self.transformed_dir / "combined_dataset.json"
        
    def load_existing_data(self):
        """Charger les données existantes du fichier combiné"""
        logger.info(f"📂 Chargement des données existantes : {self.combined_file}")
        
        if not self.combined_file.exists():
            logger.warning("⚠️  Aucun fichier combiné existant, création d'un nouveau")
            return {
                "metadata": {
                    "source": "combined",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "version": "1.0"
                },
                "documents": []
            }
        
        with open(self.combined_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"✅ {len(data['documents'])} documents existants chargés")
        return data
    
    def load_enrichment_files(self):
        """Charger tous les fichiers JSON du dossier enrichment"""
        logger.info(f"📂 Recherche de fichiers d'enrichissement dans : {self.enrichment_dir}")
        
        if not self.enrichment_dir.exists():
            logger.error(f"❌ Dossier introuvable : {self.enrichment_dir}")
            return []
        
        enrichment_files = list(self.enrichment_dir.glob("*.json"))
        logger.info(f"📄 {len(enrichment_files)} fichiers trouvés")
        
        all_documents = []
        for file_path in enrichment_files:
            logger.info(f"   📥 Chargement : {file_path.name}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    documents = data.get('documents', [])
                    all_documents.extend(documents)
                    logger.info(f"      ✅ {len(documents)} documents ajoutés")
            except Exception as e:
                logger.error(f"      ❌ Erreur : {e}")
        
        logger.info(f"✅ Total : {len(all_documents)} nouveaux documents chargés")
        return all_documents
    
    def remove_duplicates(self, existing_docs, new_docs):
        """Supprimer les doublons basés sur l'ID"""
        logger.info("🔄 Suppression des doublons...")
        
        # Construire le set d'IDs existants
        existing_ids = set()
        for doc in existing_docs:
            # L'ID peut être dans metadata.id ou directement dans le doc
            if 'metadata' in doc and 'id' in doc['metadata']:
                existing_ids.add(doc['metadata']['id'])
            elif 'id' in doc:
                existing_ids.add(doc['id'])
        
        logger.info(f"   📊 {len(existing_ids)} IDs existants")
        
        unique_new_docs = []
        duplicates = 0
        
        for doc in new_docs:
            # Récupérer l'ID du nouveau document
            doc_id = doc.get('id') or doc.get('metadata', {}).get('id')
            
            if doc_id and doc_id not in existing_ids:
                unique_new_docs.append(doc)
                existing_ids.add(doc_id)
            else:
                duplicates += 1
        
        logger.info(f"   ✅ {len(unique_new_docs)} documents uniques")
        if duplicates > 0:
            logger.info(f"   ⚠️  {duplicates} doublons ignorés")
        
        return unique_new_docs
    
    def merge_and_save(self):
        """Fusionner les données existantes avec les nouvelles et sauvegarder"""
        logger.info("🚀 Démarrage de l'enrichissement de la base de données")
        logger.info("=" * 60)
        
        # Charger les données
        existing_data = self.load_existing_data()
        new_documents = self.load_enrichment_files()
        
        if not new_documents:
            logger.warning("⚠️  Aucun nouveau document à ajouter")
            return
        
        # Supprimer les doublons
        unique_new_docs = self.remove_duplicates(
            existing_data['documents'], 
            new_documents
        )
        
        if not unique_new_docs:
            logger.warning("⚠️  Tous les documents sont déjà présents")
            return
        
        # Fusionner
        logger.info("🔄 Fusion des données...")
        existing_data['documents'].extend(unique_new_docs)
        
        # Mettre à jour les métadonnées
        existing_data['metadata']['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existing_data['metadata']['last_enrichment'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existing_data['metadata']['total_documents'] = len(existing_data['documents'])
        
        # Sauvegarder
        logger.info(f"💾 Sauvegarde dans : {self.combined_file}")
        self.transformed_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.combined_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        logger.info("✅ Base de données enrichie avec succès!")
        logger.info("=" * 60)
        logger.info(f"📊 STATISTIQUES FINALES :")
        logger.info(f"   • Documents existants : {len(existing_data['documents']) - len(unique_new_docs)}")
        logger.info(f"   • Nouveaux documents : {len(unique_new_docs)}")
        logger.info(f"   • TOTAL : {len(existing_data['documents'])}")
        logger.info("=" * 60)
        
        # Créer un backup
        backup_file = self.transformed_dir / f"combined_dataset_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Backup créé : {backup_file.name}")
        
        return existing_data
    
    def get_statistics(self):
        """Afficher les statistiques par catégorie"""
        logger.info("\n📊 STATISTIQUES PAR CATÉGORIE :")
        logger.info("=" * 60)
        
        data = self.load_existing_data()
        categories = {}
        
        for doc in data['documents']:
            category = doc['metadata'].get('category', 'non_classé')
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   • {category:30s} : {count:3d} documents")
        
        logger.info("=" * 60)


def main():
    """Point d'entrée principal"""
    print("\n" + "=" * 60)
    print("🚀 ENRICHISSEMENT DE LA BASE DE DONNÉES ChromaDB")
    print("=" * 60 + "\n")
    
    enricher = DatabaseEnricher()
    
    # Fusionner et sauvegarder
    enricher.merge_and_save()
    
    # Afficher les statistiques
    enricher.get_statistics()
    
    print("\n" + "=" * 60)
    print("✅ ÉTAPE SUIVANTE :")
    print("   Exécutez le script de vectorisation pour mettre à jour ChromaDB :")
    print("   python src/pipeline/update_vectorstore.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
