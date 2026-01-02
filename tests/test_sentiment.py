"""
Tests unitaires pour l'analyse de sentiment
"""

import pytest
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.sentiment.youtube_analyzer import YouTubeSentimentAnalyzer


class TestSentimentAnalyzer:
    """Tests de l'analyseur de sentiment"""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture: Créer un analyseur"""
        return YouTubeSentimentAnalyzer()
    
    def test_analyzer_creation(self, analyzer):
        """Test: L'analyseur peut être créé"""
        assert analyzer is not None
        assert analyzer.classifier is not None
    
    def test_positive_sentiment(self, analyzer):
        """Test: Détecter un sentiment positif"""
        texts = [
            "Vive le Maroc! Excellente performance!",
            "C'est magnifique, quelle victoire!",
            "Bravo aux Lions de l'Atlas! 🇲🇦"
        ]
        
        for text in texts:
            result = analyzer.analyze_text(text)
            assert result['label'] in ['POSITIVE', 'LABEL_2']
            assert result['score'] > 0.5
    
    def test_negative_sentiment(self, analyzer):
        """Test: Détecter un sentiment négatif"""
        texts = [
            "Quelle déception, c'est horrible",
            "Performance catastrophique",
            "Je suis très déçu"
        ]
        
        for text in texts:
            result = analyzer.analyze_text(text)
            assert result['label'] in ['NEGATIVE', 'LABEL_0']
            assert result['score'] > 0.5
    
    def test_neutral_sentiment(self, analyzer):
        """Test: Détecter un sentiment neutre"""
        texts = [
            "Le match commence à 20h",
            "Il y a 24 équipes",
            "La CAN se déroule au Maroc"
        ]
        
        for text in texts:
            result = analyzer.analyze_text(text)
            assert result is not None
            assert 'label' in result
            assert 'score' in result
    
    def test_empty_text(self, analyzer):
        """Test: Gérer un texte vide"""
        result = analyzer.analyze_text("")
        assert result is not None
    
    def test_multilingual(self, analyzer):
        """Test: Analyse multilingue"""
        texts = {
            'fr': "C'est excellent!",
            'en': "This is great!",
            'ar': "رائع جداً"  # "Très bien"
        }
        
        for lang, text in texts.items():
            result = analyzer.analyze_text(text)
            assert result is not None
            assert 'label' in result


class TestBatchAnalysis:
    """Tests de l'analyse en batch"""
    
    def test_analyze_multiple_comments(self):
        """Test: Analyser plusieurs commentaires"""
        analyzer = YouTubeSentimentAnalyzer()
        
        comments = [
            {"text": "Excellent match!", "likes": 10},
            {"text": "Décevant", "likes": 5},
            {"text": "Match nul", "likes": 3}
        ]
        
        results = []
        for comment in comments:
            result = analyzer.analyze_text(comment['text'])
            results.append(result)
        
        assert len(results) == len(comments)
        assert all('label' in r for r in results)


class TestSentimentMetrics:
    """Tests des métriques de sentiment"""
    
    def test_confidence_score(self):
        """Test: Le score de confiance est valide"""
        analyzer = YouTubeSentimentAnalyzer()
        result = analyzer.analyze_text("C'est vraiment génial!")
        
        assert 0.0 <= result['score'] <= 1.0
    
    def test_label_format(self):
        """Test: Le format du label est correct"""
        analyzer = YouTubeSentimentAnalyzer()
        result = analyzer.analyze_text("Test")
        
        assert result['label'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'LABEL_0', 'LABEL_1', 'LABEL_2']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

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
