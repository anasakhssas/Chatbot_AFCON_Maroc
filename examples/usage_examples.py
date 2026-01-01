"""
Exemple d'utilisation des données transformées pour le RAG
"""
import json
from pathlib import Path
from collections import Counter

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "transformed" / "combined_dataset.json"


def load_dataset():
    """Charger le dataset combiné"""
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def example_basic_stats():
    """Exemple 1: Statistiques de base"""
    print("=" * 70)
    print("📊 EXEMPLE 1: Statistiques de Base")
    print("=" * 70)
    
    dataset = load_dataset()
    documents = dataset['documents']
    
    print(f"\n✅ Total documents: {len(documents)}")
    print(f"📅 Date de création: {dataset['metadata']['creation_date']}")
    
    # Compter par catégorie
    categories = Counter(doc['metadata']['category'] for doc in documents)
    print("\n📑 Par catégorie:")
    for cat, count in categories.items():
        print(f"  • {cat}: {count}")
    
    # Compter par source
    sources = Counter(doc['metadata']['source'] for doc in documents)
    print("\n📰 Par source:")
    for src, count in sources.items():
        print(f"  • {src}: {count}")


def example_filter_by_category():
    """Exemple 2: Filtrer par catégorie"""
    print("\n" + "=" * 70)
    print("🔍 EXEMPLE 2: Filtrer par Catégorie")
    print("=" * 70)
    
    dataset = load_dataset()
    documents = dataset['documents']
    
    # Filtrer les résultats de matchs
    match_results = [
        doc for doc in documents 
        if doc['metadata']['category'] == 'match_result'
    ]
    
    print(f"\n🏆 Résultats de matchs trouvés: {len(match_results)}")
    print("\nPremiers 3 matchs:")
    for i, doc in enumerate(match_results[:3], 1):
        meta = doc['metadata']
        print(f"\n{i}. {meta['title']}")
        print(f"   📅 Date: {meta['date']}")
        print(f"   🔗 Lien: {meta['link']}")


def example_search_by_team():
    """Exemple 3: Rechercher par équipe"""
    print("\n" + "=" * 70)
    print("🔍 EXEMPLE 3: Rechercher par Équipe")
    print("=" * 70)
    
    dataset = load_dataset()
    documents = dataset['documents']
    
    # Rechercher tous les articles sur le Maroc
    team = "Morocco"
    morocco_articles = [
        doc for doc in documents 
        if team in doc['text'] or team in str(doc['metadata']['keywords'])
    ]
    
    print(f"\n🇲🇦 Articles mentionnant '{team}': {len(morocco_articles)}")
    print("\nTitres:")
    for i, doc in enumerate(morocco_articles, 1):
        print(f"{i}. {doc['metadata']['title']}")


def example_search_by_player():
    """Exemple 4: Rechercher par joueur"""
    print("\n" + "=" * 70)
    print("🔍 EXEMPLE 4: Rechercher par Joueur")
    print("=" * 70)
    
    dataset = load_dataset()
    documents = dataset['documents']
    
    # Rechercher les articles mentionnant Salah
    player = "Salah"
    player_articles = [
        doc for doc in documents 
        if player in doc['text']
    ]
    
    print(f"\n⚽ Articles mentionnant '{player}': {len(player_articles)}")
    for doc in player_articles:
        meta = doc['metadata']
        print(f"\n📰 {meta['title']}")
        print(f"   📅 {meta['date']}")
        # Extraire le contexte autour du nom du joueur
        text = doc['text']
        idx = text.find(player)
        if idx != -1:
            context = text[max(0, idx-50):min(len(text), idx+100)]
            print(f"   📝 Contexte: ...{context}...")


def example_get_latest_news():
    """Exemple 5: Obtenir les dernières news"""
    print("\n" + "=" * 70)
    print("📰 EXEMPLE 5: Dernières Actualités")
    print("=" * 70)
    
    dataset = load_dataset()
    documents = dataset['documents']
    
    # Trier par date
    sorted_docs = sorted(
        documents, 
        key=lambda x: x['metadata']['date'], 
        reverse=True
    )
    
    print("\n🆕 Les 5 dernières actualités:")
    for i, doc in enumerate(sorted_docs[:5], 1):
        meta = doc['metadata']
        print(f"\n{i}. {meta['title']}")
        print(f"   📅 {meta['date']}")
        print(f"   📑 Catégorie: {meta['category']}")


def example_prepare_for_rag():
    """Exemple 6: Préparer les données pour le RAG"""
    print("\n" + "=" * 70)
    print("🤖 EXEMPLE 6: Format pour le RAG")
    print("=" * 70)
    
    dataset = load_dataset()
    documents = dataset['documents']
    
    # Format pour LangChain/LlamaIndex
    rag_documents = []
    for doc in documents[:3]:  # Prendre les 3 premiers comme exemple
        rag_doc = {
            "page_content": doc['text'],  # Le texte pour la vectorisation
            "metadata": doc['metadata']    # Métadonnées pour le filtrage
        }
        rag_documents.append(rag_doc)
    
    print("\n📦 Format prêt pour LangChain/LlamaIndex:")
    print(f"   • Nombre de documents: {len(rag_documents)}")
    print(f"   • Structure: page_content + metadata")
    print("\n📝 Exemple de document:")
    print(json.dumps(rag_documents[0], indent=2, ensure_ascii=False)[:500] + "...")


def main():
    """Exécuter tous les exemples"""
    print("\n" + "🏆" * 35)
    print("     EXEMPLES D'UTILISATION - DONNÉES CAN 2025")
    print("🏆" * 35 + "\n")
    
    if not DATASET_PATH.exists():
        print("❌ Dataset non trouvé. Exécutez d'abord le pipeline:")
        print("   python -m src.pipeline.pipeline")
        return
    
    # Exécuter les exemples
    example_basic_stats()
    example_filter_by_category()
    example_search_by_team()
    example_search_by_player()
    example_get_latest_news()
    example_prepare_for_rag()
    
    print("\n" + "=" * 70)
    print("✅ Tous les exemples terminés!")
    print("=" * 70)
    print("\n💡 Ces exemples montrent comment:")
    print("   • Charger et explorer le dataset")
    print("   • Filtrer par catégorie, équipe, joueur")
    print("   • Préparer les données pour le RAG")
    print("\n🚀 Prochaine étape: Créer les embeddings et ChromaDB")


if __name__ == "__main__":
    main()
