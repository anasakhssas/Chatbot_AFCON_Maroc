"""Demo scraper with sample CAN 2025 data for testing"""
import json
from datetime import datetime
from pathlib import Path
from .config import DATA_DIR, TIMESTAMP_FORMAT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sample_can2025_data():
    """Generate sample CAN 2025 news data based on the Wikipedia information"""
    
    sample_articles = [
        {
            "id": f"demo_1_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Morocco Opens AFCON 2025 with Victory Over Comoros",
            "content": "Morocco kicked off the 2025 Africa Cup of Nations with a commanding 2-0 victory over Comoros at Prince Moulay Abdellah Stadium. Brahim Díaz opened the scoring in the 55th minute, with Ayoub El Kaabi doubling the lead in the 74th minute. The Atlas Lions dominated possession and showcased their attacking prowess in front of 60,180 fans in Rabat.",
            "date": "2025-12-21",
            "link": "https://www.cafonline.com/afcon2025/news/morocco-beats-comoros-2-0",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "Morocco", "Comoros", "Group A", "Brahim Díaz", "El Kaabi"],
            "category": "match_result"
        },
        {
            "id": f"demo_2_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Egypt Defeats Zimbabwe 2-1 in Thrilling Group B Encounter",
            "content": "Mohamed Salah scored a crucial late penalty as Egypt came from behind to beat Zimbabwe 2-1 at Adrar Stadium in Agadir. Prince Dube gave Zimbabwe the lead in the 20th minute, but Omar Marmoush equalized in the 64th minute before Salah's penalty in stoppage time secured all three points for the Pharaohs.",
            "date": "2025-12-22",
            "link": "https://www.cafonline.com/afcon2025/news/egypt-zimbabwe-result",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "Egypt", "Zimbabwe", "Mohamed Salah", "Group B"],
            "category": "match_result"
        },
        {
            "id": f"demo_3_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Nigeria Dominates Tunisia 3-2 in Group C Thriller",
            "content": "Nigeria showcased their attacking prowess with a 3-2 victory over Tunisia at Fez Stadium. Victor Osimhen, Wilfred Ndidi, and Ademola Lookman scored for the Super Eagles, who demonstrated why they're among the tournament favorites. Tunisia fought back bravely but couldn't overcome Nigeria's quality.",
            "date": "2025-12-27",
            "link": "https://www.cafonline.com/afcon2025/news/nigeria-tunisia-3-2",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "Nigeria", "Tunisia", "Group C", "Osimhen", "Lookman"],
            "category": "match_result"
        },
        {
            "id": f"demo_4_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Senegal and DR Congo Play Out 1-1 Draw in Group D",
            "content": "Senegal and DR Congo shared the spoils in an entertaining 1-1 draw at Tangier Grand Stadium. Sadio Mané scored for Senegal in the 69th minute, but Cédric Bakambu equalized for DR Congo just eight minutes later. Both teams remain strong contenders to progress from Group D.",
            "date": "2025-12-27",
            "link": "https://www.cafonline.com/afcon2025/news/senegal-drcongo-draw",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "Senegal", "DR Congo", "Sadio Mané", "Group D"],
            "category": "match_result"
        },
        {
            "id": f"demo_5_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Algeria Tops Group E with Perfect Record",
            "content": "Algeria secured their place at the top of Group E with a commanding 3-1 victory over Equatorial Guinea. Riyad Mahrez was the star of the show, contributing to all three goals. The Desert Foxes have won all three group games and look like genuine title contenders.",
            "date": "2025-12-31",
            "link": "https://www.cafonline.com/afcon2025/news/algeria-perfect-record",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "Algeria", "Mahrez", "Group E", "Equatorial Guinea"],
            "category": "match_result"
        },
        {
            "id": f"demo_6_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Ivory Coast Defeats Gabon 3-2 in Group F Thriller",
            "content": "The defending champions Ivory Coast came from behind twice to beat Gabon 3-2 in a thrilling Group F encounter at Marrakesh Stadium. Gabon's Denis Bouanga and Guélor Kanga had given them a 2-1 lead, but late goals from Evann Guessand and Bazoumana Touré secured victory for Les Éléphants.",
            "date": "2025-12-31",
            "link": "https://www.cafonline.com/afcon2025/news/ivory-coast-gabon-3-2",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "Ivory Coast", "Gabon", "defending champions", "Group F"],
            "category": "match_result"
        },
        {
            "id": f"demo_7_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Morocco Prepares for Round of 16 Against Tanzania",
            "content": "Host nation Morocco will face Tanzania in the Round of 16 at Prince Moulay Abdellah Stadium on January 4th. The Atlas Lions topped Group A with 7 points and will be looking to continue their impressive run in front of their home fans. Tanzania qualified as one of the best third-placed teams.",
            "date": "2026-01-01",
            "link": "https://www.cafonline.com/afcon2025/news/morocco-tanzania-preview",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "Morocco", "Tanzania", "Round of 16", "knockout"],
            "category": "match_preview"
        },
        {
            "id": f"demo_8_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "CAF Announces Match Officials for AFCON 2025 Knockout Stage",
            "content": "The Confederation of African Football has announced the list of match officials who will oversee the knockout stage matches of the 2025 Africa Cup of Nations. The selection includes 28 referees and 31 assistant referees from across the continent, ensuring the highest standards of officiating.",
            "date": "2026-01-01",
            "link": "https://www.cafonline.com/afcon2025/news/match-officials-knockout",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "match officials", "referees", "knockout stage"],
            "category": "tournament_news"
        },
        {
            "id": f"demo_9_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Record Attendance at Tangier Grand Stadium",
            "content": "The Tangier Grand Stadium set a new attendance record for the tournament with 75,000 fans packing the venue for the Group D match between Senegal and DR Congo. The passionate atmosphere showcased the Moroccan fans' love for African football and created an unforgettable experience.",
            "date": "2025-12-27",
            "link": "https://www.cafonline.com/afcon2025/news/record-attendance-tangier",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "attendance", "Tangier", "stadium", "fans"],
            "category": "tournament_news"
        },
        {
            "id": f"demo_10_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": "Riyad Mahrez Leads Golden Boot Race with 3 Goals",
            "content": "Algeria's Riyad Mahrez is currently leading the race for the Golden Boot with 3 goals after the group stage. He is tied with Morocco's Ayoub El Kaabi and Brahim Díaz. The competition for top scorer promises to intensify as the knockout stages begin.",
            "date": "2026-01-01",
            "link": "https://www.cafonline.com/afcon2025/news/golden-boot-race",
            "source": "CAF AFCON 2025",
            "fetched_at": datetime.now().isoformat(),
            "keywords": ["CAN 2025", "AFCON", "Riyad Mahrez", "Golden Boot", "top scorer", "Algeria"],
            "category": "statistics"
        }
    ]
    
    return sample_articles


def save_demo_data():
    """Save demo data to file"""
    articles = generate_sample_can2025_data()
    
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    filename = f"can2025_demo_data_{timestamp}.json"
    filepath = DATA_DIR / filename
    
    data = {
        'metadata': {
            'total_articles': len(articles),
            'fetch_date': datetime.now().isoformat(),
            'sources': ['CAF AFCON 2025'],
            'note': 'This is demo data based on real AFCON 2025 information for testing purposes'
        },
        'articles': articles
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ Demo data saved: {len(articles)} articles")
    logger.info(f"📁 File location: {filepath}")
    return str(filepath)


if __name__ == "__main__":
    print("=" * 70)
    print("🏆 CAN 2025 - Demo Data Generator")
    print("=" * 70)
    filepath = save_demo_data()
    print(f"\n✅ Success! Demo data created at:\n{filepath}")
    print("\n📊 Articles include:")
    print("  - Match results from Group Stage")
    print("  - Tournament news and updates")
    print("  - Player statistics")
    print("  - Match previews")
    print("=" * 70)
