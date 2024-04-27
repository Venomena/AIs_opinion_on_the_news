import requests
from app import db, BlogPost
from app import app, db, BlogPost
import logging

# Configure logging at the start of your script or application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def some_function(data):
    logging.info('Starting some_function with data: %s', data)
    # Perform some operations
    result = data + " processed"
    logging.info('Completed some_function, result: %s', result)
    return result

# Define your actual LLM API endpoint and headers here
#OLLAMA_HOST = '127.0.0.1:11444'
LLM_API_ENDPOINT = 'http://127.0.0.1:11434/api/generate'
LLM_API_HEADERS = {
    'Content-Type': 'application/json',
    # Add other necessary headers here
}

def call_llm_api(prompt):
    """
    Calls an LLM API for content generation or summarization.
    """
    payload = {
        'model': 'llama3:8b',  # Adjust according to your LLM API
        'prompt': prompt,
        'max_tokens': 100  # Adjust as needed
    }
    try:
        response = requests.post(LLM_API_ENDPOINT, json=payload, headers=LLM_API_HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json().get('choices', [{}])[0].get('text', '')
    except requests.RequestException as e:
        print(f"Request to LLM API failed: {e}")
        return "LLM API call failed."

def summarize_all_blogs():
    """
    Generates a summary of all blog posts in the database.
    """
    with app.app_context():  # Ensures that you are within the application context
        with db.session.no_autoflush:
            blog_posts = BlogPost.query.all()
            content = " ".join(post.content for post in blog_posts)
            summary_prompt = f"Summarize the following content: {content}"
            summary = call_llm_api(summary_prompt)
            return summary
