"""
Configuration settings for the customer support chatbot.
"""
import os
from typing import Dict, List

class Config:
    """Application configuration class."""
    
    # API Configuration
    API_HOST = os.getenv('API_HOST', 'localhost')
    API_PORT = int(os.getenv('API_PORT', 5000))
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 100))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 3600))  # 1 hour
    
    # Supported languages
    SUPPORTED_LANGUAGES = ['en', 'es']
    DEFAULT_LANGUAGE = 'en'
    
    # Sentiment thresholds
    SENTIMENT_POSITIVE_THRESHOLD = 0.1
    SENTIMENT_NEGATIVE_THRESHOLD = -0.1
    
    # Confidence thresholds
    INTENT_CONFIDENCE_THRESHOLD = 0.6
    FALLBACK_THRESHOLD = 0.3
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'chatbot.log')

# Response templates for different categories
RESPONSE_TEMPLATES = {
    'en': {
        'greeting': [
            "Hello! How can I help you today?",
            "Hi there! What can I assist you with?",
            "Welcome! How may I help you?"
        ],
        'product_info': [
            "I'd be happy to help you with product information. Could you please specify which product you're interested in?",
            "Let me help you find the product details you need. What product are you looking for?"
        ],
        'pricing': [
            "I can help you with pricing information. Which product or service are you interested in?",
            "Let me get you the latest pricing details. What would you like to know about?"
        ],
        'shipping': [
            "I can help you with shipping information. Do you have an order number or would you like general shipping details?",
            "Let me assist you with shipping. Are you asking about a specific order or general shipping policies?"
        ],
        'returns': [
            "I can help you with returns and refunds. Do you have an order number you'd like to return?",
            "Let me assist you with your return. Could you provide your order details?"
        ],
        'technical_support': [
            "I'm here to help with technical issues. Could you describe the problem you're experiencing?",
            "Let me help you resolve this technical issue. What specific problem are you facing?"
        ],
        'fallback': [
            "I'm not sure I understand. Could you please rephrase your question?",
            "I'd like to help, but I need more information. Could you be more specific?",
            "I'm having trouble understanding your request. Could you try asking in a different way?"
        ],
        'positive_sentiment': [
            "I'm glad to help! ",
            "Great! ",
            "Wonderful! "
        ],
        'negative_sentiment': [
            "I understand your frustration. Let me help resolve this for you. ",
            "I'm sorry you're experiencing this issue. I'll do my best to help. ",
            "I apologize for any inconvenience. Let me assist you. "
        ]
    },
    'es': {
        'greeting': [
            "¡Hola! ¿Cómo puedo ayudarte hoy?",
            "¡Hola! ¿En qué puedo asistirte?",
            "¡Bienvenido! ¿Cómo puedo ayudarte?"
        ],
        'product_info': [
            "Me complace ayudarte con información del producto. ¿Podrías especificar qué producto te interesa?",
            "Permíteme ayudarte a encontrar los detalles del producto que necesitas. ¿Qué producto buscas?"
        ],
        'pricing': [
            "Puedo ayudarte con información de precios. ¿Qué producto o servicio te interesa?",
            "Permíteme obtener los detalles de precios más recientes. ¿Qué te gustaría saber?"
        ],
        'shipping': [
            "Puedo ayudarte con información de envío. ¿Tienes un número de pedido o quieres detalles generales de envío?",
            "Permíteme asistirte con el envío. ¿Preguntas sobre un pedido específico o políticas generales de envío?"
        ],
        'returns': [
            "Puedo ayudarte con devoluciones y reembolsos. ¿Tienes un número de pedido que quieres devolver?",
            "Permíteme asistirte con tu devolución. ¿Podrías proporcionar los detalles de tu pedido?"
        ],
        'technical_support': [
            "Estoy aquí para ayudar con problemas técnicos. ¿Podrías describir el problema que experimentas?",
            "Permíteme ayudarte a resolver este problema técnico. ¿Qué problema específico enfrentas?"
        ],
        'fallback': [
            "No estoy seguro de entender. ¿Podrías reformular tu pregunta?",
            "Me gustaría ayudar, pero necesito más información. ¿Podrías ser más específico?",
            "Tengo problemas para entender tu solicitud. ¿Podrías intentar preguntar de otra manera?"
        ],
        'positive_sentiment': [
            "¡Me alegra ayudar! ",
            "¡Excelente! ",
            "¡Maravilloso! "
        ],
        'negative_sentiment': [
            "Entiendo tu frustración. Permíteme ayudarte a resolver esto. ",
            "Lamento que experimentes este problema. Haré mi mejor esfuerzo para ayudar. ",
            "Me disculpo por cualquier inconveniente. Permíteme asistirte. "
        ]
    }
}