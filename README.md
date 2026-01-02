# 🏆 Chatbot CAN 2025 - Intelligence Artificielle pour la Coupe d'Afrique

Application web intelligente avec analyse de sentiment pour la CAN 2025 au Maroc. Système RAG (Retrieval-Augmented Generation) alimenté par Groq LLM et analyse de sentiment des supporters sur YouTube.

## ✨ Fonctionnalités

### 💬 Chatbot Intelligent
- Réponses basées sur des données réelles (Wikipedia)
- Recherche sémantique avec ChromaDB
- Sources affichées pour chaque réponse
- Interface de chat moderne et intuitive
- **Pas d'hallucinations** - données vérifiées uniquement

### 📊 Analyse de Sentiment YouTube
- Extraction automatique de commentaires YouTube
- Analyse multilingue (Français, Anglais, Arabe)
- Classification : Positif / Neutre / Négatif
- Visualisations interactives (graphiques, statistiques)
- Top 5 commentaires les plus populaires
- Score de confiance à 95-98% avec modèle CardiffNLP

### 🔄 Scraper Multi-Sources
- Wikipedia (FR + EN) ✅
- BBC Sport (prêt pour tournoi)
- ESPN (prêt pour tournoi)
- FlashScore (résultats en temps réel)

## 🚀 Démarrage Rapide

### 1. Installation

```bash
# Cloner le repository
git clone https://github.com/anasakhssas/Chatbot_AFCON_Maroc.git
cd Chatbot_AFCON_Maroc

# Créer l'environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration

Créez un fichier `.env` avec votre clé API Groq (gratuite) :

```bash
GROQ_API_KEY=votre_cle_ici
```

> 🎁 **Obtenez votre clé gratuite** sur : https://console.groq.com/keys
> - 30 requêtes/minute
> - Aucune carte bancaire requise
> - Modèle llama-3.3-70b ultra-rapide

### 3. Lancer l'Application

```bash
# Windows
.\venv\Scripts\python.exe -m streamlit run src/app.py

# Linux/Mac
python -m streamlit run src/app.py
```

Ouvrez votre navigateur sur : **http://localhost:8501**

## 📖 Guide d'Utilisation

### Page Chatbot

1. **Posez vos questions** sur la CAN 2025 :
   - "Où se déroule la CAN 2025 ?"
   - "Combien d'équipes participent ?"
   - "Qui sont les meilleurs buteurs ?"
   - "Quelles sont les dates du tournoi ?"

2. **Consultez les sources** affichées sous chaque réponse

3. **Historique de conversation** conservé automatiquement

### Page Analyse de Sentiment

1. **Trouvez une vidéo YouTube** sur la CAN 2025

2. **Copiez l'URL** et collez-la dans le champ

3. **Configurez les options** (facultatif) :
   - Nombre de commentaires (50-1000)
   - Afficher la distribution de confiance

4. **Cliquez sur "Analyser"** et obtenez :
   - Pourcentages de sentiments (positif/neutre/négatif)
   - Graphiques interactifs
   - Top 5 commentaires positifs/négatifs
   - Scores de confiance

## 🛠️ Technologies Utilisées

**Backend & IA :**
- **Groq API** - LLM ultra-rapide (llama-3.3-70b)
- **LangChain** - Framework RAG
- **ChromaDB** - Base vectorielle
- **HuggingFace** - Embeddings multilingues
- **CardiffNLP** - Modèle sentiment analysis (95-98% précision)

**Scraping & Données :**
- **BeautifulSoup4** - Parsing HTML
- **Requests** - HTTP avec retry logic
- **YouTube Comment Downloader** - Extraction commentaires

**Interface & Visualisation :**
- **Streamlit** - Interface web
- **Plotly** - Graphiques interactifs
- **Matplotlib** - Visualisations

## 📁 Structure du Projet

```
Chatbot_AFCON_Maroc/
├── src/
│   ├── app.py                    # Application Streamlit (point d'entrée)
│   ├── pipeline/
│   │   ├── real_scraper.py       # Scraper multi-sources optimisé
│   │   ├── pipeline.py           # Pipeline ETL
│   │   └── auto_pipeline.py      # Automatisation
│   ├── rag/
│   │   ├── chatbot.py            # Chatbot RAG
│   │   ├── vectorizer.py         # Vectorisation ChromaDB
│   │   └── config.py             # Configuration
│   └── sentiment/
│       ├── youtube_analyzer.py   # Analyseur sentiment YouTube
│       └── visualizer.py         # Graphiques et visualisations
├── data/
│   ├── raw/                      # Données brutes scrapées
│   └── transformed/              # Données transformées pour RAG
├── chroma_db/                    # Base vectorielle (généré auto)
├── tests/                        # Tests unitaires
└── requirements.txt              # Dépendances Python
```

## 🔧 Commandes Utiles

### Régénérer les Données

```bash
# Scraper les données Wikipedia
python -m src.pipeline.real_scraper

