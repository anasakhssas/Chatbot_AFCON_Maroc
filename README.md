# 🏆 CAN 2025 Chatbot - Système RAG Complet avec Interface Web

## Description
Chatbot intelligent avec système RAG (Retrieval-Augmented Generation) pour répondre aux questions sur la Coupe d'Afrique des Nations 2025 au Maroc. Utilise **Groq API gratuite** pour le LLM, **HuggingFace embeddings** (100% local), et **Streamlit** pour l'interface web moderne.

## ✅ Fonctionnalités Implémentées

### Phase 1: Pipeline ETL ✅
- ✅ Web scraping automatisé avec gestion d'erreurs
- ✅ Collecte depuis sources officielles (CAF, BBC Sport)
- ✅ Extraction structurée (titre, contenu, date, lien, mots-clés)
- ✅ Transformation pour RAG (enrichissement, métadonnées)
- ✅ Stockage JSON optimisé
- ✅ Générateur de données démo (20 articles réalistes)

### Phase 2: Système RAG ✅
- ✅ Vectorisation avec HuggingFace Embeddings (gratuit, local)
- ✅ Base vectorielle ChromaDB
- ✅ Recherche sémantique performante
- ✅ Chatbot Q&A avec LangChain + Groq (llama-3.3-70b-versatile)
- ✅ Mode interactif avec historique
- ✅ Support multi-questions (batch)

### Phase 3: Interface Web ✅ NOUVEAU
- ✅ Interface Streamlit moderne et responsive
- ✅ Chat interactif en temps réel
- ✅ Affichage des sources avec métadonnées
- ✅ Sidebar avec statistiques et exemples
- ✅ Design aux couleurs du Maroc 🇲🇦
- ✅ Questions prédéfinies pour démarrage rapide

## 📦 Installation

### 1. Dépendances Python

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer toutes les dépendances (ETL + RAG + Streamlit)
pip install -r requirements.txt
```

### 2. Configuration API Groq (GRATUITE)

```powershell
# Créer un fichier .env avec votre clé API Groq
echo "GROQ_API_KEY=votre_cle_groq_ici" > .env
```

> 🎁 **API Groq gratuite** : 30 requêtes/minute, ultra-rapide, sans carte bancaire
> Obtenez votre clé sur : https://console.groq.com/keys

## 🚀 Utilisation Rapide

### 🌐 Interface Web (Recommandé - Pipeline Automatisé)

```powershell
# Lancer l'application web Streamlit - TOUT EST AUTOMATIQUE !
.\venv\Scripts\python.exe -m streamlit run src/app.py
```

Puis ouvrez : **http://localhost:8501** dans votre navigateur

**🤖 Pipeline Automatisé :**
- ✅ **Extraction automatique** : Génère les données démo si absentes
- ✅ **Transformation automatique** : Prépare les données pour RAG
- ✅ **Vectorisation automatique** : Crée ChromaDB si nécessaire
- ✅ **Prêt à l'emploi** : Lancez et utilisez directement !

**Fonctionnalités web :**
- 💬 Chat interactif avec historique
- 📚 Affichage des sources pour chaque réponse
- 💡 Questions d'exemple prédéfinies
- 📊 Statistiques en temps réel
- 🔄 Bouton "Rafraîchir les données" pour régénérer le pipeline
- 🎨 Design moderne aux couleurs du Maroc

### 🖥️ Mode Terminal (CLI - Manuel)

Si vous voulez exécuter manuellement chaque étape :

```powershell
# 1️⃣ Générer les données et les transformer
python -m src.pipeline.pipeline

# 2️⃣ Vectoriser les données (créer ChromaDB)
python -m src.rag.vectorizer

# 3️⃣ Tester le chatbot en mode CLI
python -m src.rag.chatbot
```

**Note :** En mode web, ces étapes sont automatiques !

---

## 📚 Utilisation Détaillée

### Phase 1: Pipeline ETL

#### Option A: Pipeline Complet (Recommandé)
```powershell
# Exécute Extract → Transform en une commande
python -m src.pipeline.pipeline
```

#### Option B: Étapes Séparées
```powershell
# 1. Extraction uniquement
python -m src.pipeline.demo_scraper

