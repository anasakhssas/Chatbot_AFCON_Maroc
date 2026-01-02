"""
Exporteurs pour les résumés de matchs
- PDF: Génération de documents PDF stylés
- Image: Création de cartes visuelles pour les réseaux sociaux
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List
import io
import os
import logging

logger = logging.getLogger(__name__)


class PDFExporter:
    """Exporte les résumés en PDF stylé avec les couleurs du Maroc"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
        # Style titre principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#C1272D'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Style sous-titre
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#006233'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        # Style corps de texte
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            spaceAfter=12,
            fontName='Helvetica'
        )
    
    def export_single_summary(self, summary: Dict, filepath: str):
        """
        Exporte un résumé unique en PDF
        
        Args:
            summary: Dict contenant le résumé et métadonnées
            filepath: Chemin du fichier PDF à créer
        """
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            story = []
            
            # Titre principal
            title_text = summary.get('title', 'Résumé de Match')
            story.append(Paragraph(f"🏆 {title_text}", self.title_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Métadonnées
            meta_text = f"Généré le {summary.get('generated_at', '')[:10]} • {summary.get('word_count', 0)} mots"
            story.append(Paragraph(meta_text, self.body_style))
            story.append(Spacer(1, 1*cm))
            
            # Score si disponible
            if 'score' in summary:
                score_text = f"<b>Score:</b> {summary['score']}"
                story.append(Paragraph(score_text, self.subtitle_style))
                story.append(Spacer(1, 0.5*cm))
            
            # Contenu du résumé
            summary_text = summary.get('summary', '').replace('\n', '<br/>')
            story.append(Paragraph(summary_text, self.body_style))
            
            # Footer
            story.append(Spacer(1, 2*cm))
            footer_text = "⚽ Généré automatiquement par Chatbot CAN 2025 🇲🇦"
            footer_style = ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            story.append(Paragraph(footer_text, footer_style))
            
            doc.build(story)
            logger.info(f"📄 PDF créé: {filepath}")
            
        except Exception as e:
            logger.error(f"❌ Erreur création PDF: {e}")
            raise
    
    def export_multiple_summaries(self, summaries: List[Dict], filepath: str, title: str = "Résumés de Matchs"):
        """
        Exporte plusieurs résumés en un seul PDF
        
        Args:
            summaries: Liste de résumés
            filepath: Chemin du fichier PDF
            title: Titre du document
        """
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            story = []
            
            # Titre principal
            story.append(Paragraph(f"🏆 {title}", self.title_style))
            story.append(Spacer(1, 0.3*cm))
            
            # Nombre de matchs
            count_text = f"{len(summaries)} matchs résumés"
            story.append(Paragraph(count_text, self.body_style))
            story.append(Spacer(1, 1*cm))
            
            # Chaque résumé
            for idx, summary in enumerate(summaries, 1):
                if 'error' in summary:
                    continue
                
                # Numéro et titre du match
                match_title = f"{idx}. {summary.get('title', f'Match {idx}')}"
                story.append(Paragraph(match_title, self.subtitle_style))
                story.append(Spacer(1, 0.3*cm))
                
                # Score si disponible
                if 'score' in summary:
                    score_text = f"<b>Score:</b> {summary['score']}"
                    story.append(Paragraph(score_text, self.body_style))
                
                # Résumé
                summary_text = summary.get('summary', '').replace('\n', '<br/>')
                story.append(Paragraph(summary_text, self.body_style))
                story.append(Spacer(1, 0.8*cm))
            
            # Footer
            story.append(Spacer(1, 1*cm))
            footer_text = "⚽ Généré automatiquement par Chatbot CAN 2025 🇲🇦"
            footer_style = ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            story.append(Paragraph(footer_text, footer_style))
            
            doc.build(story)
            logger.info(f"📄 PDF créé avec {len(summaries)} résumés: {filepath}")
            
        except Exception as e:
            logger.error(f"❌ Erreur création PDF multiple: {e}")
            raise


class ImageExporter:
    """Crée des cartes visuelles pour les réseaux sociaux"""
    
    def __init__(self):
        self.maroc_red = (193, 39, 45)
        self.maroc_green = (0, 98, 51)
        self.white = (255, 255, 255)
        self.light_gray = (245, 245, 245)
    
    def create_social_card(self, summary: Dict, filepath: str, size: tuple = (1080, 1080)):
        """
        Crée une carte visuelle 1080x1080 pour Instagram/Facebook
        
        Args:
            summary: Dict du résumé
            filepath: Chemin de l'image à créer
            size: Taille de l'image (défaut: 1080x1080 pour Instagram)
        """
        try:
            # Créer l'image
            img = Image.new('RGB', size, self.white)
            draw = ImageDraw.Draw(img)
            
            width, height = size
            
            # Bande supérieure rouge
            draw.rectangle([0, 0, width, 150], fill=self.maroc_red)
            
            # Bande inférieure verte
            draw.rectangle([0, height-100, width, height], fill=self.maroc_green)
            
            # Zone centrale claire
            margin = 60
            draw.rectangle(
                [margin, 200, width-margin, height-150],
                fill=self.light_gray,
                outline=self.maroc_green,
                width=3
            )
            
            # Texte - essayer d'utiliser des polices système
            try:
                title_font = ImageFont.truetype("arial.ttf", 48)
                score_font = ImageFont.truetype("arialbd.ttf", 72)
                body_font = ImageFont.truetype("arial.ttf", 32)
                small_font = ImageFont.truetype("arial.ttf", 24)
            except:
                # Fallback sur police par défaut
                title_font = ImageFont.load_default()
                score_font = ImageFont.load_default()
                body_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Titre sur la bande rouge
            title = summary.get('title', 'Match CAN 2025')[:40]
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(
                ((width - title_width) // 2, 50),
                title,
                fill=self.white,
                font=title_font
            )
            
            # Score au centre (si disponible)
            if 'score' in summary:
                score = summary['score']
                score_bbox = draw.textbbox((0, 0), score, font=score_font)
                score_width = score_bbox[2] - score_bbox[0]
                draw.text(
                    ((width - score_width) // 2, 250),
                    score,
                    fill=self.maroc_red,
                    font=score_font
                )
            
            # Résumé (extraire les lignes principales)
            summary_text = summary.get('summary', '')
            lines = []
            
            # Extraire les buteurs
            for line in summary_text.split('\n'):
                if '⚽' in line or '•' in line or 'Buts' in line or 'Stats' in line:
                    clean_line = line.strip()[:50]
                    if clean_line:
                        lines.append(clean_line)
            
            # Afficher les lignes principales
            y_pos = 400 if 'score' in summary else 300
            for line in lines[:6]:  # Max 6 lignes
                line_bbox = draw.textbbox((0, 0), line, font=body_font)
                line_width = line_bbox[2] - line_bbox[0]
                draw.text(
                    ((width - line_width) // 2, y_pos),
                    line,
                    fill=(50, 50, 50),
                    font=body_font
                )
                y_pos += 60
            
            # Footer sur la bande verte
            footer = "⚽ CAN 2025 🇲🇦"
            footer_bbox = draw.textbbox((0, 0), footer, font=body_font)
            footer_width = footer_bbox[2] - footer_bbox[0]
            draw.text(
                ((width - footer_width) // 2, height - 70),
                footer,
                fill=self.white,
                font=body_font
            )
            
            # Sauvegarder
            img.save(filepath, 'PNG', quality=95)
            logger.info(f"🖼️ Carte sociale créée: {filepath}")
            
        except Exception as e:
            logger.error(f"❌ Erreur création carte: {e}")
            raise
    
    def create_story_card(self, summary: Dict, filepath: str):
        """
        Crée une carte verticale 1080x1920 pour Instagram Stories
        
        Args:
            summary: Dict du résumé
            filepath: Chemin de l'image à créer
        """
        # Même logique mais format vertical
        self.create_social_card(summary, filepath, size=(1080, 1920))
        logger.info(f"📱 Story créée: {filepath}")


if __name__ == "__main__":
    # Test des exporteurs
    test_summary = {
        "title": "Maroc vs Égypte",
        "score": "2-1",
        "summary": """🏆 Maroc 2-1 Égypte

⚽ Buts:
• 23' - Brahim Díaz (Maroc)
• 67' - Mohamed Salah (Égypte)
• 89' - Achraf Hakimi (Maroc)

📊 Statistiques:
• Possession: 58% - 42%
• Tirs cadrés: 7-5

🌟 Homme du match: Achraf Hakimi

💬 Victoire cruciale du Maroc qui prend la tête du groupe.""",
        "word_count": 45,
        "generated_at": "2025-01-02T15:30:00"
    }
    
    print("\n🧪 Test des exporteurs\n")
    
    # Test PDF
    print("📄 Création PDF...")
    pdf_exporter = PDFExporter()
    pdf_exporter.export_single_summary(test_summary, "test_resume.pdf")
    print("✅ PDF créé: test_resume.pdf")
    
    # Test Image
    print("\n🖼️ Création carte sociale...")
    img_exporter = ImageExporter()
    img_exporter.create_social_card(test_summary, "test_card.png")
    print("✅ Carte créée: test_card.png")
