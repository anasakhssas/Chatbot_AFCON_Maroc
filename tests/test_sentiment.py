"""
Script de test pour l'analyseur de sentiment YouTube
Teste les fonctionnalités de base sans interface Streamlit
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sentiment.youtube_analyzer import YouTubeSentimentAnalyzer

def test_url_extraction():
    """Test de l'extraction d'ID depuis différents formats d'URL"""
    print("🧪 Test 1: Extraction d'ID de vidéo YouTube\n")
    
    analyzer = YouTubeSentimentAnalyzer()
    
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
    ]
    
    for url in test_urls:
        try:
            video_id = analyzer.extract_video_id(url)
            print(f"✅ URL: {url}")
            print(f"   ID:  {video_id}\n")
        except Exception as e:
            print(f"❌ Erreur pour {url}: {e}\n")


def test_sentiment_classification():
    """Test de la classification de sentiment"""
    print("\n🧪 Test 2: Classification de sentiment\n")
    
    analyzer = YouTubeSentimentAnalyzer()
    
    test_comments = [
        "Excellent match! Le Maroc a dominé du début à la fin. Bravo aux joueurs! 🇲🇦⚽",
        "Match nul et sans intérêt. Déçu de la performance.",
        "Le match était correct, rien d'exceptionnel.",
        "👍👍👍",
        "Quelle honte! L'équipe ne mérite pas d'être là.",
    ]
    
    for comment in test_comments:
        sentiment, confidence = analyzer.analyze_sentiment(comment)
        emoji = "😊" if sentiment == "positive" else "😐" if sentiment == "neutral" else "😢"
        
        print(f"{emoji} Commentaire: {comment[:60]}...")
        print(f"   Sentiment: {sentiment.upper()} (confiance: {confidence:.2%})\n")


def test_small_video_analysis():
    """Test d'analyse d'une vraie vidéo YouTube (avec peu de commentaires)"""
    print("\n🧪 Test 3: Analyse d'une vidéo YouTube\n")
    print("⚠️  Ce test nécessite une connexion internet et peut prendre 1-2 minutes")
    print("⚠️  Utilisez une vidéo courte avec peu de commentaires pour le test")
    
    # Demander à l'utilisateur
    test_url = input("\nEntrez une URL YouTube à tester (ou laissez vide pour passer): ").strip()
    
    if not test_url:
        print("Test ignoré.")
        return
    
    try:
        analyzer = YouTubeSentimentAnalyzer()
        
        print(f"\n📥 Analyse de: {test_url}")
        print("⏳ Téléchargement et analyse en cours...\n")
        
        # Analyser avec seulement 50 commentaires pour le test
        stats = analyzer.analyze_video(test_url, max_comments=50)
        
        print("\n✅ Analyse terminée!")
        print(f"\n📊 Résultats:")
        print(f"   Total: {stats['total_comments']} commentaires")
        print(f"   😊 Positif: {stats['positive']['count']} ({stats['positive']['percentage']:.1f}%)")
        print(f"   😐 Neutre:  {stats['neutral']['count']} ({stats['neutral']['percentage']:.1f}%)")
        print(f"   😢 Négatif: {stats['negative']['count']} ({stats['negative']['percentage']:.1f}%)")
        
        # Afficher top 3 commentaires positifs
        if stats['top_positive']:
            print(f"\n😊 Top 3 commentaires positifs:")
            for i, comment in enumerate(stats['top_positive'][:3], 1):
                print(f"   {i}. {comment['author']}: {comment['text'][:80]}...")
                print(f"      (👍 {comment['likes']} likes, confiance: {comment['confidence']:.2%})")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTS DE L'ANALYSEUR DE SENTIMENT YOUTUBE")
    print("=" * 70)
    
    # Test 1: Extraction d'ID
    test_url_extraction()
    
    # Test 2: Classification de sentiment
    test_sentiment_classification()
    
    # Test 3: Analyse complète (optionnel)
    response = input("\n⚠️  Voulez-vous tester l'analyse d'une vraie vidéo? (y/n): ").strip().lower()
    if response == 'y':
        test_small_video_analysis()
    
    print("\n" + "=" * 70)
    print("✅ Tests terminés!")
    print("=" * 70)