# 2. Transformation uniquement
python -m src.pipeline.transform

# 3. Scraping réel (en développement)
python -m src.pipeline.scraper
```

### Phase 2: Système RAG ⭐ NOUVEAU

#### Vectorisation (Une seule fois)
```powershell
# Créer la base vectorielle ChromaDB
python -m src.rag.vectorizer
```
**Résultat:** 20 documents indexés dans `chroma_db/`

#### Chatbot Interactif
```powershell
# Lancer le chatbot avec tests puis mode interactif
python -m src.rag.chatbot
```

**Commandes dans le chat:**
- Poser une question sur la CAN 2025
- `history` - Voir l'historique
- `quit` - Quitter

#### Exemples Avancés
```powershell
# Menu avec 8 exemples détaillés
python examples\rag_examples.py
```

**Exemples disponibles:**
1. Vectorisation des données
2. Recherche sémantique
3. Questions-réponses simples
4. Questions en batch
5. Réponse détaillée avec sources
6. Comparaison de formulations
7. Statistiques du système
8. Mode interactif

---

## 🤖 Exemples de Questions

Le chatbot peut répondre à des questions comme:

```
❓ "Qui a marqué pour le Maroc ?"
💬 "Brahim Díaz a ouvert le score en 55ème minute..."

❓ "Quel est le meilleur buteur du tournoi ?"
💬 "Riyad Mahrez mène la course au soulier d'or avec 3 buts..."

❓ "Résultat du match Égypte Zimbabwe"
💬 "L'Égypte a battu le Zimbabwe 2-1..."
```

---

## 📖 Utilisation Programmatique

### Pipeline ETL
```python
# Pipeline complet
from src.pipeline.pipeline import run_complete_pipeline
run_complete_pipeline()

# Ou étapes séparées
from src.pipeline.demo_scraper import save_demo_data
from src.pipeline.transform import DataTransformer

# Extraction
filepath = save_demo_data()

# Transformation
transformer = DataTransformer()
transformer.transform_all_files()
transformer.create_combined_dataset()
```

### Système RAG
```python
from src.rag.chatbot import ChatbotCAN2025

# Créer le chatbot
chatbot = ChatbotCAN2025()

# Poser une question
response = chatbot.ask("Qui a marqué pour le Maroc ?")
print(response['answer'])
print(f"Basé sur {response['num_sources']} sources")

