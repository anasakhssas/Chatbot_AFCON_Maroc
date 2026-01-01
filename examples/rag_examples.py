"""
Exemples d'utilisation du système RAG pour le Chatbot CAN 2025
Démonstrations de vectorisation et de questions-réponses
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.config import RAGConfig
from src.rag.vectorizer import VectorizerCAN2025
from src.rag.chatbot import ChatbotCAN2025


def example_1_vectorization():
    """Exemple 1: Vectoriser les données et créer ChromaDB"""
    print("\n" + "="*70)
    print("📋 EXEMPLE 1 : VECTORISATION DES DONNÉES")
    print("="*70 + "\n")
    
    # Créer le vectorizer
    vectorizer = VectorizerCAN2025()
    
    # Créer le vectorstore
    print("🔄 Création du vectorstore...")
    vectorstore = vectorizer.create_vectorstore()
    
    # Afficher les stats
    stats = vectorizer.get_stats()
    print(f"\n✅ Vectorisation terminée!")
    print(f"📊 {stats['total_documents']} documents indexés")
    
    input("\nAppuyez sur Entrée pour continuer...\n")


def example_2_search():
    """Exemple 2: Recherche sémantique dans le vectorstore"""
    print("\n" + "="*70)
    print("📋 EXEMPLE 2 : RECHERCHE SÉMANTIQUE")
    print("="*70 + "\n")
    
    # Charger le vectorizer
    vectorizer = VectorizerCAN2025()
    vectorizer.load_vectorstore()
    
    # Questions de test
    queries = [
        "Maroc victoire",
        "Meilleur buteur tournoi",
        "Résultats matchs groupe"
    ]
    
    for query in queries:
        print(f"\n🔍 Recherche : '{query}'")
        print("-" * 70)
        results = vectorizer.test_search(query, k=2)
        print()
    
    input("\nAppuyez sur Entrée pour continuer...\n")


def example_3_simple_qa():
    """Exemple 3: Questions-réponses simples"""
    print("\n" + "="*70)
    print("📋 EXEMPLE 3 : QUESTIONS-RÉPONSES SIMPLES")
    print("="*70 + "\n")
    
    # Créer le chatbot
    chatbot = ChatbotCAN2025(load_existing=True)
    
    # Question simple
    question = "Qui a marqué pour le Maroc ?"
    print(f"❓ Question : {question}\n")
    
    response = chatbot.ask(question, verbose=False)
    
    print(f"💬 Réponse : {response['answer']}")
    print(f"\n📚 Basé sur {response['num_sources']} sources")
    
    input("\nAppuyez sur Entrée pour continuer...\n")


def example_4_batch_questions():
    """Exemple 4: Traitement en batch de plusieurs questions"""
    print("\n" + "="*70)
    print("📋 EXEMPLE 4 : QUESTIONS EN BATCH")
    print("="*70 + "\n")
    
    # Créer le chatbot
    chatbot = ChatbotCAN2025(load_existing=True)
    
    # Liste de questions
    questions = [
        "Quel est le score du match Maroc contre Comores ?",
        "Qui a gagné entre l'Égypte et le Zimbabwe ?",
        "Combien de buts a marqué le Nigeria ?",
        "Quelle équipe est en tête du groupe ?"
    ]
    
    print(f"📊 Traitement de {len(questions)} questions...\n")
    
    # Traiter en batch
    responses = chatbot.batch_ask(questions, verbose=False)
    
    # Afficher les résultats
    for i, resp in enumerate(responses, 1):
        print(f"\n{i}. Q: {resp['question']}")
        print(f"   R: {resp['answer']}")
        print(f"   📚 Sources: {resp['num_sources']}")
    
    input("\nAppuyez sur Entrée pour continuer...\n")


def example_5_detailed_response():
    """Exemple 5: Réponse détaillée avec sources"""
    print("\n" + "="*70)
    print("📋 EXEMPLE 5 : RÉPONSE DÉTAILLÉE AVEC SOURCES")
    print("="*70 + "\n")
    
    # Créer le chatbot
    chatbot = ChatbotCAN2025(load_existing=True)
    
    # Question complexe
    question = "Quels sont les résultats des matchs du premier tour de la CAN 2025 ?"
    
    # Obtenir une réponse détaillée
    response = chatbot.ask(question, verbose=True)
    
    input("\nAppuyez sur Entrée pour continuer...\n")


def example_6_compare_questions():
    """Exemple 6: Comparer différentes formulations"""
    print("\n" + "="*70)
    print("📋 EXEMPLE 6 : COMPARAISON DE FORMULATIONS")
    print("="*70 + "\n")
    
    # Créer le chatbot
    chatbot = ChatbotCAN2025(load_existing=True)
    
    # Même question, différentes formulations
    questions = [
        "Qui a marqué pour le Maroc ?",
        "Quels sont les buteurs marocains ?",
        "Liste des joueurs qui ont inscrit des buts pour l'équipe du Maroc"
    ]
    
    print("🔄 Test de compréhension sémantique avec 3 formulations similaires:\n")
    
    for i, q in enumerate(questions, 1):
        print(f"\n{'─'*70}")
        print(f"Version {i}: {q}")
        print('─'*70)
        
        response = chatbot.ask(q, verbose=False)
        print(f"💬 {response['answer']}\n")
    
    print("\n💡 Observation: Le système RAG comprend le sens, pas juste les mots!")
    
    input("\nAppuyez sur Entrée pour continuer...\n")


def example_7_statistics():
    """Exemple 7: Statistiques du système"""
    print("\n" + "="*70)
    print("📋 EXEMPLE 7 : STATISTIQUES DU SYSTÈME")
    print("="*70 + "\n")
    
    # Créer le chatbot
    chatbot = ChatbotCAN2025(load_existing=True)
    
    # Poser quelques questions
    questions = [
        "Qui a gagné la CAN 2025 ?",
        "Quel est le meilleur buteur ?",
        "Combien d'équipes ont participé ?"
    ]
    
    print("🔄 Génération de quelques conversations...\n")
    for q in questions:
        chatbot.ask(q, verbose=False)
        print(f"✓ {q}")
    
    # Afficher les stats
    print("\n📊 STATISTIQUES COMPLÈTES")
    print("="*70)
    
    stats = chatbot.get_stats()
    
    print(f"\n🤖 Configuration LLM:")
    print(f"   Modèle       : {stats['llm_model']}")
    print(f"   Embeddings   : {stats['embedding_model']}")
    print(f"   Température  : {stats['configuration']['temperature']}")
    print(f"   Max tokens   : {stats['configuration']['max_tokens']}")
    print(f"   Top K        : {stats['configuration']['top_k']}")
    
    print(f"\n💾 Vectorstore:")
    print(f"   Documents    : {stats['vectorstore']['total_documents']}")
    print(f"   Collection   : {stats['vectorstore']['collection_name']}")
    
    print(f"\n💬 Conversations:")
    print(f"   Total        : {stats['conversations']}")
    
    print(f"\n📂 Catégories:")
    for cat, count in stats['vectorstore']['categories'].items():
        print(f"   {cat:<20} : {count} documents")
    
    print("\n" + "="*70)
    
    input("\nAppuyez sur Entrée pour continuer...\n")


def example_8_interactive():
    """Exemple 8: Mode interactif"""
    print("\n" + "="*70)
    print("📋 EXEMPLE 8 : MODE INTERACTIF")
    print("="*70 + "\n")
    
    # Créer le chatbot
    chatbot = ChatbotCAN2025(load_existing=True)
    
    print("🎮 Lancement du mode chat interactif...")
    print("💡 Astuce: Tapez 'history' pour voir l'historique\n")
    
    # Lancer le mode chat
    chatbot.chat()


def main():
    """Menu principal des exemples"""
    
    # Vérifier la configuration
    print("\n🔧 VÉRIFICATION DE LA CONFIGURATION")
    print("="*70)
    
    errors = RAGConfig.validate()
    if errors:
        print("\n❌ ERREURS DE CONFIGURATION:")
        for error in errors:
            print(f"   {error}")
        print("\n💡 Solution:")
        print("   1. Définissez OPENAI_API_KEY dans vos variables d'environnement")
        print("   2. Ou créez un fichier .env avec : OPENAI_API_KEY=votre_clé")
        print("\n   Windows PowerShell:")
        print("   $env:OPENAI_API_KEY='votre_clé'\n")
        return
    
    print("✅ Configuration valide!\n")
    
    # Menu des exemples
    examples = [
        ("Vectorisation des données", example_1_vectorization),
        ("Recherche sémantique", example_2_search),
        ("Questions-réponses simples", example_3_simple_qa),
        ("Questions en batch", example_4_batch_questions),
        ("Réponse détaillée avec sources", example_5_detailed_response),
        ("Comparaison de formulations", example_6_compare_questions),
        ("Statistiques du système", example_7_statistics),
        ("Mode interactif", example_8_interactive)
    ]
    
    while True:
        print("\n" + "="*70)
        print("🎯 EXEMPLES RAG - CHATBOT CAN 2025")
        print("="*70)
        
        for i, (title, _) in enumerate(examples, 1):
            print(f"{i}. {title}")
        print("0. Quitter")
        print("="*70)
        
        choice = input("\n➤ Choisissez un exemple (0-8) : ").strip()
        
        if choice == '0':
            print("\n👋 Au revoir!\n")
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                title, func = examples[idx]
                func()
            else:
                print("\n❌ Choix invalide!")
        except ValueError:
            print("\n❌ Veuillez entrer un nombre!")
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!\n")
            break
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
