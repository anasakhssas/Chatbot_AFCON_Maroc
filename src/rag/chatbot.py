"""
Module Chatbot RAG pour la CAN 2025
Utilise ChromaDB et LangChain pour répondre aux questions
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from .config import RAGConfig
from .vectorizer import VectorizerCAN2025

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ChatbotCAN2025:
    """Chatbot RAG pour répondre aux questions sur la CAN 2025"""
    
    def __init__(self, config: RAGConfig = None, load_existing: bool = True):
        """
        Initialiser le chatbot
        
        Args:
            config: Configuration RAG
            load_existing: Si True, charge un vectorstore existant, sinon en crée un nouveau
        """
        self.config = config or RAGConfig
        self.vectorizer = VectorizerCAN2025(config=self.config)
        self.llm = None
        self.qa_chain = None
        self.conversation_history = []
        
        # Charger ou créer le vectorstore
        if load_existing and self.config.CHROMA_DB_DIR.exists():
            logger.info("📂 Chargement du vectorstore existant...")
            self.vectorizer.load_vectorstore()
        else:
            logger.info("🔄 Création d'un nouveau vectorstore...")
            self.vectorizer.create_vectorstore()
        
        # Initialiser le LLM et la chaîne QA
        self._initialize_llm()
        self._initialize_qa_chain()
        
        logger.info("✅ ChatbotCAN2025 initialisé et prêt")
    
    def _initialize_llm(self):
        """Initialiser le modèle de langage Groq (gratuit et ultra-rapide!)"""
        logger.info(f"🤖 Initialisation du LLM Groq : {self.config.LLM_MODEL}")
        
        self.llm = ChatGroq(
            model=self.config.LLM_MODEL,
            temperature=self.config.LLM_TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS,
            groq_api_key=self.config.GROQ_API_KEY
        )
        
        logger.info("✅ LLM Groq initialisé (GRATUIT!)")
    
    def _initialize_qa_chain(self):
        """Initialiser la chaîne de question-réponse"""
        logger.info("🔗 Initialisation de la chaîne RAG...")
        
        # Créer le retriever avec les paramètres de recherche
        self.retriever = self.vectorizer.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.config.TOP_K_RESULTS}
        )
        
        # Créer le template de prompt
        prompt = ChatPromptTemplate.from_template(self.config.QUERY_PROMPT)
        
        # Créer la chaîne RAG moderne
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.qa_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        logger.info("✅ Chaîne RAG initialisée")
    
    def ask(self, question: str, verbose: bool = False) -> Dict[str, Any]:
        """
        Poser une question au chatbot
        
        Args:
            question: La question en langage naturel
            verbose: Si True, affiche les détails du processus
        
        Returns:
            Dictionnaire avec la réponse, sources et métadonnées
        """
        logger.info(f"❓ Question : {question}")
        
        try:
            # Récupérer les documents pertinents
            source_documents = self.retriever.invoke(question)
            
            # Exécuter la chaîne RAG
            answer = self.qa_chain.invoke(question)
            
            # Formater la réponse
            response = {
                'question': question,
                'answer': answer,
                'sources': [],
                'timestamp': datetime.now().isoformat(),
                'model': self.config.LLM_MODEL,
                'num_sources': len(source_documents)
            }
            
            # Ajouter les sources
            for i, doc in enumerate(source_documents, 1):
                source = {
                    'rank': i,
                    'category': doc.metadata.get('category', 'N/A'),
                    'source': doc.metadata.get('source', 'N/A'),
                    'date': doc.metadata.get('date', 'N/A'),
                    'title': doc.metadata.get('title', 'N/A'),
                    'excerpt': doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                }
                response['sources'].append(source)
            
            # Ajouter à l'historique
            self.conversation_history.append(response)
            
            # Affichage verbose
            if verbose:
                self._print_response(response)
            
            logger.info(f"✅ Réponse générée avec {len(source_documents)} sources")
            return response
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la génération de la réponse : {e}")
            raise
    def _print_response(self, response: Dict[str, Any]):
        """Afficher une réponse formatée"""
        print("\n" + "="*70)
        print(f"❓ QUESTION")
        print("="*70)
        print(f"{response['question']}\n")
        
        print("="*70)
        print(f"💬 RÉPONSE")
        print("="*70)
        print(f"{response['answer']}\n")
        
        print("="*70)
        print(f"📚 SOURCES ({response['num_sources']} documents)")
        print("="*70)
        for source in response['sources']:
            print(f"\n{source['rank']}. [{source['category']}] {source['title']}")
            print(f"   📅 {source['date']} | 🌐 {source['source']}")
            print(f"   📄 {source['excerpt']}")
        
        print("\n" + "="*70 + "\n")
    
    def chat(self):
        """Mode interactif de chat"""
        print("\n" + "="*70)
        print("🤖 CHATBOT CAN 2025 - MODE INTERACTIF")
        print("="*70)
        print("Posez vos questions sur la CAN 2025!")
        print("Commandes : 'quit' ou 'exit' pour quitter, 'history' pour l'historique")
        print("="*70 + "\n")
        
        while True:
            try:
                # Demander une question
                question = input("❓ Vous : ").strip()
                
                # Commandes spéciales
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Au revoir!\n")
                    break
                
                if question.lower() == 'history':
                    self._print_history()
                    continue
                
                if not question:
                    continue
                
                # Générer la réponse
                response = self.ask(question, verbose=True)
                
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir!\n")
                break
            except Exception as e:
                print(f"\n❌ Erreur : {e}\n")
    
    def _print_history(self):
        """Afficher l'historique des conversations"""
        if not self.conversation_history:
            print("\n📭 Aucune conversation dans l'historique\n")
            return
        
        print("\n" + "="*70)
        print(f"📜 HISTORIQUE ({len(self.conversation_history)} questions)")
        print("="*70)
        
        for i, conv in enumerate(self.conversation_history, 1):
            print(f"\n{i}. Q: {conv['question']}")
            print(f"   R: {conv['answer'][:100]}...")
            print(f"   🕐 {conv['timestamp']} | 📚 {conv['num_sources']} sources")
        
        print("\n" + "="*70 + "\n")
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtenir les statistiques du chatbot"""
        vectorstore_stats = self.vectorizer.get_stats()
        
        stats = {
            'vectorstore': vectorstore_stats,
            'llm_model': self.config.LLM_MODEL,
            'embedding_model': self.config.EMBEDDING_MODEL,
            'conversations': len(self.conversation_history),
            'configuration': {
                'temperature': self.config.LLM_TEMPERATURE,
                'max_tokens': self.config.MAX_TOKENS,
                'top_k': self.config.TOP_K_RESULTS
            }
        }
        
        return stats
    
    def batch_ask(self, questions: List[str], verbose: bool = False) -> List[Dict[str, Any]]:
        """
        Poser plusieurs questions en batch
        
        Args:
            questions: Liste de questions
            verbose: Si True, affiche chaque réponse
        
        Returns:
            Liste des réponses
        """
        logger.info(f"📊 Traitement de {len(questions)} questions en batch...")
        
        responses = []
        for i, question in enumerate(questions, 1):
            logger.info(f"Question {i}/{len(questions)}")
            response = self.ask(question, verbose=verbose)
            responses.append(response)
        
        logger.info(f"✅ Batch terminé : {len(responses)} réponses générées")
        return responses


def main():
    """Fonction principale pour tester le chatbot"""
    print("\n🚀 CHATBOT CAN 2025 - DÉMARRAGE\n")
    
    # Afficher la configuration
    RAGConfig.print_config()
    
    # Créer le chatbot
    print("🔄 Initialisation du chatbot...")
    chatbot = ChatbotCAN2025(load_existing=True)
    
    # Questions de test
    test_questions = [
        "Qui a marqué pour le Maroc contre les Comores ?",
        "Quel est le score du match Égypte contre Zimbabwe ?",
        "Quelles équipes ont participé à la CAN 2025 ?",
        "Qui est le meilleur buteur du tournoi ?",
        "Quand le Maroc joue-t-il son prochain match ?"
    ]
    
    print("\n" + "="*70)
    print("🧪 TESTS AUTOMATIQUES")
    print("="*70)
    
    # Tester avec plusieurs questions
    for question in test_questions:
        print(f"\n{'─'*70}")
        response = chatbot.ask(question, verbose=True)
        input("Appuyez sur Entrée pour continuer...")
    
    # Afficher les statistiques
    print("\n📊 STATISTIQUES DU CHATBOT")
    print("="*70)
    stats = chatbot.get_stats()
    print(f"Total conversations : {stats['conversations']}")
    print(f"Documents indexés   : {stats['vectorstore']['total_documents']}")
    print(f"Modèle LLM         : {stats['llm_model']}")
    print("="*70)
    
    # Proposer le mode interactif
    print("\n💬 Voulez-vous passer en mode interactif ? (o/n)")
    choice = input("➤ ").strip().lower()
    
    if choice in ['o', 'oui', 'y', 'yes']:
        chatbot.chat()
    else:
        print("\n✅ Tests terminés!\n")


if __name__ == "__main__":
    main()
