"""
Setup script for the customer support chatbot.
"""
import nltk
import ssl
import logging

def download_nltk_data():
    """Download required NLTK data."""
    try:
        # Handle SSL certificate issues
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        print("✓ NLTK data downloaded successfully")
        
    except Exception as e:
        print(f"⚠ Warning: Could not download NLTK data: {e}")
        print("The chatbot will still work, but some NLP features may be limited.")

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('chatbot.log'),
            logging.StreamHandler()
        ]
    )
    print("✓ Logging configured")

def main():
    """Run setup tasks."""
    print("Setting up Customer Support Chatbot...")
    
    # Download NLTK data
    download_nltk_data()
    
    # Setup logging
    setup_logging()
    
    print("\n✓ Setup complete!")
    print("\nTo start the chatbot:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run setup: python setup.py")
    print("3. Start the web interface: python app.py")
    print("4. Run tests: python run_tests.py")

if __name__ == '__main__':
    main()