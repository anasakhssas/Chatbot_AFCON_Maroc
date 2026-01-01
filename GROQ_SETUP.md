# 🚀 Configuration Groq - API Gratuite

## 🎉 Pourquoi Groq ?

### ✅ Avantages
- **100% GRATUIT** - Pas de carte bancaire requise
- **Ultra-rapide** - 10x plus rapide qu'OpenAI (500+ tokens/sec)
- **Modèles puissants** - LLaMA 3.1 70B, Mixtral 8x7B
- **Généreux** - 30 requêtes/minute gratuit
- **Pas de quota initial** - Commence immédiatement

### 💰 Comparaison des Coûts

| Provider | Coût/1M tokens | Limite gratuite |
|----------|----------------|-----------------|
| OpenAI   | $0.50 - $2.00  | $5 crédit (expire) |
| **Groq** | **GRATUIT**    | **30 req/min** |
| Anthropic| $3.00 - $15.00 | Aucune |

---

## 📝 Obtenir une Clé API Groq (2 minutes)

### Étape 1: Créer un Compte
1. Aller sur **https://console.groq.com/**
2. Cliquer sur "Sign Up"
3. Se connecter avec:
   - Google Account (recommandé)
   - GitHub
   - Email

### Étape 2: Créer une Clé API
1. Une fois connecté, aller dans **"API Keys"**
2. Cliquer sur **"Create API Key"**
3. Donner un nom: `CAN2025_Chatbot`
4. Copier la clé (commence par `gsk_...`)

**⚠️ IMPORTANT:** Sauvegardez la clé immédiatement, vous ne pourrez plus la voir!

### Étape 3: Configurer dans le Projet

```powershell
# Option 1: Variable d'environnement (session actuelle)
$env:GROQ_API_KEY = "gsk_votre_clé_ici"

# Option 2: Variable d'environnement (permanent)
[System.Environment]::SetEnvironmentVariable('GROQ_API_KEY', 'gsk_votre_clé_ici', 'User')

# Option 3: Fichier .env (recommandé)
# Créer un fichier .env à la racine:
```

Contenu du fichier `.env`:
```
GROQ_API_KEY=gsk_votre_clé_ici
```

---

## 🔧 Installation des Dépendances

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les packages Groq + Embeddings gratuits
pip install groq==0.4.1 langchain-groq==0.0.1 sentence-transformers==2.2.2 torch==2.1.0
```

**Ou installer tout depuis requirements.txt:**
```powershell
pip install -r requirements.txt
```

---

## ✅ Vérifier la Configuration

```powershell
# Test rapide de la clé API
python -c "import os; print('✅ Clé Groq configurée!' if os.getenv('GROQ_API_KEY') else '❌ Clé Groq manquante')"

# Test complet
python -m src.rag.chatbot
```

---

## 🤖 Modèles Groq Disponibles (GRATUITS)

### Recommandés pour le Chatbot CAN 2025

| Modèle | Taille | Vitesse | Qualité | Cas d'usage |
|--------|--------|---------|---------|-------------|
| **llama-3.1-70b-versatile** | 70B | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | **Recommandé** - Meilleur équilibre |
| llama-3.1-8b-instant | 8B | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Très rapide, bon pour tests |
| mixtral-8x7b-32768 | 47B | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Excellent pour français |
| gemma2-9b-it | 9B | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Alternatif rapide |

### Configuration dans `src/rag/config.py`

```python
# Défaut (recommandé)
LLM_MODEL = "llama-3.1-70b-versatile"

# Pour plus de vitesse
LLM_MODEL = "llama-3.1-8b-instant"

