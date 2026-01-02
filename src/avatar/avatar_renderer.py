"""
Avatar visuel animé avec expression faciale simple
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64


class AvatarRenderer:
    """Rendu de l'avatar avec expressions faciales"""
    
    def __init__(self):
        self.colors = {
            'skin': (210, 180, 140),      # Ton peau
            'maroc_red': (193, 39, 45),   # Rouge Maroc
            'maroc_green': (0, 98, 51),   # Vert Maroc
            'white': (255, 255, 255),
            'black': (50, 50, 50),
            'mouth_line': (100, 50, 50)
        }
    
    def create_avatar(self, state: str = "neutral", size: tuple = (400, 400)):
        """
        Crée une image d'avatar avec expression
        
        Args:
            state: "neutral", "speaking", "happy", "thinking"
            size: Taille de l'image
            
        Returns:
            Image base64 encodée
        """
        # Créer image
        img = Image.new('RGB', size, (245, 245, 245))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = size[0] // 2, size[1] // 2
        
        # Cercle de fond (drapeau Maroc style)
        draw.ellipse(
            [50, 50, size[0]-50, size[1]-50],
            fill=self.colors['maroc_red'],
            outline=self.colors['maroc_green'],
            width=8
        )
        
        # Visage (cercle peau)
        face_radius = 120
        draw.ellipse(
            [center_x - face_radius, center_y - face_radius - 20,
             center_x + face_radius, center_y + face_radius - 20],
            fill=self.colors['skin'],
            outline=self.colors['black'],
            width=3
        )
        
        # Cheveux (style maghrébin)
        for i in range(-3, 4):
            x_offset = i * 35
            draw.ellipse(
                [center_x + x_offset - 20, center_y - face_radius - 40,
                 center_x + x_offset + 20, center_y - face_radius + 20],
                fill=self.colors['black']
            )
        
        # Yeux
        eye_y = center_y - 40
        left_eye_x = center_x - 40
        right_eye_x = center_x + 40
        
        if state == "thinking":
            # Yeux fermés (en réflexion)
            draw.line([left_eye_x - 15, eye_y, left_eye_x + 15, eye_y], 
                     fill=self.colors['black'], width=4)
            draw.line([right_eye_x - 15, eye_y, right_eye_x + 15, eye_y], 
                     fill=self.colors['black'], width=4)
        else:
            # Yeux ouverts
            # Blanc des yeux
            for eye_x in [left_eye_x, right_eye_x]:
                draw.ellipse([eye_x - 15, eye_y - 12, eye_x + 15, eye_y + 12],
                           fill=self.colors['white'], 
                           outline=self.colors['black'], width=2)
                # Pupilles
                draw.ellipse([eye_x - 6, eye_y - 6, eye_x + 6, eye_y + 6],
                           fill=self.colors['black'])
        
        # Bouche (varie selon l'état)
        mouth_y = center_y + 30
        
        if state == "speaking":
            # Bouche ouverte (forme O)
            draw.ellipse(
                [center_x - 20, mouth_y - 15, center_x + 20, mouth_y + 15],
                fill=self.colors['mouth_line'],
                outline=self.colors['black'],
                width=3
            )
        elif state == "happy":
            # Sourire large
            draw.arc(
                [center_x - 40, mouth_y - 20, center_x + 40, mouth_y + 20],
                start=0, end=180,
                fill=self.colors['black'],
                width=5
            )
        elif state == "thinking":
            # Bouche de réflexion (ligne)
            draw.line(
                [center_x - 30, mouth_y, center_x + 30, mouth_y],
                fill=self.colors['black'],
                width=3
            )
        else:  # neutral
            # Sourire léger
            draw.arc(
                [center_x - 35, mouth_y - 15, center_x + 35, mouth_y + 15],
                start=0, end=180,
                fill=self.colors['black'],
                width=4
            )
        
        # Badge "Expert CAN" (étoile verte)
        star_x = center_x + 80
        star_y = center_y - 60
        draw.polygon(
            [
                (star_x, star_y - 15),
                (star_x + 5, star_y - 5),
                (star_x + 15, star_y),
                (star_x + 5, star_y + 5),
                (star_x, star_y + 15),
                (star_x - 5, star_y + 5),
                (star_x - 15, star_y),
                (star_x - 5, star_y - 5)
            ],
            fill=self.colors['maroc_green'],
            outline=self.colors['white']
        )
        
        # Convertir en base64 pour Streamlit
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def get_html_avatar(self, state: str = "neutral"):
        """Retourne HTML avec avatar intégré"""
        img_data = self.create_avatar(state)
        
        html = f"""
        <div style="
            text-align: center;
            margin: 20px 0;
        ">
            <img src="{img_data}" style="
                width: 300px;
                height: 300px;
                border-radius: 50%;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
                animation: pulse 2s infinite;
            "/>
        </div>
        
        <style>
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
            }}
        </style>
        """
        
        return html


if __name__ == "__main__":
    # Test du renderer
    renderer = AvatarRenderer()
    
    print("🧪 Test du renderer d'avatar\n")
    
    states = ["neutral", "speaking", "happy", "thinking"]
    
    for state in states:
        print(f"✅ État '{state}' généré")
        img_data = renderer.create_avatar(state)
        print(f"   Taille data: {len(img_data)} caractères\n")
    
    print("✅ Tous les états testés avec succès !")
