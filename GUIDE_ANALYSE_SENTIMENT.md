# 📊 Analyse de Sentiment - Guide d'Utilisation

## Vue d'ensemble

La fonctionnalité **Analyse de Sentiment** permet d'analyser automatiquement les commentaires YouTube sur des vidéos liées à la CAN 2025. L'outil extrait les commentaires, analyse leur sentiment (positif, neutre, négatif), et présente les résultats avec des visualisations interactives.

## 🎯 Fonctionnalités

### Version Basique (Actuelle)

✅ **Extraction de commentaires YouTube**
- Téléchargement automatique des commentaires
- Support jusqu'à 1000 commentaires par vidéo
- Tri par popularité (commentaires les plus likés)

✅ **Analyse de sentiment multilingue**
- Modèle: `nlptown/bert-base-multilingual-uncased-sentiment`
- Support: Français, Anglais, Arabe
- Classification: Positif / Neutre / Négatif
- Score de confiance pour chaque commentaire

✅ **Visualisations interactives**
- Graphique en camembert (distribution des sentiments)
- Graphique en barres (nombre de commentaires)
- Nuage de mots (mots les plus fréquents)
- Distribution des scores de confiance

✅ **Top commentaires**
- Top 5 commentaires positifs (les plus likés)
- Top 5 commentaires négatifs (les plus likés)
- Affichage de l'auteur, nombre de likes, confiance

## 📋 Comment utiliser

### 1. Accéder à l'outil

1. Lancez l'application Streamlit: `streamlit run src/app.py`
2. Dans la barre latérale, sélectionnez **"📊 Analyse de Sentiment"**

### 2. Analyser une vidéo YouTube

1. **Trouver une vidéo YouTube sur la CAN 2025**
   - Exemple: Résumés de matchs, interviews, analyses
   
2. **Copier l'URL de la vidéo**
   - Format accepté: `https://www.youtube.com/watch?v=VIDEO_ID`
   - Ou: `https://youtu.be/VIDEO_ID`

3. **Coller l'URL dans le champ**
   - Collez l'URL dans le champ "🔗 URL de la vidéo YouTube"

4. **Configurer les options (optionnel)**
   - Cliquez sur "⚙️ Options avancées"
   - Ajustez le nombre de commentaires (50-1000)
   - Activez/désactivez le nuage de mots
   - Activez/désactivez la distribution de confiance

5. **Lancer l'analyse**
   - Cliquez sur "🔍 Analyser les commentaires"
   - Attendez que l'analyse se termine (30s - 2min selon le nombre de commentaires)

### 3. Interpréter les résultats

#### Métriques principales
- **😊 Positif**: Pourcentage de commentaires positifs
- **😐 Neutre**: Pourcentage de commentaires neutres
- **😢 Négatif**: Pourcentage de commentaires négatifs

#### Graphiques
- **Camembert**: Vue d'ensemble rapide de la distribution
- **Barres**: Nombre absolu de commentaires par sentiment

#### Nuage de mots
- **Tous**: Mots les plus fréquents dans tous les commentaires
- **Positifs**: Mots des commentaires positifs uniquement
- **Négatifs**: Mots des commentaires négatifs uniquement

#### Top commentaires
- **Top 5 Positifs**: Commentaires les plus likés avec sentiment positif
- **Top 5 Négatifs**: Commentaires les plus likés avec sentiment négatif

## 🛠️ Architecture Technique

### Modules

```
src/sentiment/
├── __init__.py                  # Package initialization
├── youtube_analyzer.py          # Extraction + Analyse YouTube
└── visualizer.py                # Génération de graphiques
```

### Dépendances

```python
# Extraction de commentaires
youtube-comment-downloader       # Téléchargement commentaires YouTube

# Analyse de sentiment
transformers                     # Modèles Hugging Face
torch                           # Backend PyTorch

# Visualisations
plotly                          # Graphiques interactifs
wordcloud                       # Nuages de mots
matplotlib                      # Backend pour wordcloud
```

### Modèle d'analyse

**nlptown/bert-base-multilingual-uncased-sentiment**
- Type: BERT multilingue
- Tâche: Sentiment analysis (5 étoiles)
- Langues: FR, EN, AR, ES, IT, NL
- Mapping:
  - 1-2 étoiles → Négatif
  - 3 étoiles → Neutre
  - 4-5 étoiles → Positif

## 📊 Exemples d'utilisation

### Cas d'usage 1: Analyser la réaction à un match

**Objectif**: Comprendre le sentiment des supporters après Maroc vs Égypte

