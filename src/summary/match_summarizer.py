"""
Module de résumé automatique de matchs de football
Génère des résumés structurés à partir de textes longs
"""

from groq import Groq
import os
import re
import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MatchSummarizer:
    """Générateur de résumés de matchs avec Groq LLM"""
    
    def __init__(self):
        """Initialise le résumeur avec l'API Groq"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY non trouvée dans les variables d'environnement")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        
        logger.info("✅ MatchSummarizer initialisé avec Groq")
    
    def extract_basic_info(self, text: str) -> Dict:
        """
        Extrait les informations de base avec regex
        
        Args:
            text: Texte source du match
            
        Returns:
            Dict avec équipes, score, date si trouvés
        """
        info = {}
        
        # Pattern pour score (ex: "Maroc 2-1 Égypte" ou "2-1")
        score_pattern = r'(\d+)\s*[-:]\s*(\d+)'
        score_match = re.search(score_pattern, text)
        if score_match:
            info['score'] = f"{score_match.group(1)}-{score_match.group(2)}"
        
        # Pattern pour équipes communes
        teams_patterns = [
            r'(Maroc|Égypte|Sénégal|Nigeria|Ghana|Cameroun|Côte d\'Ivoire|Algérie)',
            r'(Morocco|Egypt|Senegal|Nigeria|Ghana|Cameroon|Algeria)',
        ]
        
        teams_found = []
        for pattern in teams_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            teams_found.extend(matches)
        
        # Prendre les 2 premières équipes uniques
        unique_teams = []
        for team in teams_found:
            if team not in unique_teams:
                unique_teams.append(team)
            if len(unique_teams) == 2:
                break
        
        if len(unique_teams) == 2:
            info['teams'] = unique_teams
        
        return info
    
    def generate_summary(
        self,
        text: str,
        length: str = "medium",
        language: str = "fr"
    ) -> Dict:
        """
        Génère un résumé de match avec Groq
        
        Args:
            text: Texte complet du match à résumer
            length: "short" (50 mots), "medium" (150 mots), "long" (300 mots)
            language: "fr" ou "en"
            
        Returns:
            Dict avec le résumé et métadonnées
        """
        # Déterminer le nombre de mots cible
        word_limits = {
            "short": 50,
            "medium": 150,
            "long": 300
        }
        max_words = word_limits.get(length, 150)
        
        # Langue du prompt
        lang_instructions = {
            "fr": "en français",
            "en": "in English"
        }
        lang_instruction = lang_instructions.get(language, "en français")
        
        # Prompt structuré pour Groq
        prompt = f"""Tu es un expert en résumé de matchs de football. Analyse le texte suivant et génère un résumé structuré {lang_instruction}.

TEXTE DU MATCH:
{text[:4000]}

INSTRUCTIONS:
1. Identifie les équipes et le score final
2. Liste les buteurs avec les minutes des buts
3. Mentionne les moments clés (cartons, penalties, etc.)
4. Donne 2-3 statistiques importantes (possession, tirs, etc.)
5. Indique l'homme du match si mentionné
6. Ajoute un paragraphe de contexte (1-2 phrases)

FORMAT SOUHAITÉ:
🏆 [Équipe 1] [Score] [Équipe 2]

⚽ Buts:
• [Minute]' - [Joueur] ([Équipe])
• [Minute]' - [Joueur] ([Équipe])

📊 Statistiques:
• Possession: [%] - [%]
• Tirs cadrés: [X]-[X]

🌟 Homme du match: [Joueur]

💬 [Paragraphe de contexte]

