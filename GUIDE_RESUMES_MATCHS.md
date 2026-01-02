# 📝 Guide - Résumés Automatiques de Matchs

## 🎯 Vue d'ensemble

Cette fonctionnalité permet de générer automatiquement des résumés structurés de matchs de football à partir d'articles de presse ou de textes longs. Les résumés peuvent être exportés en PDF professionnel ou en cartes visuelles pour les réseaux sociaux.

## ✨ Fonctionnalités

### 1. Génération de Résumés
- **3 longueurs disponibles** :
  - Court : ~50 mots (résumé ultra-concis)
  - Moyen : ~150 mots (résumé équilibré)
  - Long : ~300 mots (résumé détaillé)

- **2 langues** : Français et English

- **Format structuré automatique** :
  ```
  🏆 [Équipe 1] [Score] [Équipe 2]
  
  ⚽ Buts:
  • [Minute]' - [Joueur] ([Équipe])
  
  📊 Statistiques:
  • Possession: [%] - [%]
  • Tirs cadrés: [X]-[X]
  
  🌟 Homme du match: [Joueur]
  
  💬 [Contexte du match]
  ```

### 2. Export Multi-Formats

#### PDF Professionnel
- Design aux couleurs du Maroc (rouge #C1272D, vert #006233)
- Mise en page soignée avec ReportLab
- Titres, scores, métadonnées
- Footer personnalisé
- Support multi-résumés (digest compilé)

#### Cartes Visuelles
- Format 1080×1080 pour Instagram/Facebook
- Bandes rouge (haut) et verte (bas) aux couleurs du Maroc
- Score en grand au centre
- Informations clés affichées
- Prêt à partager sur les réseaux sociaux

#### Texte
- Copie directe dans le presse-papiers
- Format Markdown compatible

### 3. Modes d'Utilisation

#### Mode Simple
1. Collez le texte d'un article de match (ou URL Wikipedia)
2. Choisissez la longueur (court/moyen/long)
3. Sélectionnez la langue
4. Cliquez "Générer le Résumé"
5. Exportez en PDF, Image ou Texte

#### Mode Batch
1. Collez plusieurs articles séparés par `---`
2. Configurez les options
3. Générez tous les résumés en une fois
4. Téléchargez le PDF compilé avec tous les matchs

#### Mode Historique
- Consultez tous les résumés générés dans la session
- Exportez l'historique complet en PDF
- Réutilisez les résumés précédents

## 🛠️ Composants Techniques

### Module `match_summarizer.py`
```python
class MatchSummarizer:
    - generate_summary(text, length, language) -> Dict
    - generate_multiple_summaries(texts, length, language) -> List[Dict]
    - extract_basic_info(text) -> Dict
    - save_summary(summary, filepath)
    - load_summary(filepath) -> Dict
```

**Fonctionnalités** :
- Utilise Groq API avec llama-3.3-70b
- Extraction automatique du score, équipes, buteurs
- Température 0.3 pour cohérence
- Rate limit respecté (2s entre chaque résumé)

### Module `exporters.py`

#### PDFExporter
```python
class PDFExporter:
    - export_single_summary(summary, filepath)
    - export_multiple_summaries(summaries, filepath, title)
```

**Caractéristiques** :
- ReportLab pour génération PDF
- Styles personnalisés (titre, sous-titre, corps)
- Couleurs Maroc (rouge, vert)
- Mise en page A4 professionnelle

#### ImageExporter
```python
class ImageExporter:
    - create_social_card(summary, filepath, size=(1080, 1080))
    - create_story_card(summary, filepath)  # 1080×1920
```

**Caractéristiques** :
- PIL/Pillow pour génération d'images
- Design personnalisé aux couleurs du Maroc
- Bandes colorées haut/bas
- Texte centré et hiérarchisé
- Format Instagram/Facebook optimisé

## 💰 Coûts et Limites

### 100% Gratuit ✅
- **Groq API** : Gratuite, 30 requêtes/minute
- **ReportLab** : Open-source gratuit
- **Pillow** : Open-source gratuit
- **Streamlit** : Open-source gratuit

### Calcul de Coût
```
100 résumés × 500 tokens = 50,000 tokens
Groq API gratuite : 0€
Temps estimé : 3-4 minutes (avec délai de 2s)
```

### Rate Limit
- Groq : 30 requêtes/minute
- Délai automatique de 2s entre chaque résumé en mode batch
- Alternative : Ollama (local, illimité)

## 📊 Exemples d'Utilisation

### Exemple 1 : Résumé Simple
```python
from src.summary.match_summarizer import MatchSummarizer

summarizer = MatchSummarizer()

text = """
[Article complet du match...]
"""

summary = summarizer.generate_summary(
    text=text,
    length="medium",  # court, moyen, ou long
    language="fr"     # fr ou en
)

print(summary['summary'])
# Affiche le résumé structuré
```

### Exemple 2 : Export PDF
```python
from src.summary.exporters import PDFExporter

pdf_exporter = PDFExporter()

pdf_exporter.export_single_summary(
    summary=summary,
    filepath="exports/match_maroc_egypte.pdf"
)
```

### Exemple 3 : Carte Sociale
```python
from src.summary.exporters import ImageExporter

img_exporter = ImageExporter()

img_exporter.create_social_card(
    summary=summary,
    filepath="exports/card_maroc_egypte.png",
    size=(1080, 1080)  # Instagram
)
```

### Exemple 4 : Batch Processing
```python
texts = [
    {"text": "Article match 1...", "title": "Maroc vs Égypte"},
    {"text": "Article match 2...", "title": "Sénégal vs Nigeria"},
    {"text": "Article match 3...", "title": "Ghana vs Cameroun"}
]

summaries = summarizer.generate_multiple_summaries(
    texts=texts,
    length="medium",
    language="fr",
    delay=2.0  # Respecter rate limit
)

# Export PDF compilé
pdf_exporter.export_multiple_summaries(
    summaries=summaries,
    filepath="exports/digest_journee2.pdf",
    title="Résumés CAN 2025 - Journée 2"
)
```

## 🎨 Personnalisation

### Changer les Couleurs
Dans `exporters.py` :
```python
class ImageExporter:
    def __init__(self):
        self.maroc_red = (193, 39, 45)      # Rouge Maroc
        self.maroc_green = (0, 98, 51)      # Vert Maroc
        self.white = (255, 255, 255)
        self.light_gray = (245, 245, 245)
```

### Modifier le Prompt
Dans `match_summarizer.py`, méthode `generate_summary()` :
```python
prompt = f"""Tu es un expert en résumé de matchs...

FORMAT SOUHAITÉ:
🏆 [Équipe 1] [Score] [Équipe 2]
...

CONTRAINTE: Maximum {max_words} mots au total."""
```

### Ajuster la Température
Pour résumés plus créatifs (moins cohérents) :
```python
response = self.client.chat.completions.create(
    model=self.model,
    temperature=0.7,  # Augmenter pour plus de variété
    ...
)
```

## 🔧 Dépannage

### Erreur "GROQ_API_KEY non trouvée"
- Vérifiez que `.env` contient `GROQ_API_KEY=votre_cle`
- Rechargez l'environnement : `load_dotenv()`

### Erreur "Rate limit exceeded"
- Ajoutez un délai de 2-3 secondes entre chaque résumé
- Réduisez le nombre de résumés simultanés
- Utilisez Ollama en local (illimité)

### PDF ne s'affiche pas correctement
- Vérifiez que ReportLab est installé : `pip install reportlab`
- Vérifiez les permissions d'écriture dans `exports/`

### Images floues
- Augmentez la taille : `size=(2160, 2160)` (4K)
- Utilisez des polices TrueType : `arial.ttf`, `arialbd.ttf`

### Résumés trop courts/longs
- Ajustez les limites dans `word_limits` :
```python
word_limits = {
    "short": 50,
    "medium": 150,
    "long": 300
}
```

## 📈 Améliorations Futures

### v2.0 (Suggestions)
- [ ] Support de plus de langues (Arabe, Espagnol)
- [ ] Export Word/HTML en plus de PDF
- [ ] Templates personnalisables par équipe
- [ ] Intégration avec ChromaDB pour recherche
- [ ] API REST pour génération automatisée
- [ ] Webhooks pour auto-génération après matchs
- [ ] Stories Instagram verticales (1080×1920)
- [ ] Animations GIF pour réseaux sociaux
- [ ] Comparaison multi-matchs (tableaux)
- [ ] Newsletter automatique par email

## 📚 Ressources

- **Documentation Groq** : https://console.groq.com/docs
- **ReportLab Guide** : https://www.reportlab.com/docs/reportlab-userguide.pdf
- **Pillow Docs** : https://pillow.readthedocs.io/
- **Streamlit Docs** : https://docs.streamlit.io/

## 🤝 Contribution

Pour améliorer cette fonctionnalité :
1. Fork le projet
2. Créez une branche : `git checkout -b feature/amelioration-resumes`
3. Testez vos modifications
4. Commit : `git commit -m "Amélioration: [description]"`
5. Push : `git push origin feature/amelioration-resumes`
6. Ouvrez une Pull Request

## 📝 Changelog

### v1.0.0 (2026-01-02)
- ✅ Génération de résumés avec Groq llama-3.3-70b
- ✅ 3 longueurs : court, moyen, long
- ✅ 2 langues : FR, EN
- ✅ Export PDF professionnel (ReportLab)
- ✅ Export cartes sociales 1080×1080 (Pillow)
- ✅ Mode batch (plusieurs résumés)
- ✅ Historique de session
- ✅ Interface Streamlit intégrée
- ✅ 100% gratuit avec Groq API

---

**Auteur** : Anas Akhssas  
**Projet** : Chatbot CAN 2025 Maroc  
**Date** : Janvier 2026  
**License** : MIT
