
1

Automatic Zoom
Cahier des Charges Complet – Assistant Intelligent CAN 2025 (Version PFE) 
 
Introduction 
Dans le cadre de ce Projet de Fin d’Études (PFE), ce travail vise à concevoir et développer un 
assistant intelligent dédié à la Coupe d’Afrique des Nations (CAN) 2025. L’objectif est 
d’exploiter l’intelligence artificielle générative et les systèmes RAG afin d’améliorer 
l’expérience des fans de football via une plateforme interactive et intelligente. 
 
1. Contexte et Problématique 
La CAN génère un volume massif d’informations (matchs, résultats, réactions des 
supporters). Les utilisateurs rencontrent des difficultés à accéder rapidement à des 
informations fiables et synthétiques. L’intégration d’un assistant intelligent basé sur des 
données officielles permet de répondre à ce besoin. 
 
2. Objectifs du Projet 
- Concevoir un pipeline automatisé de collecte et traitement des données 
- Implémenter une base vectorielle pour la recherche sémantique 
- Développer un chatbot RAG fiable et précis 
- Enrichir l’expérience utilisateur par des fonctionnalités avancées 
- Mettre en place une architecture modulaire et scalable 
 
3. Cas d’Usage 
- Consultation des résultats et calendriers 
- Questions-réponses sur les équipes et matchs 
- Résumés automatiques des matchs 
- Analyse de sentiment des supporters 
- Recommandations personnalisées 
 
4. Description Fonctionnelle 
 
4.1 Pipeline de Données (ETL) 
- Sources : sites officiels CAF, plateformes sportives 
- Extraction automatisée (web scraping / API) 
- Nettoyage et normalisation des données 
- Structuration en documents textuels 
- Vectorisation et stockage dans ChromaDB 
- Orchestration et planification des tâches 
 
4.2 Système RAG 
- Encodage des requêtes utilisateurs 
- Recherche sémantique 
- Injection du contexte dans le prompt 
- Génération de réponses contrôlées 
 
4.3 Fonctionnalités Avancées 
- Résumé automatique de matchs 
- Analyse de sentiment (NLP) 
- Recommandation de contenus 
 
5. Architecture Technique 
- Backend : FastAPI 
- Pipeline IA : LangChain / LlamaIndex 
- Base vectorielle : ChromaDB 
- Modèles LLM : OpenRouter / Ollama 