CONTRAINTE: Maximum {max_words} mots au total."""

        try:
            logger.info(f"🔄 Génération du résumé ({length}, {language})...")
            
            # Appel à Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un expert en résumé de matchs de football. Tu génères des résumés structurés, précis et concis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800,
            )
            
            summary_text = response.choices[0].message.content
            
            # Extraire infos de base pour métadonnées
            basic_info = self.extract_basic_info(text)
            
            result = {
                "summary": summary_text,
                "length": length,
                "language": language,
                "word_count": len(summary_text.split()),
                "generated_at": datetime.now().isoformat(),
                "model": self.model,
                **basic_info
            }
            
            logger.info(f"✅ Résumé généré ({result['word_count']} mots)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur génération résumé: {e}")
            raise
    
    def generate_multiple_summaries(
        self,
        texts: List[Dict],
        length: str = "medium",
        language: str = "fr",
        delay: float = 2.0
    ) -> List[Dict]:
        """
        Génère des résumés pour plusieurs matchs
        
        Args:
            texts: Liste de dicts avec 'text' et optionnel 'title'
            length: Longueur du résumé
            language: Langue
            delay: Délai entre chaque résumé (pour respecter rate limit)
            
        Returns:
            Liste de résumés générés
        """
        import time
        
        summaries = []
        total = len(texts)
        
        logger.info(f"📚 Génération de {total} résumés...")
        
        for idx, item in enumerate(texts, 1):
            try:
                text = item.get('text', '')
                title = item.get('title', f'Match {idx}')
                
                logger.info(f"  ⏳ [{idx}/{total}] {title[:50]}...")
                
                summary = self.generate_summary(text, length, language)
                summary['title'] = title
                summary['index'] = idx
                
                summaries.append(summary)
                
                # Délai pour respecter rate limit
                if idx < total:
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"  ❌ Erreur pour match {idx}: {e}")
                summaries.append({
                    "title": title,
                    "index": idx,
                    "error": str(e)
                })
        
        logger.info(f"✅ {len([s for s in summaries if 'error' not in s])}/{total} résumés générés")
        return summaries
    
    def save_summary(self, summary: Dict, filepath: str):
        """Sauvegarde un résumé en JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            logger.info(f"💾 Résumé sauvegardé: {filepath}")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            raise
    
    def load_summary(self, filepath: str) -> Dict:
        """Charge un résumé depuis JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Erreur chargement: {e}")
            raise


def create_digest(summaries: List[Dict], title: str = "Résumé de la Journée") -> str:
    """
    Crée un digest HTML de plusieurs résumés
    
    Args:
        summaries: Liste de résumés
        title: Titre du digest
        
    Returns:
        HTML formaté
    """
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #C1272D 0%, #006233 100%);
            }}
            .container {{
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            h1 {{
                color: #C1272D;
                text-align: center;
                border-bottom: 3px solid #006233;
                padding-bottom: 10px;
            }}
            .match-summary {{
                margin: 20px 0;
                padding: 15px;
                border-left: 4px solid #C1272D;
                background: #f8f9fa;
                border-radius: 5px;
            }}
            .match-title {{
                font-weight: bold;
                color: #006233;
                font-size: 1.2em;
                margin-bottom: 10px;
            }}
            .summary-content {{
                white-space: pre-wrap;
                line-height: 1.6;
            }}
            .footer {{
                text-align: center;
                color: #666;
                margin-top: 30px;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏆 {title}</h1>
            <p style="text-align: center; color: #666;">
                {len(summaries)} matchs • {datetime.now().strftime('%d/%m/%Y')}
            </p>
    """
    
    for summary in summaries:
        if 'error' not in summary:
            html += f"""
            <div class="match-summary">
                <div class="match-title">{summary.get('title', 'Match')}</div>
                <div class="summary-content">{summary.get('summary', '')}</div>
            </div>
            """
    
    html += """
            <div class="footer">
                <p>⚽ Généré automatiquement par Chatbot CAN 2025 🇲🇦</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    # Test du résumeur
    from dotenv import load_dotenv
    load_dotenv()
    
    summarizer = MatchSummarizer()
    
    # Exemple de texte
    sample_text = """
    Match passionnant hier soir au stade Mohammed V de Casablanca.
    Le Maroc affrontait l'Égypte dans un match crucial pour la qualification.
    
    Brahim Díaz a ouvert le score à la 23ème minute sur une passe décisive d'Achraf Hakimi.
    Le Maroc dominait largement avec 58% de possession de balle.
    
    Mohamed Salah a égalisé à la 67ème minute sur penalty après une faute de Mazraoui.
    
    Mais c'est Achraf Hakimi qui a offert la victoire au Maroc à la 89ème minute
    avec une frappe puissante qui a battu El Shenawy.
    
    Score final: Maroc 2-1 Égypte
    
    Statistiques: Maroc 7 tirs cadrés, Égypte 5 tirs cadrés.
    Hakimi élu homme du match pour sa performance exceptionnelle.
    
    Cette victoire permet au Maroc de prendre la tête du groupe avec 6 points.
    """
    
    print("\n🧪 Test du résumeur de matchs\n")
    
    # Test résumé court
    print("📝 Génération résumé court...")
    short_summary = summarizer.generate_summary(sample_text, length="short", language="fr")
    print(f"\n{short_summary['summary']}\n")
    print(f"Mots: {short_summary['word_count']}")
    
    print("\n" + "="*70 + "\n")
    
    # Test résumé moyen
    print("📝 Génération résumé moyen...")
    medium_summary = summarizer.generate_summary(sample_text, length="medium", language="fr")
    print(f"\n{medium_summary['summary']}\n")
    print(f"Mots: {medium_summary['word_count']}")
