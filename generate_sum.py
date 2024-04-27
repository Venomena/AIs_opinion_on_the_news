import requests
from app import db, BlogPost, app
import logging
from app import AIStatus

# Configure logging at the start of your script or application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_blog_post_with_summary():
    global ai_status
    ai_status = "thinking"

def some_function(data):
    logging.info('Starting some_function with data: %s', data)
    # Perform some operations
    result = data + " processed"
    logging.info('Completed some_function, result: %s', result)
    return result

# Define your actual LLM API endpoint and headers here
LLM_API_ENDPOINT = 'http://127.0.0.1:11434/api/generate'
LLM_API_HEADERS = {
    'Content-Type': 'application/json',
    # Add any required headers here, such as Authorization tokens
    # 'Authorization': 'Bearer YOUR_TOKEN',
}

def call_llm_api(prompt):
    global ai_status
    ai_status = "reading previous posts"
    """
    Calls an LLM API for content generation or summarization.
    """
    payload = {
        'model': 'llama3:8b',  # Adjust the model name as necessary for your setup
        'prompt': prompt,
        'stream': False,
    }
    try:
        response = requests.post(LLM_API_ENDPOINT, json=payload, headers=LLM_API_HEADERS)
        response.raise_for_status()  # This will throw an error for non-200 responses
        return response.json().get('response', '')
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return "Failed to generate content due to an API error."

def generate_and_save_summaries():
    """
    Generates summaries for each blog post and saves them to the database.
    """
    with app.app_context():
        blog_posts = BlogPost.query.all()
        for post in blog_posts:
            summary_prompt = f"Generate a summary of this: {post.content}"
            summary = call_llm_api(summary_prompt)
            if summary:
                post.summary = summary  # Assign the generated summary to the summary column
                db.session.commit()

if __name__ == "__main__":
    generate_and_save_summaries()
    print("Summaries generated and saved to the database.")
