"""
Flask web application for the customer support chatbot.
"""
from flask import Flask, request, jsonify, render_template_string
import logging
from chatbot import CustomerSupportChatbot

app = Flask(__name__)

# Initialize the chatbot
chatbot = CustomerSupportChatbot()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Support Chatbot</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 800px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 20px 20px 0 0;
        }
        
        .chat-header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }
        
        .chat-header p {
            margin: 5px 0 0 0;
            opacity: 0.9;
            font-size: 14px;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message.bot {
            justify-content: flex-start;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            border: 1px solid #e1e5e9;
            border-bottom-left-radius: 4px;
        }
        
        .message-meta {
            font-size: 11px;
            opacity: 0.6;
            margin-top: 4px;
        }
        
        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #e1e5e9;
            display: flex;
            gap: 10px;
        }
        
        .chat-input input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #e1e5e9;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .chat-input input:focus {
            border-color: #667eea;
        }
        
        .chat-input button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        
        .chat-input button:hover {
            transform: translateY(-1px);
        }
        
        .chat-input button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .typing-indicator {
            display: none;
            padding: 12px 16px;
            background: white;
            border: 1px solid #e1e5e9;
            border-radius: 18px;
            border-bottom-left-radius: 4px;
            max-width: 70%;
            margin-bottom: 15px;
        }
        
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .typing-dots span {
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
                opacity: 0.4;
            }
            30% {
                transform: translateY(-10px);
                opacity: 1;
            }
        }
        
        .language-selector {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            padding: 8px 12px;
            color: white;
            font-size: 12px;
        }
        
        @media (max-width: 768px) {
            .chat-container {
                width: 95%;
                height: 90vh;
                border-radius: 10px;
            }
            
            .chat-header {
                border-radius: 10px 10px 0 0;
                padding: 15px;
            }
            
            .message-content {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="language-selector">
                <select id="languageSelect" onchange="changeLanguage()">
                    <option value="en">English</option>
                    <option value="es">Español</option>
                </select>
            </div>
            <h1>Customer Support</h1>
            <p>How can I help you today?</p>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-content">
                    Hello! I'm your customer support assistant. I can help you with:
                    <br>• Product information and pricing
                    <br>• Order status and shipping
                    <br>• Returns and refunds
                    <br>• Technical support
                    <br>• Account information
                    <br><br>How can I assist you today?
                </div>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()" id="sendButton">Send</button>
        </div>
    </div>

    <script>
        let currentLanguage = 'en';
        
        function changeLanguage() {
            currentLanguage = document.getElementById('languageSelect').value;
            const header = document.querySelector('.chat-header');
            const placeholder = document.getElementById('messageInput');
            
            if (currentLanguage === 'es') {
                header.querySelector('h1').textContent = 'Soporte al Cliente';
                header.querySelector('p').textContent = '¿Cómo puedo ayudarte hoy?';
                placeholder.placeholder = 'Escribe tu mensaje...';
                document.getElementById('sendButton').textContent = 'Enviar';
            } else {
                header.querySelector('h1').textContent = 'Customer Support';
                header.querySelector('p').textContent = 'How can I help you today?';
                placeholder.placeholder = 'Type your message...';
                document.getElementById('sendButton').textContent = 'Send';
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            
            // Clear input and disable send button
            input.value = '';
            document.getElementById('sendButton').disabled = true;
            
            // Show typing indicator
            document.getElementById('typingIndicator').style.display = 'block';
            scrollToBottom();
            
            try {
                // Send message to chatbot
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        user_id: 'web_user_' + Date.now(),
                        language: currentLanguage
                    })
                });
                
                const data = await response.json();
                
                // Hide typing indicator
                document.getElementById('typingIndicator').style.display = 'none';
                
                // Add bot response
                addMessage(data.response.text, 'bot', data.response);
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('typingIndicator').style.display = 'none';
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
            
            // Re-enable send button
            document.getElementById('sendButton').disabled = false;
            input.focus();
        }
        
        function addMessage(text, sender, metadata = null) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = text.replace(/\\n/g, '<br>');
            
            messageDiv.appendChild(contentDiv);
            
            if (metadata) {
                const metaDiv = document.createElement('div');
                metaDiv.className = 'message-meta';
                metaDiv.textContent = `Intent: ${metadata.intent} | Confidence: ${(metadata.confidence * 100).toFixed(1)}% | Language: ${metadata.language}`;
                messageDiv.appendChild(metaDiv);
            }
            
            messagesContainer.appendChild(messageDiv);
            scrollToBottom();
        }
        
        function scrollToBottom() {
            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // Focus on input when page loads
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('messageInput').focus();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main chat interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the web interface."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        user_id = data.get('user_id')
        
        # Process the message through the chatbot
        response = chatbot.process_message(message, user_id)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for programmatic access to the chatbot."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        user_id = data.get('user_id')
        
        response = chatbot.process_message(message, user_id)
        
        return jsonify(response)
        
    except Exception as e:
        logging.error(f"Error in API chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """Get conversation history for a specific user."""
    try:
        history = chatbot.get_conversation_history(user_id)
        return jsonify({
            'user_id': user_id,
            'conversation_count': len(history),
            'history': history
        })
        
    except Exception as e:
        logging.error(f"Error getting history: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/history/<user_id>', methods=['DELETE'])
def clear_history(user_id):
    """Clear conversation history for a specific user."""
    try:
        chatbot.clear_conversation_history(user_id)
        return jsonify({
            'success': True,
            'message': f'History cleared for user {user_id}'
        })
        
    except Exception as e:
        logging.error(f"Error clearing history: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'customer-support-chatbot',
        'timestamp': chatbot.conversation_history[-1]['timestamp'] if chatbot.conversation_history else None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)