# Pour meilleur support français
LLM_MODEL = "mixtral-8x7b-32768"
```

---

## 🎯 Embeddings Gratuits (Local)

Le projet utilise **sentence-transformers** pour les embeddings:
- ✅ **100% gratuit**
- ✅ **Fonctionne en local** (pas d'API)
- ✅ **Support français** excellent
- ✅ **Pas de quota**

### Modèle Utilisé
```python
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
```

**Caractéristiques:**
- Support 50+ langues (dont français)
- Taille: 420 Mo (téléchargé une fois)
- Performance: Excellente pour RAG
- Alternative rapide: `all-MiniLM-L6-v2` (80 Mo, anglais uniquement)

---

## 📊 Limites Gratuites Groq

### Quotas par Minute (Gratuit)
- **Requêtes:** 30 par minute
- **Tokens:** ~14,000 par minute
- **Contexte:** Jusqu'à 32,768 tokens

### Pour notre Chatbot CAN 2025
- **Par question:** ~500 tokens (contexte + réponse)
- **Capacité:** ~28 questions/minute
- **Largement suffisant** pour usage normal!

### Si Limite Atteinte
```
Error: Rate limit exceeded
```
**Solution:** Attendre 60 secondes ou ajouter un délai entre questions

---

## 🚀 Utilisation

### 1. Vectoriser les Données
```powershell
python -m src.rag.vectorizer
```
**Temps estimé:** 2-3 minutes (téléchargement modèle + vectorisation)

### 2. Lancer le Chatbot
```powershell
python -m src.rag.chatbot
```

### 3. Mode Interactif
```
❓ Vous : Qui a marqué pour le Maroc ?
💬 Chatbot : Brahim Díaz a ouvert le score en 55ème minute...
```

---

## 🐛 Dépannage

### Erreur: "GROQ_API_KEY not found"
```powershell
# Vérifier si définie
echo $env:GROQ_API_KEY

# Redéfinir
$env:GROQ_API_KEY = "gsk_votre_clé"
```

### Erreur: "Rate limit exceeded"
**Cause:** Plus de 30 requêtes/minute

**Solution:**
```python
import time
# Ajouter un délai entre questions
time.sleep(2)  # 2 secondes entre chaque question
```

### Erreur: "Module 'groq' not found"
```powershell
pip install groq langchain-groq
```

### Modèle d'embeddings lent au premier lancement
**Normal!** Le modèle (420 Mo) se télécharge la première fois.
- Dossier: `C:\Users\VOTREUSER\.cache\huggingface\`
- Durée: 2-5 minutes selon connexion
- Ensuite: Instantané

---

## 💡 Conseils d'Optimisation

### 1. Réduire le Contexte
```python
# Dans config.py
TOP_K_RESULTS = 2  # Au lieu de 3 (moins de tokens)
MAX_TOKENS = 300   # Au lieu de 500 (réponses plus courtes)
```

### 2. Batch Processing
```python
# Traiter plusieurs questions d'un coup
questions = ["Q1", "Q2", "Q3"]
responses = chatbot.batch_ask(questions)
```

### 3. Cache les Embeddings
Les embeddings sont automatiquement cachés par ChromaDB, pas besoin de recalculer!

---

## 📚 Ressources

- **Groq Console:** https://console.groq.com/
- **Groq Documentation:** https://console.groq.com/docs
- **Modèles disponibles:** https://console.groq.com/docs/models
- **Status Groq:** https://status.groq.com/
- **Discord Groq:** https://groq.com/discord

---

## 🎉 Résumé

### Ce qui est GRATUIT
✅ **Clé API Groq** - Pas de carte bancaire  
✅ **30 requêtes/minute** - Largement suffisant  
✅ **Embeddings locaux** - Sentence Transformers  
✅ **ChromaDB** - Base vectorielle open-source  
✅ **Tous les modèles LLaMA/Mixtral** - Groq  

### Ce qui est PAYANT
❌ Rien pour notre usage! 🎊

---

**Prêt à commencer?**

```powershell
# 1. Obtenir clé: https://console.groq.com/keys
# 2. Configurer
$env:GROQ_API_KEY = "gsk_..."

# 3. Installer
pip install -r requirements.txt

# 4. Vectoriser
python -m src.rag.vectorizer

# 5. Chatbot!
python -m src.rag.chatbot
```

**🚀 Profitez de votre chatbot CAN 2025 GRATUIT!**
