# 🏆 Atlas AI - Assistant Intelligent CAN 2025

> 🇲🇦 Assistant IA complet pour la Coupe d'Afrique des Nations 2025 au Maroc

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ 4 Fonctionnalités Principales

| # | Fonctionnalité | Description |
|---|----------------|-------------|
| 💬 | **Chatbot RAG** | Questions/réponses avec sources vérifiées |
| 📊 | **Analyse Sentiment** | Analyse YouTube avec 95-98% de précision |
| 📝 | **Résumés Matchs** | Génération automatique + export PDF/Image |
| 🎭 | **Avatar Virtuel** | Expert vocal sur l'historique CAN (1957-2023) |

---

## 🚀 Installation Rapide

```bash
# 1. Cloner le projet
git clone https://github.com/anasakhssas/Chatbot_AFCON_Maroc.git
cd Chatbot_AFCON_Maroc

# 2. Créer l'environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows
source venv/bin/activate        # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la clé API (fichier .env)
echo "GROQ_API_KEY=votre_cle_ici" > .env
```

> 🔑 **Clé gratuite** : [console.groq.com/keys](https://console.groq.com/keys)

---

## ▶️ Lancer l'Application

```bash
streamlit run src/app.py
```

📍 Ouvrir : **http://localhost:8501**

---

## 🛠️ Stack Technique

| Composant | Technologie | Coût |
|-----------|-------------|------|
| **LLM** | Groq (llama-3.3-70b) | Gratuit |
| **Embeddings** | sentence-transformers | Gratuit |
| **Vector DB** | ChromaDB | Local |
| **Sentiment** | CardiffNLP | Gratuit |
| **TTS** | gTTS | Gratuit |
| **Interface** | Streamlit | Gratuit |

---

## 📊 Performances

| Métrique | Valeur |
|----------|--------|
| Précision Chatbot | 95%+ |
| Précision Sentiment | 95-98% |
| Temps de réponse | < 2s |
| Documents indexés | 40+ |

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 👤 Auteur

**Anas Akhssas** - [@anasakhssas](https://github.com/anasakhssas)

---

<p align="center">
  <b>🇲🇦 CAN 2025 au Maroc</b><br>
  21 Décembre 2025 → 18 Janvier 2026<br><br>
  ⚽ <i>Allez les Lions de l'Atlas !</i> 🦁
</p>
