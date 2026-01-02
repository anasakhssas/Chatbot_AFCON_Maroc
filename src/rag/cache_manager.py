"""
Gestionnaire de cache pour les réponses du chatbot
Optimise les performances en évitant de recalculer les réponses identiques
"""

import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ResponseCache:
    """
    Cache intelligent pour les réponses du chatbot
    
    Features:
    - Cache basé sur hash MD5 de la question
    - TTL (Time To Live) configurable
    - Statistiques d'utilisation (hit rate)
    - Nettoyage automatique des entrées expirées
    """
    
    def __init__(
        self,
        cache_dir: Path = Path("cache/responses"),
        ttl_hours: int = 24,
        max_cache_size_mb: int = 100
    ):
        """
        Initialiser le cache
        
        Args:
            cache_dir: Répertoire de stockage du cache
            ttl_hours: Durée de vie des entrées en heures
            max_cache_size_mb: Taille maximale du cache en MB
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.ttl_hours = ttl_hours
        self.max_cache_size_mb = max_cache_size_mb
        
        # Statistiques
        self.hits = 0
        self.misses = 0
        
        logger.info(f"📦 Cache initialisé: {self.cache_dir} (TTL: {ttl_hours}h)")
    
    def _normalize_question(self, question: str) -> str:
        """Normaliser une question pour le cache"""
        # Supprimer espaces, ponctuation, mettre en minuscules
        normalized = question.lower().strip()
        normalized = ''.join(c for c in normalized if c.isalnum() or c.isspace())
        return normalized
    
    def _hash_question(self, question: str) -> str:
        """Générer un hash MD5 de la question"""
        normalized = self._normalize_question(question)
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _get_cache_file(self, question: str) -> Path:
        """Obtenir le chemin du fichier cache"""
        hash_key = self._hash_question(question)
        return self.cache_dir / f"{hash_key}.json"
    
    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """Vérifier si une entrée cache est expirée"""
        cached_time = datetime.fromisoformat(cache_entry['cached_at'])
        expiry_time = cached_time + timedelta(hours=self.ttl_hours)
        return datetime.now() > expiry_time
    
    def get(self, question: str) -> Optional[Dict[str, Any]]:
        """
        Récupérer une réponse du cache
        
        Args:
            question: La question à rechercher
            
        Returns:
            La réponse cachée ou None si non trouvée/expirée
        """
        cache_file = self._get_cache_file(question)
        
        if not cache_file.exists():
            self.misses += 1
            logger.debug(f"❌ Cache miss: {question[:50]}...")
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_entry = json.load(f)
            
            # Vérifier expiration
            if self._is_expired(cache_entry):
                logger.debug(f"⏰ Cache expiré: {question[:50]}...")
                cache_file.unlink()  # Supprimer l'entrée expirée
                self.misses += 1
                return None
            
            self.hits += 1
            logger.info(f"✅ Cache hit: {question[:50]}...")
            return cache_entry['response']
            
        except Exception as e:
            logger.error(f"Erreur lecture cache: {e}")
            self.misses += 1
            return None
    
    def set(self, question: str, response: Dict[str, Any]):
        """
        Sauvegarder une réponse dans le cache
        
        Args:
            question: La question
            response: La réponse à cacher
        """
        cache_file = self._get_cache_file(question)
        
        cache_entry = {
            'question': question,
            'response': response,
            'cached_at': datetime.now().isoformat(),
            'ttl_hours': self.ttl_hours
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_entry, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"💾 Réponse cachée: {question[:50]}...")
            
            # Vérifier la taille du cache
            self._check_cache_size()
            
        except Exception as e:
            logger.error(f"Erreur écriture cache: {e}")
    
    def _check_cache_size(self):
        """Vérifier et limiter la taille du cache"""
        total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*.json"))
        total_size_mb = total_size / (1024 * 1024)
        
        if total_size_mb > self.max_cache_size_mb:
            logger.warning(f"⚠️ Cache trop grand ({total_size_mb:.1f} MB), nettoyage...")
            self.clean_expired()
    
    def clean_expired(self):
        """Nettoyer toutes les entrées expirées"""
        removed = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_entry = json.load(f)
                
                if self._is_expired(cache_entry):
                    cache_file.unlink()
                    removed += 1
            except Exception as e:
                logger.error(f"Erreur nettoyage {cache_file}: {e}")
        
        if removed > 0:
            logger.info(f"🗑️ {removed} entrées expirées supprimées")
    
    def clear(self):
        """Vider complètement le cache"""
        removed = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            removed += 1
        
        logger.info(f"🗑️ Cache vidé: {removed} entrées supprimées")
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtenir les statistiques du cache"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total_requests': total_requests,
            'hit_rate': round(hit_rate, 2),
            'cached_entries': len(cache_files),
            'cache_size_mb': round(total_size / (1024 * 1024), 2),
            'ttl_hours': self.ttl_hours
        }
    
    def print_stats(self):
        """Afficher les statistiques"""
        stats = self.get_stats()
        
        print("\n📊 STATISTIQUES DU CACHE")
        print("=" * 60)
        print(f"Total requêtes     : {stats['total_requests']}")
        print(f"Cache hits         : {stats['hits']}")
        print(f"Cache misses       : {stats['misses']}")
        print(f"Taux de hit        : {stats['hit_rate']}%")
        print(f"Entrées cachées    : {stats['cached_entries']}")
        print(f"Taille cache       : {stats['cache_size_mb']} MB")
        print(f"TTL                : {stats['ttl_hours']} heures")
        print("=" * 60)


# Exemple d'utilisation
if __name__ == "__main__":
    # Tester le cache
    cache = ResponseCache()
    
    # Simuler des requêtes
    test_question = "Où se déroule la CAN 2025?"
    test_response = {
        'answer': "La CAN 2025 se déroule au Maroc.",
        'sources': [],
        'timestamp': datetime.now().isoformat()
    }
    
    # Première requête (miss)
    result = cache.get(test_question)
    print(f"Première requête: {result}")
    
    # Sauvegarder
    cache.set(test_question, test_response)
    
    # Deuxième requête (hit)
    result = cache.get(test_question)
    print(f"Deuxième requête: {result}")
    
    # Afficher stats
    cache.print_stats()
