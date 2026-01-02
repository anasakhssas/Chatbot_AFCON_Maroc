"""
Fonctions de visualisation pour l'analyse de sentiment
"""

import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import Dict, List
import io
import base64


def create_sentiment_pie_chart(stats: Dict) -> go.Figure:
    """
    Crée un graphique en camembert des sentiments
    
    Args:
        stats: Statistiques de l'analyse
        
    Returns:
        Figure Plotly
    """
    labels = ['😊 Positif', '😐 Neutre', '😢 Négatif']
    values = [
        stats['positive']['percentage'],
        stats['neutral']['percentage'],
        stats['negative']['percentage']
    ]
    colors = ['#2ecc71', '#95a5a6', '#e74c3c']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont_size=14
    )])
    
    fig.update_layout(
        title={
            'text': f"Distribution des Sentiments ({stats['total_comments']} commentaires)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        showlegend=True,
        height=400,
        margin=dict(t=80, b=20, l=20, r=20)
    )
    
    return fig


def create_sentiment_bar_chart(stats: Dict) -> go.Figure:
    """
    Crée un graphique en barres des sentiments
    
    Args:
        stats: Statistiques de l'analyse
        
    Returns:
        Figure Plotly
    """
    categories = ['Positif', 'Neutre', 'Négatif']
    counts = [
        stats['positive']['count'],
        stats['neutral']['count'],
        stats['negative']['count']
    ]
    colors = ['#2ecc71', '#95a5a6', '#e74c3c']
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=counts,
        marker_color=colors,
        text=counts,
        textposition='auto',
        textfont=dict(size=16, color='white')
    )])
    
    fig.update_layout(
        title={
            'text': "Nombre de Commentaires par Sentiment",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        xaxis_title="Sentiment",
        yaxis_title="Nombre de commentaires",
        showlegend=False,
        height=400,
        margin=dict(t=80, b=60, l=60, r=20)
    )
    
    return fig


def create_wordcloud(comments: List[Dict], sentiment: str = None) -> str:
    """
    Crée un nuage de mots à partir des commentaires
    
    Args:
        comments: Liste des commentaires
        sentiment: Filtrer par sentiment ('positive', 'negative', 'neutral')
        
    Returns:
        Image base64 du nuage de mots
    """
    # Filtrer par sentiment si spécifié
    if sentiment:
        comments = [c for c in comments if c.get('sentiment') == sentiment]
    
    # Combiner tous les textes
    text = ' '.join([c['text'] for c in comments])
    
    if not text.strip():
        return None
    
    # Créer le nuage de mots
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(text)
    
    # Convertir en image base64
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    
    # Sauvegarder en mémoire
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    plt.close()
    
    # Encoder en base64
    img_base64 = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{img_base64}"


def create_confidence_distribution(stats: Dict) -> go.Figure:
    """
    Crée un graphique de distribution des scores de confiance
    
    Args:
        stats: Statistiques de l'analyse
        
    Returns:
        Figure Plotly
    """
    all_comments = (
        stats['positive']['comments'] +
        stats['neutral']['comments'] +
        stats['negative']['comments']
    )
    
    sentiments = []
    confidences = []
    
    for comment in all_comments:
        sentiments.append(comment['sentiment'].capitalize())
        confidences.append(comment['confidence'])
    
    fig = go.Figure()
    
    for sentiment, color in [('Positive', '#2ecc71'), ('Neutral', '#95a5a6'), ('Negative', '#e74c3c')]:
        sentiment_confidences = [
            conf for sent, conf in zip(sentiments, confidences) if sent == sentiment
        ]
        
        if sentiment_confidences:
            fig.add_trace(go.Box(
                y=sentiment_confidences,
                name=sentiment,
                marker_color=color,
                boxmean='sd'
            ))
    
    fig.update_layout(
        title={
            'text': "Distribution des Scores de Confiance",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        yaxis_title="Score de Confiance",
        showlegend=True,
        height=400,
        margin=dict(t=80, b=60, l=60, r=20)
    )
    
    return fig
