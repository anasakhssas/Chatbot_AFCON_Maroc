# 📚 Enrichissement de la Base de Données ChromaDB

Ce dossier contient les fichiers pour enrichir votre base de données vectorielle avec de nouvelles informations.

## 🎯 Objectif

Ajouter des informations détaillées sur :
- La CAN 2025 (dates, stades, équipes, calendrier, billetterie)
- L'historique complet de la CAN (1957-2023)
- Profils détaillés des joueurs stars
- Records et statistiques

## 📁 Structure

```
data/enrichment/
├── can2025_informations_completes.json     # 12 documents sur la CAN 2025
├── can_historique_complet.json             # 12 documents historiques
├── joueurs_stars_can2025.json              # 12 profils de joueurs
└── README.md                                # Ce fichier
```

## 🚀 Utilisation

### Étape 1 : Fusionner les données

Fusionnez les nouveaux fichiers avec les données existantes :

```bash
python src/pipeline/enrich_database.py
```

**Ce script va :**
- ✅ Charger les données existantes de `data/transformed/combined_dataset.json`
- ✅ Charger tous les fichiers JSON du dossier `data/enrichment/`
- ✅ Supprimer les doublons (basé sur les IDs)
- ✅ Fusionner et sauvegarder dans `combined_dataset.json`
- ✅ Créer un backup automatique
- ✅ Afficher les statistiques par catégorie

### Étape 2 : Mettre à jour ChromaDB

Recréez la base vectorielle avec les nouvelles données :

```bash
python src/pipeline/update_vectorstore.py
```

**Ce script va :**
- ✅ Créer un backup de l'ancien vectorstore (si existant)
- ✅ Charger tous les documents du fichier combiné
- ✅ Vectoriser avec sentence-transformers (peut prendre 2-5 minutes)
- ✅ Créer le nouveau vectorstore ChromaDB
- ✅ Tester la recherche sémantique
- ✅ Afficher les statistiques finales

### Étape 3 : Tester le chatbot

Lancez l'application Streamlit et testez :

```bash
streamlit run src/app.py
```

**Questions à tester :**
- "Quand commence la CAN 2025 ?"
- "Quels sont les stades de la CAN ?"
- "Qui est Achraf Hakimi ?"
- "Combien de titres a l'Égypte ?"
- "Qui a gagné la CAN en 2023 ?"
- "Parle-moi de la victoire du Maroc en 1976"

## 📊 Contenu des Fichiers JSON

### 1. `can2025_informations_completes.json` (12 documents)

**Catégories :**
- `informations_generales` : Dates, format, 24 équipes
- `infrastructures` : 6 stades (Casablanca, Rabat, Marrakech, Agadir, Tanger, Oujda)
- `equipes_qualifiees` : Liste des 24 nations
- `phase_de_groupes` : Composition des 6 poules A-F
- `selection_maroc` : Hakimi, Ziyech, En-Nesyri, Regragui
- `pronostics` : Favoris (Maroc, Sénégal, Égypte, Cameroun, Algérie)
- `calendrier` : Dates des phases (21 déc - 18 jan)
- `records_statistiques` : Records à battre
- `arbitrage_technologie` : VAR, Goal-Line Technology
- `billetterie_pratique` : Prix (100-2000 MAD), réservation
- `economie_impact` : 8 milliards MAD, 2M visiteurs
- `diffusion_media` : Arryadia, BeIN Sports, 500M téléspectateurs

### 2. `can_historique_complet.json` (12 documents)

**Catégories :**
- `histoire_origines` : Création 1957, première édition
- `maroc_historique` : Victoire 1976, finale 2004
- `grandes_nations` : Égypte (7 titres), Cameroun (5), Sénégal (2021), Côte d'Ivoire (2023)
- `moments_historiques` : Zambie 2012 (émotion crash 1993)
- `records_historiques` : Samuel Eto'o (18 buts), Hossam Hassan (34 matchs)

### 3. `joueurs_stars_can2025.json` (12 documents)

**Profils détaillés :**

**Maroc :**
- Achraf Hakimi (PSG, latéral droit)
- Hakim Ziyech (Galatasaray, meneur de jeu)
- Youssef En-Nesyri (AS Roma, buteur)
- Sofyan Amrabat (Manchester United, milieu défensif)
- Yassine Bounou (Al-Hilal, gardien)
- Nayef Aguerd (West Ham, défenseur central)
- Azzedine Ounahi (Panathinaïkos, milieu)