# Transformer les données
python -m src.pipeline.pipeline

# Vectoriser dans ChromaDB
python -m src.rag.vectorizer
```

### Tests

```bash
# Tester l'analyse de sentiment
python tests/test_sentiment.py

# Tester le chatbot en mode CLI
python -m src.rag.chatbot
```

## 📊 Données Sources

**Actuellement actives :**
- Wikipedia FR : https://fr.wikipedia.org/wiki/Coupe_d%27Afrique_des_nations_de_football_2025
- Wikipedia EN : https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations

**Prêtes pour activation :**
- BBC Sport : https://www.bbc.com/sport/africa
- ESPN : https://www.espn.com/soccer/
- FlashScore : https://www.flashscore.com/football/africa/africa-cup-of-nations/

## 🎯 Exemples de Questions

**Informations Générales :**
- Où se déroule la CAN 2025 ?
- Quelles sont les dates du tournoi ?
- Combien d'équipes participent ?

**Équipes & Joueurs :**
- Qui sont les meilleurs buteurs ?
- Quelles équipes sont dans le groupe A ?
- Quel pays est tenant du titre ?

**Stades & Infrastructure :**
- Quels stades accueillent les matchs ?
- Quelle est la capacité du stade principal ?
- Dans quelles villes se jouent les matchs ?

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Documentation

- **Guide d'Analyse de Sentiment** : `GUIDE_ANALYSE_SENTIMENT.md`
- **Configuration RAG** : Voir `src/rag/config.py`
- **Scraper Best Practices** : Documentation intégrée dans `real_scraper.py`

## 🐛 Problèmes Connus

- Le scraping BBC/ESPN/FlashScore nécessite ajustement des sélecteurs HTML quand le tournoi démarre
- ChromaDB doit être régénéré après modification des données sources
- L'analyse YouTube est limitée aux vidéos avec commentaires activés

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Anas Akhssas**
- GitHub: [@anasakhssas](https://github.com/anasakhssas)
- Repository: [Chatbot_AFCON_Maroc](https://github.com/anasakhssas/Chatbot_AFCON_Maroc)

## 🙏 Remerciements

- **Groq** pour l'API LLM gratuite et ultra-rapide
- **HuggingFace** pour les modèles d'embeddings et sentiment analysis
- **Streamlit** pour le framework web simple et puissant
- **Wikipedia** pour les données sources fiables

---

**⚽ Allez les Lions de l'Atlas ! 🇲🇦**
## 🛠️ Technologies Utilisées

**Backend & IA :**
- **Groq API** - LLM ultra-rapide (llama-3.3-70b)
- **LangChain** - Framework RAG
- **ChromaDB** - Base vectorielle
- **HuggingFace** - Embeddings multilingues
- **CardiffNLP** - Modèle sentiment analysis (95-98% précision)

**Scraping & Données :**
- **BeautifulSoup4** - Parsing HTML
- **Requests** - HTTP avec retry logic
- **YouTube Comment Downloader** - Extraction commentaires

**Interface & Visualisation :**
- **Streamlit** - Interface web
- **Plotly** - Graphiques interactifs
- **Matplotlib** - Visualisations

## 📁 Structure du Projet

```
Chatbot_AFCON_Maroc/
├── src/
│   ├── app.py                    # Application Streamlit (point d'entrée)
│   ├── pipeline/
│   │   ├── real_scraper.py       # Scraper multi-sources optimisé
│   │   ├── pipeline.py           # Pipeline ETL
│   │   └── auto_pipeline.py      # Automatisation
│   ├── rag/
│   │   ├── chatbot.py            # Chatbot RAG
│   │   ├── vectorizer.py         # Vectorisation ChromaDB
│   │   └── config.py             # Configuration
│   └── sentiment/
│       ├── youtube_analyzer.py   # Analyseur sentiment YouTube
│       └── visualizer.py         # Graphiques et visualisations
├── data/
│   ├── raw/                      # Données brutes scrapées
│   └── transformed/              # Données transformées pour RAG
├── chroma_db/                    # Base vectorielle (généré auto)
├── tests/                        # Tests unitaires
└── requirements.txt              # Dépendances Python
```

## 🔧 Commandes Utiles

### Régénérer les Données

```bash
# Scraper les données Wikipedia
python -m src.pipeline.real_scraper

