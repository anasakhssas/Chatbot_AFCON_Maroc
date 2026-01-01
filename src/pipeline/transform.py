"""Transform extracted data for RAG system"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from .config import BASE_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "daily_fetch"
TRANSFORMED_DATA_DIR = DATA_DIR / "transformed"

# Create directories
TRANSFORMED_DATA_DIR.mkdir(parents=True, exist_ok=True)


class DataTransformer:
    """Transform raw JSON data into RAG-ready format"""
    
    def __init__(self):
        self.raw_data_dir = RAW_DATA_DIR
        self.transformed_dir = TRANSFORMED_DATA_DIR
        
    def transform_article(self, article: Dict) -> Dict:
        """
        Transform a single article into RAG-ready format
        Creates a comprehensive text representation for embeddings
        """
        # Create a rich text representation combining all fields
        article_text = self._create_article_text(article)
        
        # Extract metadata
        metadata = {
            "id": article.get("id", ""),
            "title": article.get("title", ""),
            "date": article.get("date", ""),
            "source": article.get("source", ""),
            "link": article.get("link", ""),
            "category": article.get("category", "general"),
            "keywords": article.get("keywords", []),
            "fetched_at": article.get("fetched_at", "")
        }
        
        return {
            "text": article_text,
            "metadata": metadata,
            "original_content": article.get("content", "")
        }
    
    def _create_article_text(self, article: Dict) -> str:
        """
        Create a comprehensive text representation for RAG
        Combines title, content, and metadata into searchable text
        """
        parts = []
        
        # Add title with emphasis
        title = article.get("title", "").strip()
        if title:
            parts.append(f"Article: {title}")
        
        # Add date information
        date = article.get("date", "").strip()
        if date:
            parts.append(f"Date: {date}")
        
        # Add source
        source = article.get("source", "").strip()
        if source:
            parts.append(f"Source: {source}")
        
        # Add category
        category = article.get("category", "").strip()
        if category:
            parts.append(f"Catégorie: {category}")
        
        # Add main content
        content = article.get("content", "").strip()
        if content:
            parts.append(f"\nContenu:\n{content}")
        
        # Add keywords for better search
        keywords = article.get("keywords", [])
        if keywords:
            keywords_str = ", ".join(keywords)
            parts.append(f"\nMots-clés: {keywords_str}")
        
        return "\n".join(parts)
    
    def transform_file(self, input_file: Path) -> Optional[Path]:
        """Transform a single JSON file"""
        try:
            logger.info(f"📥 Transformation du fichier: {input_file.name}")
            
            # Read raw data
            with open(input_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            articles = raw_data.get('articles', [])
            if not articles:
                logger.warning(f"⚠️ Aucun article trouvé dans {input_file.name}")
                return None
            
            # Transform each article
            transformed_articles = []
            for idx, article in enumerate(articles):
                try:
                    transformed = self.transform_article(article)
                    transformed_articles.append(transformed)
                except Exception as e:
                    logger.error(f"❌ Erreur transformation article {idx}: {e}")
                    continue
            
            # Create transformed data structure
            transformed_data = {
                "metadata": {
                    "original_file": input_file.name,
                    "total_documents": len(transformed_articles),
                    "transformation_date": datetime.now().isoformat(),
                    "original_metadata": raw_data.get('metadata', {})
                },
                "documents": transformed_articles
            }
            
            # Save transformed data
            output_filename = f"transformed_{input_file.stem}.json"
            output_path = self.transformed_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transformed_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Transformation réussie: {len(transformed_articles)} documents")
            logger.info(f"📁 Sauvegardé dans: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la transformation: {e}")
            return None
    
    def transform_all_files(self) -> List[Path]:
        """Transform all JSON files in the raw data directory"""
        logger.info("🔄 Début de la transformation de tous les fichiers...")
        
        json_files = list(self.raw_data_dir.glob("*.json"))
        
        if not json_files:
            logger.warning(f"⚠️ Aucun fichier JSON trouvé dans {self.raw_data_dir}")
            return []
        
        logger.info(f"📂 {len(json_files)} fichier(s) trouvé(s)")
        
        transformed_files = []
        for json_file in json_files:
            output_path = self.transform_file(json_file)
            if output_path:
                transformed_files.append(output_path)
        
        logger.info(f"✅ Transformation terminée: {len(transformed_files)}/{len(json_files)} fichiers")
        
        return transformed_files
    
    def create_combined_dataset(self) -> Optional[Path]:
        """
        Create a single combined dataset from all transformed files
        Useful for loading all data at once into the RAG system
        """
        logger.info("📦 Création du dataset combiné...")
        
        transformed_files = list(self.transformed_dir.glob("transformed_*.json"))
        
        if not transformed_files:
            logger.warning("⚠️ Aucun fichier transformé trouvé")
            return None
        
        all_documents = []
        all_metadata = []
        
        for file_path in transformed_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    documents = data.get('documents', [])
                    all_documents.extend(documents)
                    all_metadata.append(data.get('metadata', {}))
            except Exception as e:
                logger.error(f"❌ Erreur lecture {file_path.name}: {e}")
                continue
        
        # Create combined dataset
        combined_data = {
            "metadata": {
                "total_documents": len(all_documents),
                "creation_date": datetime.now().isoformat(),
                "source_files": [m.get('original_file', '') for m in all_metadata],
                "description": "Combined dataset for RAG system - CAN 2025 News"
            },
            "documents": all_documents
        }
        
        # Save combined dataset
        output_path = self.transformed_dir / "combined_dataset.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ Dataset combiné créé: {len(all_documents)} documents")
        logger.info(f"📁 Sauvegardé dans: {output_path}")
        
        return output_path
    
    def get_statistics(self) -> Dict:
        """Get statistics about transformed data"""
        stats = {
            "raw_files": len(list(self.raw_data_dir.glob("*.json"))),
            "transformed_files": len(list(self.transformed_dir.glob("transformed_*.json"))),
            "total_documents": 0,
            "categories": {},
            "sources": {}
        }
        
        # Read combined dataset if exists
        combined_file = self.transformed_dir / "combined_dataset.json"
        if combined_file.exists():
            with open(combined_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                documents = data.get('documents', [])
                stats['total_documents'] = len(documents)
                
                # Count by category and source
                for doc in documents:
                    metadata = doc.get('metadata', {})
                    category = metadata.get('category', 'unknown')
                    source = metadata.get('source', 'unknown')
                    
                    stats['categories'][category] = stats['categories'].get(category, 0) + 1
                    stats['sources'][source] = stats['sources'].get(source, 0) + 1
        
        return stats


def run_transformation():
    """Main function to run the transformation pipeline"""
    print("=" * 70)
    print("🔄 CAN 2025 - Transformation des Données pour RAG")
    print("=" * 70)
    
    transformer = DataTransformer()
    
    # Transform all files
    transformed_files = transformer.transform_all_files()
    
    if transformed_files:
        print(f"\n✅ {len(transformed_files)} fichier(s) transformé(s)")
        
        # Create combined dataset
        combined_path = transformer.create_combined_dataset()
        
        if combined_path:
            # Show statistics
            stats = transformer.get_statistics()
            print("\n📊 Statistiques:")
            print(f"  - Fichiers bruts: {stats['raw_files']}")
            print(f"  - Fichiers transformés: {stats['transformed_files']}")
            print(f"  - Total documents: {stats['total_documents']}")
            
            if stats['categories']:
                print("\n  📑 Par catégorie:")
                for cat, count in stats['categories'].items():
                    print(f"    • {cat}: {count}")
            
            if stats['sources']:
                print("\n  📰 Par source:")
                for src, count in stats['sources'].items():
                    print(f"    • {src}: {count}")
            
            print(f"\n✅ Dataset combiné prêt pour le RAG: {combined_path}")
    else:
        print("\n⚠️ Aucun fichier n'a été transformé")
    
    print("=" * 70)


if __name__ == "__main__":
    run_transformation()