# Mode interactif
chatbot.chat()
```

## 📊 Structure des Données

### 1. Données Brutes (`data/daily_fetch/`)

```json
{
  "metadata": {
    "total_articles": 10,
    "fetch_date": "2026-01-01T13:34:20",
    "sources": ["CAF AFCON 2025"]
  },
  "articles": [
    {
      "id": "demo_1_20260101133420",
      "title": "Morocco Opens AFCON 2025 with Victory",
      "content": "Morocco kicked off the 2025 Africa Cup...",
      "category": "match_result",
      "keywords": ["CAN 2025", "Morocco", "Comoros"]
    }
  ]
}
```

### 2. Données Transformées (`data/transformed/`)

Format optimisé pour RAG avec texte enrichi:

```json
{
  "metadata": {
    "total_documents": 20,
    "categories": {
      "match_result": 12,
      "match_preview": 2,
      "tournament_news": 4,
      "statistics": 2
    }
  },
  "documents": [
    {
      "text": "Morocco Opens AFCON 2025 with Victory Over Comoros\n\nDate: 2025-12-21\n\nSource: CAF AFCON 2025\n\nMorocco kicked off...",
      "metadata": {
        "id": "demo_1_20260101133420",
        "category": "match_result",
        "teams": ["Morocco", "Comoros"],
        "score": "2-0"
      },
      "original_content": {...}
    }
  ]
}
```

### 3. Base Vectorielle (`chroma_db/`)

ChromaDB stocke:
- **Embeddings** : Vecteurs de 1536 dimensions (OpenAI)
- **Métadonnées** : Catégorie, source, date, équipes...
- **Textes** : Contenu enrichi pour le RAG

---

## 📁 Architecture du Projet

```
Chatbot_AFCON_Maroc/
├── src/
│   ├── app.py                 # 🌐 Interface Web Streamlit ⭐ NOUVEAU
│   │
│   ├── pipeline/              # ETL Pipeline
│   │   ├── config.py          # Configuration (sources, paths)
│   │   ├── scraper.py         # Web scraping
│   │   ├── demo_scraper.py    # Générateur de données démo
│   │   ├── transform.py       # Transformation RAG
│   │   └── pipeline.py        # Orchestration ETL
│   │
│   └── rag/                   # Système RAG
│       ├── config.py          # Configuration (Groq, ChromaDB)
│       ├── vectorizer.py      # Vectorisation + ChromaDB
│       └── chatbot.py         # Chatbot Q&A avec LangChain
│
├── examples/
│   ├── usage_examples.py      # Exemples ETL
│   └── rag_examples.py        # Exemples RAG
│
├── data/
│   ├── daily_fetch/           # Données brutes JSON
│   └── transformed/           # Données transformées
│       └── combined_dataset.json  # Dataset principal (20 docs)
│
├── chroma_db/                 # Base vectorielle ⭐ NOUVEAU
│
├── docs/
│   ├── EXPLICATION_RAG.md     # Théorie du RAG
│   └── INSTALLATION_RAG.md    # Guide d'installation
│
├── requirements.txt           # Dépendances (mis à jour)
├── .env.example              # Template configuration
└── README.md                 # Ce fichier
```

---

## ⚙️ Configuration

### Pipeline ETL
Modifiez `src/pipeline/config.py`:
- Ajouter de nouvelles sources
- Ajuster les sélecteurs CSS
- Configurer les chemins

### Système RAG
Modifiez `src/rag/config.py`:
- Clé API OpenAI (`OPENAI_API_KEY`)
- Modèles LLM et embeddings
- Paramètres RAG (top_k, température, max_tokens)
- Templates de prompts

---

## 💰 Coûts Estimés

### Vectorisation (une seule fois)
- 20 documents × ~200 tokens = **~$0.0001**

### Par Question
- Embedding : ~$0.0001
- LLM (GPT-3.5) : ~$0.002
- **Total : ~$0.002/question**

### 100 Questions
- **~$0.20 total**

---

## 🧪 Tests

### Pipeline ETL
```powershell
# Tester l'extraction
python -m src.pipeline.demo_scraper

# Tester la transformation
python -m src.pipeline.transform

# Voir les exemples
python examples\usage_examples.py
```

### Système RAG
```powershell
# Tester la vectorisation
python -m src.rag.vectorizer

# Tester le chatbot
python -m src.rag.chatbot

# Tests complets
python examples\rag_examples.py
```

---

## 📚 Documentation Complète

- **`README.md`** (ce fichier) - Vue d'ensemble et démarrage rapide
- **`EXPLICATION_RAG.md`** - Théorie du RAG, processus complet, exemples
- **`INSTALLATION_RAG.md`** - Guide détaillé d'installation et dépannage
- **`PROJET_COMPLETE.md`** - Résumé complet du projet

---

## 🚧 Roadmap

### ✅ Phase 1: Pipeline ETL (Terminé)
- [x] Web scraping avec retry
- [x] Générateur de données démo
- [x] Transformation pour RAG
- [x] Dataset combiné

### ✅ Phase 2: Système RAG (Terminé)
- [x] Vectorisation OpenAI
- [x] ChromaDB
- [x] Chatbot Q&A LangChain
- [x] Mode interactif
- [x] Documentation complète

### 🔄 Phase 3: API Backend (En cours)
- [ ] FastAPI application
- [ ] Endpoints REST (/chat, /health, /stats)
- [ ] CORS configuration
- [ ] Error handling
- [ ] API documentation (Swagger)

### 📋 Phase 4: Interface Utilisateur (À venir)
- [ ] Streamlit/Gradio UI
- [ ] Chat history display
- [ ] Source citations
- [ ] Export conversations
- [ ] Multi-language support

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

Ce projet est développé dans le cadre d'un PFE (Projet de Fin d'Études).

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
