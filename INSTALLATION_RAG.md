# Guide d'Installation et d'Utilisation - RAG CAN 2025

## 🚀 Installation Rapide

### 1. Installer les Dépendances

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les nouvelles dépendances RAG
pip install chromadb==0.4.22 langchain==0.1.0 langchain-openai==0.0.5 langchain-community==0.0.13 tiktoken==0.5.2 openai==1.10.0
```

### 2. Configurer la Clé API OpenAI

```powershell
# Option 1: Variable d'environnement (session actuelle)
$env:OPENAI_API_KEY = "votre_clé_api_openai"

# Option 2: Variable d'environnement (permanent)
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'votre_clé_api_openai', 'User')

# Option 3: Fichier .env (créer à la racine du projet)
# Contenu du fichier .env:
# OPENAI_API_KEY=votre_clé_api_openai
```

**Obtenir une clé API OpenAI:**
1. Créer un compte sur https://platform.openai.com/
2. Aller dans "API Keys" → "Create new secret key"
3. Copier la clé et la définir dans votre environnement

---

## 📖 Utilisation

### Étape 1: Vectorisation des Données

```powershell
# Créer le vectorstore ChromaDB
python -m src.rag.vectorizer
```

**Ce script va:**
- ✅ Charger les 20 documents depuis `combined_dataset.json`
- ✅ Créer les embeddings avec OpenAI
- ✅ Stocker dans ChromaDB (`chroma_db/`)
- ✅ Afficher les statistiques

**Résultat attendu:**
```
✅ VECTORISATION TERMINÉE AVEC SUCCÈS!
📁 Vectorstore sauvegardé dans : chroma_db
📊 20 documents indexés
```

---

### Étape 2: Tester le Chatbot

```powershell
# Lancer le chatbot avec tests automatiques
python -m src.rag.chatbot
```

**Ce script va:**
- ✅ Charger le vectorstore existant
- ✅ Tester 5 questions prédéfinies
- ✅ Afficher réponses + sources
- ✅ Proposer le mode interactif

---

### Étape 3: Exemples Complets

```powershell
# Menu interactif avec 8 exemples
python examples\rag_examples.py
```

**Exemples disponibles:**
1. **Vectorisation** - Créer ChromaDB
2. **Recherche sémantique** - Tests de similarité
3. **Q&A simples** - Question unique
4. **Batch** - Plusieurs questions
5. **Détaillé** - Réponse avec sources
6. **Comparaison** - Différentes formulations
7. **Statistiques** - Infos du système
8. **Interactif** - Chat en direct

---

## 💬 Mode Interactif

```powershell
# Lancer directement en mode chat
python -m src.rag.chatbot
```

**Commandes disponibles:**
- Poser n'importe quelle question sur la CAN 2025
- `history` - Voir l'historique des conversations
- `quit` ou `exit` - Quitter

**Exemple de session:**
```
❓ Vous : Qui a marqué pour le Maroc ?
💬 Chatbot : Brahim Díaz a ouvert le score en 55ème minute...
📚 Sources : 2 documents

❓ Vous : Quel est le meilleur buteur ?
💬 Chatbot : Riyad Mahrez mène la course au soulier d'or...
```

---

## 🧪 Tests et Validation

### Test 1: Vérifier la Vectorisation
```powershell
python -c "from src.rag.vectorizer import VectorizerCAN2025; v = VectorizerCAN2025(); v.load_vectorstore(); print(v.get_stats())"
```

### Test 2: Question Rapide
```powershell
python -c "from src.rag.chatbot import ChatbotCAN2025; c = ChatbotCAN2025(); print(c.ask('Qui a gagné ?')['answer'])"
```

### Test 3: Recherche Sémantique
```powershell
python -c "from src.rag.vectorizer import VectorizerCAN2025; v = VectorizerCAN2025(); v.load_vectorstore(); v.test_search('Maroc victoire', k=2)"
```

---

## 📊 Structure des Fichiers

```
Chatbot_AFCON_Maroc/
├── src/
│   ├── rag/
│   │   ├── __init__.py          # Package RAG
│   │   ├── config.py            # Configuration (API keys, modèles)
│   │   ├── vectorizer.py        # Vectorisation + ChromaDB
│   │   └── chatbot.py           # Chatbot RAG avec LangChain
│   └── pipeline/                 # Pipeline d'extraction (déjà fait)
├── examples/
│   ├── usage_examples.py        # Exemples ETL
│   └── rag_examples.py          # Exemples RAG (NOUVEAU)
├── data/
│   ├── daily_fetch/             # Données brutes
│   └── transformed/             # Données transformées
│       └── combined_dataset.json # 20 documents pour RAG
├── chroma_db/                    # Base vectorielle (créé automatiquement)
└── requirements.txt              # Dépendances (mis à jour)
```

---

## 🔧 Dépannage

### Erreur: "OPENAI_API_KEY not found"
```powershell
# Vérifier si la clé est définie
echo $env:OPENAI_API_KEY

# La redéfinir si nécessaire
$env:OPENAI_API_KEY = "sk-..."
```

### Erreur: "Module not found"
```powershell
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur: "Vectorstore not found"
```powershell
# Créer le vectorstore
python -m src.rag.vectorizer
```

### ChromaDB déjà existant
```powershell
# Supprimer pour recréer
Remove-Item -Recurse -Force chroma_db
python -m src.rag.vectorizer
```

---

## 💰 Coûts Estimés

### Vectorisation (une seule fois)
- 20 documents × 200 tokens = 4000 tokens
- Coût : ~$0.0001 (négligeable)

### Par Question
- Embedding question : ~$0.0001
- LLM (GPT-3.5) : ~$0.002
- **Total : ~$0.002 par question**

### 100 Questions
- Coût total : ~$0.20

**Recommandations:**
- ✅ `text-embedding-3-small` (embeddings économiques)
- ✅ `gpt-3.5-turbo` (pour démarrer)
- ⚠️ `gpt-4` (plus cher, meilleure qualité)

---

## 🎯 Prochaines Étapes

### Phase Actuelle: ✅ RAG Fonctionnel
- [x] Vectorisation
- [x] ChromaDB
- [x] Chatbot Q&A
- [x] Mode interactif

### Phase Suivante: API Backend
```
À FAIRE:
- [ ] FastAPI application
- [ ] Endpoints REST (/chat, /health, /stats)
- [ ] CORS configuration
- [ ] Error handling
```

### Phase Finale: Interface Utilisateur
```
À FAIRE:
- [ ] Streamlit/Gradio UI
- [ ] Chat history display
- [ ] Source citations
- [ ] Multi-language support
```

---

## 📚 Ressources

- **LangChain Docs:** https://python.langchain.com/docs/
- **ChromaDB Docs:** https://docs.trychroma.com/
- **OpenAI API:** https://platform.openai.com/docs/
- **RAG Tutorial:** https://python.langchain.com/docs/use_cases/question_answering/

---

## 🆘 Support

Pour toute question ou problème:
1. Vérifier ce guide d'installation
2. Consulter `EXPLICATION_RAG.md` pour la théorie
3. Lancer `python examples\rag_examples.py` pour voir les démos

**Bon chatbot! 🚀⚽**