# Transformer les données
python -m src.pipeline.pipeline

# Vectoriser dans ChromaDB
python -m src.rag.vectorizer
```

### Tests

```bash
# Tester l'analyse de sentiment
python tests/test_sentiment.py

# Tester le chatbot en mode CLI
python -m src.rag.chatbot
```

## 📊 Données Sources

**Actuellement actives :**
- Wikipedia FR : https://fr.wikipedia.org/wiki/Coupe_d%27Afrique_des_nations_de_football_2025
- Wikipedia EN : https://en.wikipedia.org/wiki/2025_Africa_Cup_of_Nations

**Prêtes pour activation :**
- BBC Sport : https://www.bbc.com/sport/africa
- ESPN : https://www.espn.com/soccer/
- FlashScore : https://www.flashscore.com/football/africa/africa-cup-of-nations/

## 🎯 Exemples de Questions

**Informations Générales :**
- Où se déroule la CAN 2025 ?
- Quelles sont les dates du tournoi ?
- Combien d'équipes participent ?

**Équipes & Joueurs :**
- Qui sont les meilleurs buteurs ?
- Quelles équipes sont dans le groupe A ?
- Quel pays est tenant du titre ?

**Stades & Infrastructure :**
- Quels stades accueillent les matchs ?
- Quelle est la capacité du stade principal ?
- Dans quelles villes se jouent les matchs ?

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Documentation

- **Guide d'Analyse de Sentiment** : `GUIDE_ANALYSE_SENTIMENT.md`
- **Configuration RAG** : Voir `src/rag/config.py`
- **Scraper Best Practices** : Documentation intégrée dans `real_scraper.py`

## 🐛 Problèmes Connus

- Le scraping BBC/ESPN/FlashScore nécessite ajustement des sélecteurs HTML quand le tournoi démarre
- ChromaDB doit être régénéré après modification des données sources
- L'analyse YouTube est limitée aux vidéos avec commentaires activés

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Anas Akhssas**
- GitHub: [@anasakhssas](https://github.com/anasakhssas)
- Repository: [Chatbot_AFCON_Maroc](https://github.com/anasakhssas/Chatbot_AFCON_Maroc)

## 🙏 Remerciements

- **Groq** pour l'API LLM gratuite et ultra-rapide
- **HuggingFace** pour les modèles d'embeddings et sentiment analysis
- **Streamlit** pour le framework web simple et puissant
- **Wikipedia** pour les données sources fiables

---

**⚽ Allez les Lions de l'Atlas ! 🇲🇦**

### 🔮 Phase 5: Amélioration (Futur)
- [ ] Fine-tuning du modèle
- [ ] Scraping en temps réel
- [ ] Notifications push
- [ ] Analytics dashboard
- [ ] Mobile app

---

## 🛠️ Technologies Utilisées

### Data Pipeline
- **Python 3.12** - Langage principal
- **Requests** - HTTP requests
- **BeautifulSoup4** - HTML parsing
- **Pathlib** - Gestion des fichiers

### RAG System
- **LangChain** - Framework RAG
- **ChromaDB** - Base vectorielle
- **OpenAI API** - Embeddings + LLM
- **Tiktoken** - Tokenization

---

## 🤝 Contribution

Ce projet est développé dans le cadre d'un Stage PFE.

---

## 📞 Support

Pour toute question:
1. Consulter la documentation (`EXPLICATION_RAG.md`, `INSTALLATION_RAG.md`)
2. Tester les exemples (`python examples\rag_examples.py`)
3. Vérifier les logs dans le terminal

---

## 📄 Licence

Projet académique - CAN 2025 Morocco Chatbot

---

**Développé avec ❤️ pour la CAN 2025 🏆⚽**

## 📰 Sources de Données

- **CAF AFCON 2025 Official**: Site officiel de la CAF pour la CAN 2025
- **CAF Official News**: Actualités générales de la CAF
- **BBC Sport AFCON**: Couverture internationale

## 🎯 Données Demo Disponibles

Les données demo incluent:
- ✅ Résultats réels de la phase de groupes (Morocco 2-0 Comoros, Egypt 2-1 Zimbabwe, etc.)
- ✅ Informations sur les joueurs (Salah, Mahrez, Brahim Díaz, etc.)
- ✅ Statistiques du tournoi (meilleurs buteurs, affluence)
- ✅ Actualités du tournoi

## 📁 Structure du Projet

```
Chatbot_AFCON_Maroc/
├── data/
│   ├── daily_fetch/          # 📥 Données brutes extraites
│   └── transformed/          # 🔄 Données transformées pour RAG
│       ├── transformed_*.json
│       └── combined_dataset.json  # Dataset combiné
├── src/
│   └── pipeline/
│       ├── __init__.py
│       ├── config.py         # Configuration des sources
│       ├── scraper.py        # Scraper web principal
│       ├── demo_scraper.py   # Générateur de données demo
│       ├── transform.py      # 🔄 Transformation pour RAG
│       └── pipeline.py       # 🚀 Pipeline ETL complet
## ✅ Étapes Complétées

