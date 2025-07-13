"""
Main chatbot class that orchestrates all components.
"""
import logging
import random
from typing import Dict, List, Optional
from datetime import datetime

from models.nlp_processor import NLPProcessor
from models.knowledge_base import KnowledgeBase
from api.mock_apis import APIManager, MockAPIError
from config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CustomerSupportChatbot:
    """
    Main chatbot class that handles customer support interactions.
    
    This class integrates NLP processing, knowledge base lookup,
    API calls, and response generation to provide comprehensive
    customer support functionality.
    """
    
    def __init__(self):
        """Initialize the chatbot with all required components."""
        logger.info("Initializing Customer Support Chatbot")
        
        self.nlp_processor = NLPProcessor()
        self.knowledge_base = KnowledgeBase()
        self.api_manager = APIManager()
        
        # Conversation state tracking
        self.conversation_history = []
        self.user_context = {}
        
        logger.info("Chatbot initialization complete")
    
    def process_message(self, message: str, user_id: Optional[str] = None) -> Dict:
        """
        Process a user message and generate an appropriate response.
        
        Args:
            message: User's input message
            user_id: Optional user identifier for context
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Log the incoming message
            logger.info(f"Processing message from user {user_id}: {message[:100]}...")
            
            # Process message through NLP
            nlp_result = self.nlp_processor.process_message(message)
            
            # Update conversation history
            self._update_conversation_history(message, nlp_result, user_id)
            
            # Generate response based on intent and context
            response = self._generate_response(nlp_result, user_id)
            
            # Log the response
            logger.info(f"Generated response for user {user_id}: {response['text'][:100]}...")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return self._generate_error_response(nlp_result.get('language', 'en'))
    
    def _update_conversation_history(self, message: str, nlp_result: Dict, user_id: Optional[str]):
        """Update conversation history with the current interaction."""
        conversation_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'message': message,
            'nlp_result': nlp_result
        }
        
        self.conversation_history.append(conversation_entry)
        
        # Keep only last 50 conversations to manage memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def _generate_response(self, nlp_result: Dict, user_id: Optional[str]) -> Dict:
        """
        Generate an appropriate response based on NLP analysis.
        
        Args:
            nlp_result: Results from NLP processing
            user_id: User identifier
            
        Returns:
            Response dictionary
        """
        intent = nlp_result['intent']
        confidence = nlp_result['intent_confidence']
        language = nlp_result['language']
        sentiment = self._classify_sentiment(nlp_result['sentiment'])
        entities = nlp_result['entities']
        
        # Check if confidence is high enough
        if confidence < Config.INTENT_CONFIDENCE_THRESHOLD:
            return self._handle_low_confidence(nlp_result)
        
        # Route to appropriate handler based on intent
        response_handlers = {
            'greeting': self._handle_greeting,
            'product_info': self._handle_product_info,
            'pricing': self._handle_pricing,
            'shipping': self._handle_shipping,
            'returns': self._handle_returns,
            'technical_support': self._handle_technical_support,
            'order_status': self._handle_order_status,
            'account': self._handle_account_info
        }
        
        handler = response_handlers.get(intent, self._handle_general_query)
        
        try:
            response = handler(nlp_result, user_id)
            
            # Add sentiment-aware tone adjustment
            response = self._adjust_response_tone(response, sentiment, language)
            
            return {
                'text': response,
                'intent': intent,
                'confidence': confidence,
                'language': language,
                'sentiment': sentiment,
                'entities': entities,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in response handler for intent {intent}: {str(e)}")
            return self._generate_error_response(language)
    
    def _classify_sentiment(self, sentiment_scores: Dict) -> str:
        """Classify sentiment based on polarity score."""
        polarity = sentiment_scores['polarity']
        
        if polarity > Config.SENTIMENT_POSITIVE_THRESHOLD:
            return 'positive'
        elif polarity < Config.SENTIMENT_NEGATIVE_THRESHOLD:
            return 'negative'
        else:
            return 'neutral'
    
    def _handle_greeting(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle greeting intents."""
        language = nlp_result['language']
        return self.knowledge_base.get_response_template('greeting', language)
    
    def _handle_product_info(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle product information requests."""
        language = nlp_result['language']
        message = nlp_result['original_text']
        
        # Try to find product information
        product_info = self.knowledge_base.get_product_info(message)
        
        if product_info:
            return self.knowledge_base._format_product_response(product_info, language)
        else:
            # Check inventory for mentioned products
            try:
                # Extract potential product IDs from entities or message
                for word in message.lower().split():
                    if word in ['laptop', 'smartphone', 'headphones']:
                        product_id = f"{word}_pro" if word == 'laptop' else f"{word}_x" if word == 'smartphone' else f"{word}_wireless"
                        inventory = self.api_manager.call_api('inventory', 'check_inventory', product_id)
                        
                        if language == 'es':
                            return f"Información del producto {inventory['name']}:\nCantidad disponible: {inventory['available_quantity']}\nÚltima actualización: {inventory['last_updated']}"
                        else:
                            return f"Product information for {inventory['name']}:\nAvailable quantity: {inventory['available_quantity']}\nLast updated: {inventory['last_updated']}"
            except MockAPIError:
                pass
            
            return self.knowledge_base.get_response_template('product_info', language)
    
    def _handle_pricing(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle pricing inquiries."""
        language = nlp_result['language']
        message = nlp_result['original_text']
        
        # Try to find product pricing
        product_info = self.knowledge_base.get_product_info(message)
        
        if product_info:
            if language == 'es':
                return f"El precio de {product_info['name']} es ${product_info['price']}"
            else:
                return f"The price for {product_info['name']} is ${product_info['price']}"
        
        return self.knowledge_base.get_response_template('pricing', language)
    
    def _handle_shipping(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle shipping and delivery inquiries."""
        language = nlp_result['language']
        entities = nlp_result['entities']
        
        # Check if user provided an order number
        if entities['order_numbers']:
            order_id = entities['order_numbers'][0]
            try:
                order_info = self.api_manager.call_api('order', 'get_order_status', order_id)
                
                if language == 'es':
                    response = f"Estado del pedido {order_id}:\n"
                    response += f"Estado: {order_info['status']}\n"
                    response += f"Entrega estimada: {order_info['estimated_delivery']}\n"
                    if order_info.get('tracking_number'):
                        response += f"Número de seguimiento: {order_info['tracking_number']}"
                else:
                    response = f"Order {order_id} status:\n"
                    response += f"Status: {order_info['status']}\n"
                    response += f"Estimated delivery: {order_info['estimated_delivery']}\n"
                    if order_info.get('tracking_number'):
                        response += f"Tracking number: {order_info['tracking_number']}"
                
                return response
                
            except MockAPIError as e:
                if language == 'es':
                    return f"Lo siento, no pude encontrar información para el pedido {order_id}. Error: {str(e)}"
                else:
                    return f"Sorry, I couldn't find information for order {order_id}. Error: {str(e)}"
        
        # Provide general shipping information
        faq_answer = self.knowledge_base.get_faq_answer("shipping time", language)
        if faq_answer:
            return faq_answer
        
        return self.knowledge_base.get_response_template('shipping', language)
    
    def _handle_returns(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle return and refund requests."""
        language = nlp_result['language']
        
        # Provide return policy information
        faq_answer = self.knowledge_base.get_faq_answer("return policy", language)
        if faq_answer:
            return faq_answer
        
        return self.knowledge_base.get_response_template('returns', language)
    
    def _handle_technical_support(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle technical support requests."""
        language = nlp_result['language']
        
        base_response = self.knowledge_base.get_response_template('technical_support', language)
        
        # Add some common troubleshooting steps
        if language == 'es':
            troubleshooting = "\n\nPasos básicos de solución de problemas:\n1. Reinicia el dispositivo\n2. Verifica las conexiones\n3. Actualiza el software\n4. Contacta soporte técnico si el problema persiste"
        else:
            troubleshooting = "\n\nBasic troubleshooting steps:\n1. Restart the device\n2. Check all connections\n3. Update software\n4. Contact technical support if the issue persists"
        
        return base_response + troubleshooting
    
    def _handle_order_status(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle order status inquiries."""
        language = nlp_result['language']
        entities = nlp_result['entities']
        
        if entities['order_numbers']:
            order_id = entities['order_numbers'][0]
            try:
                order_info = self.api_manager.call_api('order', 'get_order_status', order_id)
                
                if language == 'es':
                    response = f"Estado del pedido {order_id}:\n"
                    response += f"Estado: {order_info['status']}\n"
                    response += f"Total: ${order_info['total']}\n"
                    response += f"Fecha del pedido: {order_info['order_date']}\n"
                    response += f"Entrega estimada: {order_info['estimated_delivery']}"
                else:
                    response = f"Order {order_id} status:\n"
                    response += f"Status: {order_info['status']}\n"
                    response += f"Total: ${order_info['total']}\n"
                    response += f"Order date: {order_info['order_date']}\n"
                    response += f"Estimated delivery: {order_info['estimated_delivery']}"
                
                return response
                
            except MockAPIError as e:
                if language == 'es':
                    return f"Lo siento, no pude encontrar el pedido {order_id}. Por favor verifica el número de pedido."
                else:
                    return f"Sorry, I couldn't find order {order_id}. Please check the order number."
        
        if language == 'es':
            return "Para verificar el estado de tu pedido, por favor proporciona tu número de pedido."
        else:
            return "To check your order status, please provide your order number."
    
    def _handle_account_info(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle account information requests."""
        language = nlp_result['language']
        
        if user_id:
            try:
                user_info = self.api_manager.call_api('user', 'get_user_info', user_id)
                
                if language == 'es':
                    response = f"Información de la cuenta:\n"
                    response += f"Nombre: {user_info['name']}\n"
                    response += f"Email: {user_info['email']}\n"
                    response += f"Nivel de membresía: {user_info['membership_level']}\n"
                    response += f"Estado de la cuenta: {user_info['account_status']}"
                else:
                    response = f"Account information:\n"
                    response += f"Name: {user_info['name']}\n"
                    response += f"Email: {user_info['email']}\n"
                    response += f"Membership level: {user_info['membership_level']}\n"
                    response += f"Account status: {user_info['account_status']}"
                
                return response
                
            except MockAPIError as e:
                if language == 'es':
                    return f"Lo siento, no pude acceder a la información de tu cuenta. Error: {str(e)}"
                else:
                    return f"Sorry, I couldn't access your account information. Error: {str(e)}"
        
        if language == 'es':
            return "Para acceder a la información de tu cuenta, necesito que inicies sesión primero."
        else:
            return "To access your account information, I need you to log in first."
    
    def _handle_general_query(self, nlp_result: Dict, user_id: Optional[str]) -> str:
        """Handle general queries using knowledge base search."""
        language = nlp_result['language']
        message = nlp_result['original_text']
        
        # Search knowledge base
        kb_result = self.knowledge_base.search_knowledge_base(message, language)
        
        if kb_result:
            return kb_result
        
        return self.knowledge_base.get_response_template('fallback', language)
    
    def _handle_low_confidence(self, nlp_result: Dict) -> Dict:
        """Handle cases where intent confidence is low."""
        language = nlp_result['language']
        
        # Try knowledge base search as fallback
        kb_result = self.knowledge_base.search_knowledge_base(nlp_result['original_text'], language)
        
        if kb_result:
            response_text = kb_result
        else:
            response_text = self.knowledge_base.get_response_template('fallback', language)
        
        return {
            'text': response_text,
            'intent': 'unknown',
            'confidence': nlp_result['intent_confidence'],
            'language': language,
            'sentiment': 'neutral',
            'entities': nlp_result['entities'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _adjust_response_tone(self, response: str, sentiment: str, language: str) -> str:
        """Adjust response tone based on detected sentiment."""
        templates = self.knowledge_base.response_templates.get(language, self.knowledge_base.response_templates['en'])
        
        if sentiment == 'negative' and 'negative_sentiment' in templates:
            prefix = random.choice(templates['negative_sentiment'])
            return prefix + response
        elif sentiment == 'positive' and 'positive_sentiment' in templates:
            prefix = random.choice(templates['positive_sentiment'])
            return prefix + response
        
        return response
    
    def _generate_error_response(self, language: str = 'en') -> Dict:
        """Generate a generic error response."""
        if language == 'es':
            error_text = "Lo siento, ocurrió un error técnico. Por favor intenta de nuevo o contacta a nuestro equipo de soporte."
        else:
            error_text = "I'm sorry, a technical error occurred. Please try again or contact our support team."
        
        return {
            'text': error_text,
            'intent': 'error',
            'confidence': 1.0,
            'language': language,
            'sentiment': 'neutral',
            'entities': {},
            'timestamp': datetime.now().isoformat()
        }
    
    def get_conversation_history(self, user_id: Optional[str] = None) -> List[Dict]:
        """
        Get conversation history, optionally filtered by user.
        
        Args:
            user_id: Optional user identifier to filter by
            
        Returns:
            List of conversation entries
        """
        if user_id:
            return [entry for entry in self.conversation_history if entry.get('user_id') == user_id]
        
        return self.conversation_history.copy()
    
    def clear_conversation_history(self, user_id: Optional[str] = None):
        """
        Clear conversation history, optionally for a specific user.
        
        Args:
            user_id: Optional user identifier to clear history for
        """
        if user_id:
            self.conversation_history = [
                entry for entry in self.conversation_history 
                if entry.get('user_id') != user_id
            ]
        else:
            self.conversation_history.clear()
        
        logger.info(f"Cleared conversation history for user: {user_id or 'all users'}")