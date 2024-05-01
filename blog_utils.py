import requests
from app import db, BlogPost
from app import app, db, BlogPost
import logging
import os
from groq import Groq

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
# LLM_API_ENDPOINT = 'https://api.groq.com/openai/v1'
# GROQ_API_KEY="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"
# LLM_API_HEADERS = {
#     'Content-Type': 'application/json',
    # Add other necessary headers here
# }

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_llm_api(prompt):
    """
    Calls the Groq API for content generation or summarization.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Groq API call failed."


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
