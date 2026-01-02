"""
Analyseur de sentiment pour commentaires YouTube
Extrait les commentaires d'une vidéo YouTube et analyse le sentiment
"""

from youtube_comment_downloader import YoutubeCommentDownloader
from transformers import pipeline
import re
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeSentimentAnalyzer:
    """Analyseur de sentiment pour YouTube"""
    
    def __init__(self):
        """Initialise l'analyseur avec un modèle multilingue"""
        logger.info("🔄 Initialisation du modèle de sentiment...")
        
        # Modèle plus précis pour l'analyse de sentiment (FR/EN/AR)
        # cardiffnlp/twitter-xlm-roberta-base-sentiment est plus précis que nlptown
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual",
            truncation=True,
            max_length=512
        )
        
        logger.info("✅ Modèle de sentiment initialisé")
    
    def extract_video_id(self, url: str) -> str:
        """
        Extrait l'ID de la vidéo YouTube depuis l'URL
        
        Args:
            url: URL YouTube (formats supportés: youtube.com/watch?v=, youtu.be/)
            
        Returns:
            Video ID
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([\w-]+)',
            r'(?:youtu\.be\/)([\w-]+)',
            r'(?:youtube\.com\/embed\/)([\w-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError("URL YouTube invalide")
    
    def download_comments(self, video_id: str, max_comments: int = 500) -> List[Dict]:
        """
        Télécharge les commentaires d'une vidéo YouTube
        
        Args:
            video_id: ID de la vidéo YouTube
            max_comments: Nombre maximum de commentaires à récupérer
            
        Returns:
            Liste de dictionnaires avec les commentaires
        """
        logger.info(f"📥 Téléchargement des commentaires (max: {max_comments})...")
        
        downloader = YoutubeCommentDownloader()
        comments = []
        
        try:
            for idx, comment in enumerate(downloader.get_comments_from_url(
                f"https://www.youtube.com/watch?v={video_id}",
                sort_by=1  # 0 = top, 1 = newest (sort_by parameter)
            )):
                if idx >= max_comments:
                    break
                
                comments.append({
                    'text': comment['text'],
                    'author': comment.get('author', 'Anonyme'),
                    'likes': comment.get('votes', 0),
                    'time': comment.get('time', '')
                })
                
                if (idx + 1) % 50 == 0:
                    logger.info(f"  ⏳ {idx + 1} commentaires téléchargés...")
            
            logger.info(f"✅ {len(comments)} commentaires téléchargés")
            
            # Trier par likes après téléchargement pour avoir les plus populaires
            comments.sort(key=lambda x: x['likes'], reverse=True)
            
            return comments
            
        except Exception as e:
            logger.error(f"❌ Erreur téléchargement: {e}")
            raise
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyse le sentiment d'un texte
        
        Args:
            text: Texte à analyser
            
        Returns:
            Tuple (sentiment, confidence) où sentiment est 'positive', 'negative' ou 'neutral'
        """
        if not text or len(text.strip()) < 3:
            return ('neutral', 0.5)
        
        try:
            result = self.sentiment_analyzer(text[:512])[0]
            label = result['label'].lower()
            score = result['score']
            
            # Le modèle cardiffnlp retourne directement: positive, negative, neutral
            if label == 'positive':
                return ('positive', score)
            elif label == 'negative':
                return ('negative', score)
            else:
                return ('neutral', score)
                
        except Exception as e:
            logger.debug(f"⚠️ Erreur analyse: {e}")
            return ('neutral', 0.5)
    
    def analyze_comments(self, comments: List[Dict]) -> Dict:
        """
        Analyse le sentiment de tous les commentaires
        
        Args:
            comments: Liste des commentaires
            
        Returns:
            Dictionnaire avec statistiques et résultats
        """
        logger.info(f"🔍 Analyse de {len(comments)} commentaires...")
        
        results = {
            'positive': [],
            'negative': [],
            'neutral': []
        }
        
        for idx, comment in enumerate(comments):
            sentiment, confidence = self.analyze_sentiment(comment['text'])
            
            comment_result = {
                **comment,
                'sentiment': sentiment,
                'confidence': confidence
            }
            
            results[sentiment].append(comment_result)
            
            if (idx + 1) % 50 == 0:
                logger.info(f"  ⏳ {idx + 1}/{len(comments)} commentaires analysés...")
        
        # Statistiques
        total = len(comments)
        stats = {
            'total_comments': total,
            'positive': {
                'count': len(results['positive']),
                'percentage': (len(results['positive']) / total * 100) if total > 0 else 0,
                'comments': results['positive']
            },
            'negative': {
                'count': len(results['negative']),
                'percentage': (len(results['negative']) / total * 100) if total > 0 else 0,
                'comments': results['negative']
            },
            'neutral': {
                'count': len(results['neutral']),
                'percentage': (len(results['neutral']) / total * 100) if total > 0 else 0,
                'comments': results['neutral']
            }
        }
        
        logger.info("✅ Analyse terminée")
        logger.info(f"   😊 Positif: {stats['positive']['percentage']:.1f}%")
        logger.info(f"   😐 Neutre:  {stats['neutral']['percentage']:.1f}%")
        logger.info(f"   😢 Négatif: {stats['negative']['percentage']:.1f}%")
        
        return stats
    
    def get_top_comments(self, comments: List[Dict], sentiment: str, n: int = 5) -> List[Dict]:
        """
        Récupère les top N commentaires d'un sentiment donné
        
        Args:
            comments: Liste des commentaires avec sentiment
            sentiment: Type de sentiment ('positive', 'negative', 'neutral')
            n: Nombre de commentaires à retourner
            
        Returns:
            Top N commentaires triés par likes
        """
        filtered = [c for c in comments if c.get('sentiment') == sentiment]
        sorted_comments = sorted(filtered, key=lambda x: x.get('likes', 0), reverse=True)
        return sorted_comments[:n]
    
    def analyze_video(self, url: str, max_comments: int = 500) -> Dict:
        """
        Analyse complète d'une vidéo YouTube
        
        Args:
            url: URL de la vidéo YouTube
            max_comments: Nombre maximum de commentaires à analyser
            
        Returns:
            Statistiques complètes de l'analyse
        """
        try:
            # Extraire l'ID de la vidéo
            video_id = self.extract_video_id(url)
            logger.info(f"🎬 Vidéo ID: {video_id}")
            
            # Télécharger les commentaires
            comments = self.download_comments(video_id, max_comments)
            
            if not comments:
                raise ValueError("Aucun commentaire trouvé pour cette vidéo")
            
            # Analyser les sentiments
            stats = self.analyze_comments(comments)
            
            # Ajouter les top commentaires
            all_comments = (
                stats['positive']['comments'] +
                stats['negative']['comments'] +
                stats['neutral']['comments']
            )
            
            stats['top_positive'] = self.get_top_comments(all_comments, 'positive', 5)
            stats['top_negative'] = self.get_top_comments(all_comments, 'negative', 5)
            
            stats['video_url'] = url
            stats['video_id'] = video_id
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse vidéo: {e}")
            raise
