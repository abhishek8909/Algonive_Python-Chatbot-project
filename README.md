# Customer Support Chatbot

A comprehensive Python-based customer support chatbot with natural language processing capabilities, multi-language support, and API integrations.

## Features

### Natural Language Processing (NLP)
- **Sentiment Analysis**: Detects customer mood and adjusts response tone accordingly
- **Intent Classification**: Understands customer queries and routes them appropriately
- **Language Detection**: Supports English and Spanish with automatic detection
- **Entity Extraction**: Identifies order numbers, emails, phone numbers, and product names
- **Typo Correction**: Handles common spelling mistakes and variations

### Response System
- **Knowledge Base**: Predefined responses for common queries (FAQ, product info, policies)
- **Dynamic Responses**: Context-aware responses based on intent and sentiment
- **Multi-language Support**: Responses in English and Spanish
- **Fallback Handling**: Graceful handling of unclear or ambiguous queries
- **Conversation History**: Tracks user interactions for context

### API Integrations
- **Order Management**: Order status tracking and shipment information
- **User Accounts**: Account information retrieval and updates
- **Inventory Management**: Real-time stock checking and availability
- **Payment Processing**: Payment status and transaction handling
- **Rate Limiting**: Prevents API abuse with configurable limits
- **Error Handling**: Robust error handling with retry mechanisms

### Technical Features
- **Object-Oriented Design**: Clean, modular architecture
- **Comprehensive Testing**: Unit tests for all major components
- **Logging**: Detailed logging for debugging and monitoring
- **Configuration Management**: Centralized configuration system
- **Web Interface**: Beautiful, responsive chat interface
- **REST API**: Programmatic access to chatbot functionality

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd customer-support-chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup**:
   ```bash
   python setup.py
   ```

## Usage

### Web Interface

Start the web application:
```bash
python app.py
```

Visit `http://lpip freeze > requirements.txt
ocalhost:5000` to access the chat interface.

### API Usage

The chatbot provides REST API endpoints:

#### Send a message
```bash
POST /api/chat
Content-Type: application/json

{
    "message": "Hello, I need help with my order",
    "user_id": "user123"
}
```

#### Get conversation history
```bash
GET /api/history/user123
```

#### Clear conversation history
```bash
DELETE /api/history/user123
```

### Programmatic Usage

```python
from chatbot import CustomerSupportChatbot

# Initialize the chatbot
chatbot = CustomerSupportChatbot()

# Process a message
response = chatbot.process_message("Hello, I need help", user_id="user123")
print(response['text'])
```

## Configuration

Edit `config.py` to customize:

- **API settings**: Timeouts, rate limits, endpoints
- **Language support**: Add new languages or modify existing ones
- **Sentiment thresholds**: Adjust sentiment classification sensitivity
- **Confidence thresholds**: Set minimum confidence for intent classification
- **Logging**: Configure log levels and output

## Testing

Run all tests:
```bash
python run_tests.py
```

Run specific test module:
```bash
python run_tests.py test_nlp_processor
```

## Architecture

### Core Components

1. **NLPProcessor** (`models/nlp_processor.py`)
   - Text preprocessing and cleaning
   - Language detection
   - Sentiment analysis
   - Intent classification
   - Entity extraction

2. **KnowledgeBase** (`models/knowledge_base.py`)
   - FAQ management
   - Product information storage
   - Response template management
   - Multi-language content

3. **APIManager** (`api/mock_apis.py`)
   - Mock API implementations
   - Rate limiting
   - Error simulation
   - Response caching

4. **CustomerSupportChatbot** (`chatbot.py`)
   - Main orchestration logic
   - Response generation
   - Conversation management
   - Context tracking

### Supported Intents

- **Greeting**: Welcome messages and general hellos
- **Product Information**: Product details, specifications, availability
- **Pricing**: Price inquiries and cost information
- **Shipping**: Delivery status, tracking, shipping policies
- **Returns**: Return policies, refund requests, exchanges
- **Technical Support**: Troubleshooting, technical issues
- **Order Status**: Order tracking, status updates
- **Account**: Account information, profile management

### API Endpoints

The chatbot simulates integration with various backend services:

- **Order API**: Order management and tracking
- **User API**: Customer account management
- **Inventory API**: Product availability and stock levels
- **Payment API**: Payment processing and transaction status

## Examples

### Basic Conversation
```
User: Hello
Bot: Hello! How can I help you today?

User: I want to know about the laptop
Bot: **Laptop Pro 15"**
Price: $1299.99
Description: High-performance laptop with 16GB RAM, 512GB SSD, and Intel i7 processor.
Availability: In Stock

User: What's the status of order ORD-123456?
Bot: Order ORD-123456 status:
Status: shipped
Total: $1299.99
Order date: 2024-01-15
Estimated delivery: 2024-01-20
```

### Spanish Support
```
User: Hola, necesito ayuda
Bot: ¡Hola! ¿Cómo puedo ayudarte hoy?

User: ¿Cuánto cuesta el teléfono?
Bot: El precio de Smartphone X es $799.99
```

### Sentiment-Aware Responses
```
User: I'm really frustrated with this terrible service!
Bot: I understand your frustration. Let me help resolve this for you. What specific issue are you experiencing?

User: This is amazing! I love it!
Bot: Great! I'm glad to help! What would you like to know more about?
```

## Extending the Chatbot

### Adding New Intents

1. **Update training data** in `NLPProcessor._setup_intent_classifier()`
2. **Add response templates** in `config.py`
3. **Create handler method** in `CustomerSupportChatbot`
4. **Update routing** in `_generate_response()`

### Adding New Languages

1. **Add language code** to `Config.SUPPORTED_LANGUAGES`
2. **Add response templates** in `RESPONSE_TEMPLATES`
3. **Update language detection** logic if needed
4. **Add FAQ translations** in `KnowledgeBase`

### Adding New APIs

1. **Create API class** in `api/mock_apis.py`
2. **Add to APIManager** initialization
3. **Update routing** in `APIManager.call_api()`
4. **Add error handling** and rate limiting

## Performance Considerations

- **Caching**: Implement response caching for frequently asked questions
- **Database**: Replace in-memory storage with persistent database for production
- **Scaling**: Use message queues for high-volume deployments
- **Monitoring**: Add metrics collection and performance monitoring

## Security

- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Prevents abuse with configurable rate limits
- **Error Handling**: Secure error messages that don't leak sensitive information
- **Logging**: Comprehensive logging for security monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
1. Check the documentation
2. Run the test suite to verify installation
3. Check the logs for error details
4. Open an issue with detailed information

## Roadmap

- [ ] Integration with real APIs (Stripe, Shopify, etc.)
- [ ] Advanced ML models for better intent classification
- [ ] Voice interface support
- [ ] Multi-channel support (email, SMS, social media)
- [ ] Analytics dashboard
- [ ] A/B testing framework
- [ ] Integration with popular helpdesk systems