- [x] Pipeline d'extraction de données (scraping + demo)
- [x] Transformation des données pour le RAG
- [x] Format optimisé avec métadonnées enrichies
- [x] Dataset combiné prêt à l'emploi
- [x] Logging et gestion d'erreurs complète
- [x] Documentation complète

## 🔜 Prochaines Étapes

- [ ] **Vectorisation** : Créer les embeddings avec OpenAI/HuggingFace
- [ ] **ChromaDB** : Stocker les vecteurs dans la base vectorielle
- [ ] **RAG avec LangChain** : Implémenter le système de récupération
- [ ] **API FastAPI** : Créer l'endpoint du chatbot
- [ ] **Interface Utilisateur** : Streamlit ou Gradio
- [ ] **Amélioration scraping** : Selenium pour pages dynamiques

## 📊 Exemple d'Utilisation des Données Transformées

```python
import json

# Charger le dataset combiné
with open('data/transformed/combined_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Accéder aux documents
documents = dataset['documents']
print(f"Total documents: {len(documents)}")

# Exemple : Filtrer par catégorie
match_results = [
    doc for doc in documents 
    if doc['metadata']['category'] == 'match_result'
]
print(f"Résultats de matchs: {len(match_results)}")

# Exemple : Recherche par mot-clé
morocco_articles = [
    doc for doc in documents 
    if 'Morocco' in doc['metadata']['keywords']
]
print(f"Articles sur le Maroc: {len(morocco_articles)}")
``` pages dynamiques
- [ ] Implémenter le système de vectorisation (embeddings)
- [ ] Créer la base vectorielle avec ChromaDB
- [ ] Développer le système RAG avec LangChain
- [ ] Créer l'API FastAPI pour le chatbot
- [ ] Interface utilisateur (Streamlit/Gradio)l de la CAF
- **BBC Sport Africa**: Actualités sportives africaines

## Prochaines Étapes

- [ ] Ajouter plus de sources de données
- [ ] Implémenter le système de vectorisation
- [ ] Créer le système RAG avec ChromaDB
- [ ] Développer l'API FastAPI
