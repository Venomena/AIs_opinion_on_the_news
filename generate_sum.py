import requests
from app import db, BlogPost, app
import logging
from app import AIStatus
from groq import Groq
import os

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
LLM_API_ENDPOINT = 'https://api.groq.com/openai/v1'
GROQ_API_KEY='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'
LLM_API_HEADERS = {
    'Content-Type': 'application/json',
    # Add any required headers here, such as Authorization tokens
    # 'Authorization': 'Bearer YOUR_TOKEN',
}

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_llm_api(prompt):
    """
    Calls the Groq API for content generation or summarization.
    """
    # GROQ_API_KEY="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"
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Groq API call failed."


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