1. Trouver une vidéo de résumé du match sur YouTube
2. Analyser les commentaires (500 commentaires recommandé)
3. Observer:
   - Sentiment majoritaire (positif si victoire, négatif si défaite)
   - Mots clés dans le nuage (noms des joueurs, tactiques)
   - Top commentaires pour comprendre les points marquants

### Cas d'usage 2: Comparer avant/après un événement

**Objectif**: Évolution du sentiment suite à une annonce (composition d'équipe, blessure)

1. Analyser une vidéo publiée AVANT l'annonce
2. Analyser une vidéo publiée APRÈS l'annonce
3. Comparer les pourcentages de sentiments
4. Identifier les changements dans les mots clés

### Cas d'usage 3: Identifier les préoccupations des fans

**Objectif**: Trouver les sujets qui inquiètent ou enthousiasment les supporters

1. Analyser plusieurs vidéos d'analyses tactiques
2. Examiner les top commentaires négatifs (préoccupations)
3. Examiner les top commentaires positifs (points forts)
4. Utiliser le nuage de mots pour identifier les thèmes récurrents

## ⚠️ Limitations

### Limitations techniques

1. **Limite de commentaires**
   - Maximum 1000 commentaires par analyse
   - Commentaires triés par popularité (top comments)
   - Les commentaires récents non populaires peuvent être exclus

2. **Vidéos sans commentaires**
   - Nécessite que les commentaires soient activés
   - Impossible d'analyser une vidéo sans commentaires

3. **Temps de traitement**
   - 50 commentaires: ~30 secondes
   - 500 commentaires: ~2 minutes
   - 1000 commentaires: ~4 minutes

4. **Précision du modèle**
   - Le modèle peut mal interpréter le sarcasme
   - Les emojis complexes peuvent être mal classés
   - Le contexte culturel peut influencer la classification

### Limitations de contenu

1. **Langue**
   - Optimisé pour FR/EN/AR
   - Autres langues: précision réduite

2. **Spam et bots**
   - Les commentaires spam peuvent biaiser l'analyse
   - Recommandé: analyser des vidéos modérées

3. **Commentaires courts**
   - Commentaires < 3 caractères: classés neutres par défaut
   - Emojis seuls: difficulté de classification

## 🔮 Évolutions futures

### Version Avancée (Roadmap)

- [ ] Support Facebook (Graph API)
- [ ] Support Twitter/X (API v2)
- [ ] Support Instagram (commentaires publics)
- [ ] Analyse de tendances temporelles
- [ ] Comparaison multi-vidéos
- [ ] Export des résultats (PDF, Excel)

### Version Pro (Roadmap)

- [ ] Analyse en temps réel (streaming)
- [ ] Détection d'émotions (8+ émotions)
- [ ] Analyse de sarcasme/ironie
- [ ] Identification des influenceurs
- [ ] Dashboard de monitoring
- [ ] API REST pour intégration externe

## 🐛 Dépannage

### Erreur: "URL YouTube invalide"

**Cause**: Format d'URL non reconnu

**Solution**:
- Vérifier le format: `https://www.youtube.com/watch?v=VIDEO_ID`
- Éviter les URLs raccourcies ou avec paramètres supplémentaires
- Copier l'URL depuis la barre d'adresse du navigateur

### Erreur: "Aucun commentaire trouvé"

**Cause**: Vidéo sans commentaires ou commentaires désactivés

**Solution**:
- Vérifier que les commentaires sont activés sur YouTube
- Choisir une autre vidéo avec des commentaires

### Analyse très lente

**Cause**: Trop de commentaires à analyser

**Solution**:
- Réduire le nombre de commentaires (Options avancées)
- Commencer par 100-200 commentaires pour tester
- Augmenter progressivement si besoin

### Erreur de mémoire (OOM)

**Cause**: Modèle trop grand pour la RAM disponible

**Solution**:
- Réduire le nombre de commentaires
- Fermer d'autres applications gourmandes en RAM
- Redémarrer l'application Streamlit

## 📞 Support

Pour toute question ou bug:

1. Vérifier la documentation ci-dessus
2. Consulter les logs dans le terminal Streamlit
3. Vérifier que toutes les dépendances sont installées:
   ```bash
   pip install youtube-comment-downloader transformers torch plotly wordcloud matplotlib
   ```

## 📚 Ressources

- **Modèle de sentiment**: [nlptown/bert-base-multilingual-uncased-sentiment](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment)
- **YouTube Comment Downloader**: [PyPI](https://pypi.org/project/youtube-comment-downloader/)
- **Plotly**: [Documentation](https://plotly.com/python/)
- **WordCloud**: [Documentation](https://amueller.github.io/word_cloud/)

---

**Version**: 1.0 - Version Basique  
**Date**: Janvier 2026  
**Auteur**: Chatbot CAN 2025 Team