**Autres stars :**
- Mohamed Salah (Égypte, Liverpool)
- Sadio Mané (Sénégal, Al-Nassr)
- Riyad Mahrez (Algérie, Al-Ahli)
- Victor Osimhen (Nigeria, Galatasaray)

**Entraîneur :**
- Walid Regragui (sélectionneur Maroc)

## 🔧 Format des Documents

Chaque document suit cette structure :

```json
{
  "id": "can2025_general_001",
  "text": "Texte complet du document (1-3 paragraphes)",
  "metadata": {
    "category": "informations_generales",
    "source": "can2025_official",
    "date": "2025-12-21",
    "keywords": ["CAN 2025", "Maroc", "dates"],
    "title": "Titre descriptif"
  }
}
```

## ➕ Ajouter Vos Propres Données

Vous pouvez créer vos propres fichiers JSON dans ce dossier :

### Exemple : `mes_infos_supplementaires.json`

```json
{
  "metadata": {
    "source": "enrichment_custom",
    "date": "2026-01-03",
    "description": "Mes informations personnalisées"
  },
  "documents": [
    {
      "id": "custom_001",
      "text": "Votre texte ici...",
      "metadata": {
        "category": "ma_categorie",
        "source": "ma_source",
        "date": "2026-01-03",
        "keywords": ["mot1", "mot2"],
        "title": "Mon titre"
      }
    }
  ]
}
```

**Règles importantes :**
- ✅ L'ID doit être **unique** (pas de doublon)
- ✅ Le texte doit être **riche et détaillé** (1-3 paragraphes minimum)
- ✅ Les mots-clés aident la recherche sémantique
- ✅ La catégorie permet le tri

## 📈 Statistiques Attendues

Après enrichissement, vous devriez avoir :

```
📊 AVANT (Wikipedia only) :
   • ~100-200 documents

📊 APRÈS (enrichissement) :
   • ~130-230 documents
   • 36 nouveaux documents détaillés
   • Couverture complète CAN 2025 + historique + joueurs
```

## 🐛 Dépannage

### "FileNotFoundError: combined_dataset.json"

**Solution :** Le fichier n'existe pas encore.
```bash
# Créez-le d'abord avec le scraper
python src/scrapers/real_scraper.py
python src/pipeline/data_transformer.py
```

### "Doublons détectés"

**Solution :** C'est normal ! Le script ignore automatiquement les doublons.
Les statistiques afficheront : "⚠️ X doublons ignorés"

### "Erreur de vectorisation"

**Solution :** Problème de modèle ou de mémoire.
```bash
# Vérifiez que sentence-transformers est installé
pip install sentence-transformers

# Si erreur de mémoire, fermez d'autres applications
```

### "Vectorstore déjà existant"

**Solution :** Le script demande confirmation avant de remplacer.
Tapez `o` pour confirmer. Un backup est automatiquement créé.

## 📝 Maintenance

### Mettre à jour régulièrement

Pour garder les données fraîches :

1. **Ajoutez de nouveaux fichiers JSON** dans `data/enrichment/`
2. **Relancez l'enrichissement :**
   ```bash
   python src/pipeline/enrich_database.py
   python src/pipeline/update_vectorstore.py
   ```

### Nettoyer les backups anciens

Les backups s'accumulent dans :
- `data/transformed/combined_dataset_backup_*.json`
- `chroma_db_backup_*/`

Supprimez les anciens après vérification.

## ✅ Checklist Post-Enrichissement

Après avoir enrichi la base :

- [ ] Le script `enrich_database.py` a réussi (✅)
- [ ] Le script `update_vectorstore.py` a réussi (✅)
- [ ] Le chatbot répond aux questions sur la CAN 2025
- [ ] Le chatbot connaît les joueurs (Hakimi, Ziyech, etc.)
- [ ] Le chatbot connaît l'historique (1976, 2004, etc.)
- [ ] Les sources affichées sont correctes
- [ ] Le temps de réponse est acceptable (<2s)

## 🆘 Besoin d'Aide ?

Si vous rencontrez des problèmes :

1. Vérifiez les logs détaillés dans la console
2. Consultez `README.md` à la racine du projet
3. Vérifiez que tous les packages sont installés : `pip install -r requirements.txt`

---

**💡 Astuce :** Plus vous ajoutez de documents riches et détaillés, meilleur sera le chatbot !

**🎯 Objectif :** Avoir la base de connaissances la plus complète sur la CAN 2025 au Maroc.
