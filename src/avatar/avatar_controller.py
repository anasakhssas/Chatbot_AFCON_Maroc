"""
Module Avatar Virtuel pour l'Historique de la CAN
Utilise gTTS (gratuit) + animation simple
"""

from gtts import gTTS
import os
import hashlib
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HistoriqueCANLoader:
    """Charge et recherche dans l'historique de la CAN"""
    
    def __init__(self, historique_path: str = "data/historique.md"):
        self.historique_path = historique_path
        self.content = ""
        self.load_historique()
    
    def load_historique(self):
        """Charge le fichier historique"""
        try:
            with open(self.historique_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            logger.info(f"✅ Historique chargé: {len(self.content)} caractères")
        except Exception as e:
            logger.error(f"❌ Erreur chargement historique: {e}")
            self.content = "Historique non disponible."
    
    def search_info(self, query: str) -> str:
        """
        Recherche des informations dans l'historique
        
        Args:
            query: Question de l'utilisateur
            
        Returns:
            Extrait pertinent de l'historique
        """
        query_lower = query.lower()
        
        # Mots-clés pour différentes sections
        if any(word in query_lower for word in ['maroc', 'lions', '1976', 'marocain']):
            return self._extract_section("Histoire du Maroc à la CAN")
        
        elif any(word in query_lower for word in ['égypte', 'pharaons', 'record', 'plus de titres']):
            return self._extract_section("Classement par Nombre de Titres")
        
        elif any(word in query_lower for word in ['cameroun', 'indomptables']):
            return self._extract_section("Cameroun")
        
        elif any(word in query_lower for word in ['ghana', 'black stars']):
            return self._extract_section("Ghana")
        
        elif any(word in query_lower for word in ['buteur', 'eto', "eto'o", 'meilleur']):
            return self._extract_section("Meilleurs Buteurs de l'Histoire")
        
        elif any(word in query_lower for word in ['2025', 'prochaine', 'marrakech', 'casablanca']):
            return self._extract_section("CAN 2025 - Maroc")
        
        elif any(word in query_lower for word in ['première', 'origine', 'création', '1957']):
            return self._extract_section("Origines et Création")
        
        elif any(word in query_lower for word in ['palmarès', 'vainqueurs', 'champions']):
            return self._extract_section("Palmarès Complet")
        
        elif any(word in query_lower for word in ['sénégal', 'lions de la teranga', '2021']):
            return self._extract_section("Sénégal 2021")
        
        elif any(word in query_lower for word in ['zambie', '2012', 'lusaka']):
            return self._extract_section("Zambie 2012")
        
        elif any(word in query_lower for word in ['côte', 'ivoire', 'éléphants', '2023']):
            return self._extract_section("Côte d'Ivoire")
        
        else:
            # Retourner une section générale
            return self._extract_section("Classement par Nombre de Titres")
    
    def _extract_section(self, section_name: str) -> str:
        """Extrait une section spécifique du document"""
        lines = self.content.split('\n')
        
        # Trouver la section
        start_idx = -1
        for i, line in enumerate(lines):
            if section_name.lower() in line.lower():
                start_idx = i
                break
        
        if start_idx == -1:
            return "Section non trouvée dans l'historique."
        
        # Extraire jusqu'à la prochaine section majeure (##) ou fin
        section_lines = []
        for i in range(start_idx, min(start_idx + 50, len(lines))):
            line = lines[i]
            # Arrêter à la prochaine section majeure
            if i > start_idx and line.startswith('##') and not line.startswith('###'):
                break
            section_lines.append(line)
        
        return '\n'.join(section_lines).strip()


class TTSEngine:
    """Synthèse vocale avec gTTS (gratuit)"""
    
    def __init__(self):
        self.output_dir = "temp/audio"
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("✅ TTS Engine initialisé (gTTS gratuit)")
    
    def synthesize(self, text: str, lang: str = "fr") -> str:
        """
        Génère fichier audio depuis texte
        
        Args:
            text: Texte à synthétiser
            lang: Langue (fr, ar, en)
            
        Returns:
            Chemin du fichier audio généré
        """
        try:
            # Créer hash unique pour cache
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            audio_path = os.path.join(self.output_dir, f"audio_{text_hash}.mp3")
            
            # Si déjà généré, retourner directement
            if os.path.exists(audio_path):
                logger.info(f"♻️ Audio en cache: {audio_path}")
                return audio_path
            
            # Générer avec gTTS
            logger.info(f"🔄 Génération audio ({len(text)} caractères)...")
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(audio_path)
            
            logger.info(f"✅ Audio généré: {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"❌ Erreur TTS: {e}")
            raise


class AvatarController:
    """Contrôleur principal de l'avatar"""
    
    def __init__(self):
        self.historique = HistoriqueCANLoader()
        self.tts = TTSEngine()
        logger.info("✅ Avatar Controller initialisé")
    
    def process_question(self, question: str) -> dict:
        """
        Traite une question et génère la réponse audio
        
        Args:
            question: Question de l'utilisateur
            
        Returns:
            Dict avec réponse texte et audio
        """
        try:
            logger.info(f"❓ Question reçue: {question}")
            
            # 1. Rechercher dans l'historique
            info_found = self.historique.search_info(question)
            
            # 2. Générer réponse naturelle
            response = self._generate_natural_response(question, info_found)
            
            # 3. Synthétiser en audio
            audio_path = self.tts.synthesize(response, lang="fr")
            
            # 4. Calculer durée approximative
            words = len(response.split())
            duration = words * 0.4  # ~150 mots/minute
            
            result = {
                "question": question,
                "response": response,
                "audio_path": audio_path,
                "duration": round(duration, 1),
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
            logger.info(f"✅ Réponse générée ({words} mots, {duration}s)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur traitement question: {e}")
            return {
                "question": question,
                "response": "Désolé, je n'ai pas pu traiter votre question.",
                "audio_path": None,
                "duration": 0,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }
    
    def _generate_natural_response(self, question: str, info: str) -> str:
        """
        Génère une réponse naturelle basée sur l'info trouvée
        
        Args:
            question: Question originale
            info: Information trouvée
            
        Returns:
            Réponse formulée naturellement
        """
        question_lower = question.lower()
        
        # Intro dynamique
        intros = [
            "Excellente question ! ",
            "Laissez-moi vous répondre. ",
            "C'est une question intéressante. ",
            "Voici ce que je peux vous dire. ",
            "D'après l'historique de la CAN, "
        ]
        
        import random
        intro = random.choice(intros)
        
        # Extraire les faits principaux
        if "maroc" in question_lower:
            if "1976" in info:
                response = (
                    f"{intro}Le Maroc a remporté sa première et unique Coupe d'Afrique en 1976 en Éthiopie. "
                    "C'était une victoire historique contre la Guinée, avec un score de 1 à 1, "
                    "puis 3 à 0 aux tirs au but. Cette victoire fait du Maroc la première équipe "
                    "d'Afrique du Nord à remporter la CAN. Le Maroc a également été finaliste en 2004, "
                    "perdant contre la Tunisie 2 à 1."
                )
            elif "2025" in info:
                response = (
                    f"{intro}La CAN 2025 se déroulera au Maroc du 21 décembre 2025 au 18 janvier 2026. "
                    "Le tournoi se jouera dans 6 stades à travers le pays, dont le Grand Stade de Casablanca "
                    "qui peut accueillir 93 000 spectateurs. Le Maroc vise à remporter son deuxième titre, "
                    "49 ans après sa première victoire en 1976."
                )
            else:
                response = (
                    f"{intro}Le Maroc a une riche histoire en CAN. Champion en 1976, "
                    "finaliste en 2004, et pays hôte en 2025. Les Lions de l'Atlas ont participé "
                    "à 18 éditions de la compétition."
                )
        
        elif "égypte" in question_lower or "record" in question_lower:
            response = (
                f"{intro}L'Égypte est la nation la plus titrée de l'histoire de la CAN avec 7 titres ! "
                "Ils ont remporté la compétition en 1957, 1959, 1986, 1998, 2006, 2008 et 2010. "
                "L'exploit le plus remarquable est leur triple consécutif entre 2006 et 2010, "
                "une performance unique dans l'histoire de la compétition."
            )
        
        elif "cameroun" in question_lower:
            response = (
                f"{intro}Le Cameroun est le deuxième pays le plus titré avec 5 victoires en CAN. "
                "Les Indomptables ont été champions en 1984, 1988, 2000, 2002 et 2017. "
                "Samuel Eto'o, légende camerounaise, détient le record de buts en CAN avec 18 réalisations."
            )
        
        elif "buteur" in question_lower or "eto" in question_lower:
            response = (
                f"{intro}Samuel Eto'o du Cameroun est le meilleur buteur de l'histoire de la CAN "
                "avec 18 buts marqués entre 1996 et 2010. Il a également remporté 4 titres, "
                "un record pour un joueur. Derrière lui, on trouve Laurent Pokou de Côte d'Ivoire "
                "avec 14 buts, et Rashidi Yekini du Nigeria avec 13 buts."
            )
        
        elif "sénégal" in question_lower:
            response = (
                f"{intro}Le Sénégal a remporté sa première Coupe d'Afrique en 2021 au Cameroun. "
                "Après deux finales perdues en 2002 et 2019, les Lions de la Teranga ont enfin "
                "triomphé en battant l'Égypte 0 à 0, puis 4 à 2 aux tirs au but. "
                "Sadio Mané a été le héros de cette victoire historique."
            )
        
        elif "zambie" in question_lower:
            response = (
                f"{intro}La Zambie a une histoire émouvante en CAN. En 2012, ils ont remporté "
                "leur premier et unique titre au Gabon, sur le lieu exact où l'équipe nationale "
                "avait péri dans un crash aérien en 1993. Cette victoire contre la Côte d'Ivoire "
                "aux tirs au but était un hommage poignant aux joueurs disparus."
            )
        
        elif "première" in question_lower or "origine" in question_lower:
            response = (
                f"{intro}La première Coupe d'Afrique des Nations a eu lieu en 1957 au Soudan. "
                "Seulement trois équipes y ont participé : l'Égypte, l'Éthiopie et le Soudan. "
                "L'Égypte a remporté cette première édition en battant l'Éthiopie 4 à 0 en finale. "
                "La compétition a été créée par la Confédération Africaine de Football."
            )
        
        elif "2023" in question_lower or "côte" in question_lower and "ivoire" in question_lower:
            response = (
                f"{intro}La CAN 2023 en Côte d'Ivoire a été spectaculaire ! "
                "Les Éléphants ont remporté leur troisième titre à domicile en battant le Nigeria 2 à 1 en finale. "
                "C'était une remontada historique : menacés d'élimination au premier tour, "
                "ils ont finalement soulevé le trophée devant leur public."
            )
        
        else:
            # Réponse générique avec info trouvée
            # Limiter à 200 caractères max
            info_clean = info.replace('#', '').replace('*', '').replace('|', '')[:400]
            response = f"{intro}Voici ce que l'historique nous dit : {info_clean}"
        
        return response
    
    def get_popular_questions(self) -> list:
        """Retourne des questions populaires suggérées"""
        return [
            "Qui a remporté le plus de CAN ?",
            "Quand le Maroc a-t-il gagné la CAN ?",
            "Qui est le meilleur buteur de l'histoire ?",
            "Quand aura lieu la CAN 2025 ?",
            "Quelle est l'histoire du Cameroun en CAN ?",
            "Parle-moi de la victoire du Sénégal en 2021",
            "Raconte-moi l'histoire de la Zambie en 2012",
            "Combien de fois l'Égypte a gagné la CAN ?",
            "Quelle équipe a gagné la CAN 2023 ?",
            "Quand a été créée la Coupe d'Afrique ?"
        ]


if __name__ == "__main__":
    # Test du système
    print("\n" + "="*70)
    print("🎭 TEST DU SYSTÈME AVATAR VIRTUEL")
    print("="*70 + "\n")
    
    avatar = AvatarController()
    
    # Questions de test
    test_questions = [
        "Qui a remporté le plus de CAN ?",
        "Quand le Maroc a-t-il gagné la CAN ?",
        "Qui est le meilleur buteur de l'histoire ?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print("-" * 70)
        
        result = avatar.process_question(question)
        
        if result['success']:
            print(f"✅ Réponse ({result['duration']}s):")
            print(f"{result['response'][:200]}...")
            print(f"🔊 Audio: {result['audio_path']}")
        else:
            print(f"❌ Erreur: {result.get('error')}")
        
        print()
    
    print("="*70)
    print("✅ Tests terminés !")
    print("="*70 + "\n")
