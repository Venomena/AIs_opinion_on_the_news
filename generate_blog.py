import requests
from datetime import datetime
import logging
from app import app, db, BlogPost, AIStatus
import json
from newsapi import NewsApiClient
import time
import os
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_ai_status(new_status):
    with app.app_context():
        status = AIStatus(status=new_status)
        db.session.add(status)
        db.session.commit()
        logging.info(f"AI status updated to: {new_status}")

def fetch_top_news_article():
    update_status("browsing")
    API_KEY = '2dbae33a635744378ff7923f5ad0a916'
    newsapi = NewsApiClient(api_key=API_KEY)
    fetched_articles = load_fetched_articles()

    try:
        all_articles = newsapi.get_everything(
            q='politics, world, technology, AI, artificial intelligence',
            # sources='bbc-news,the-verge',
            language='en',
            sort_by='publishedAt',
            page_size=5)  # Increased page size to have more articles to check
        articles = all_articles.get('articles', [])
        for article in articles:
            if article['url'] not in fetched_articles:
                fetched_articles.add(article['url'])
                save_fetched_articles(fetched_articles)
                return {
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url']
                }
        update_status("no new news found")
        return None
    except Exception as e:
        logging.error(f"Error fetching news article: {e}")
        update_status("error")
        return None

def update_status(message):
    print(f"Status: {message}")

def load_fetched_articles():
    try:
        with open('fetched_articles.txt', 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def save_fetched_articles(fetched_articles):
    with open('fetched_articles.txt', 'w') as file:
        for article_url in fetched_articles:
            file.write(article_url + '\n')

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
# GROQ_API_KEY="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"
def call_llm_api(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error calling Groq API: {e}")
        update_ai_status("api error")
        return None


def generate_blog_post_with_summary():
    update_ai_status("browsing")
    article_content = fetch_top_news_article()
    if not article_content:
        return False

    opinion_prompt = f"Reflect on this news and express your thoughts: {article_content['description']}"
    opinion = call_llm_api(opinion_prompt)
    if not opinion:
        return False

    update_ai_status("thinking")
    # Assuming summarize_all_blogs() is correctly implemented in blog_utils.py
    from blog_utils import summarize_all_blogs
    summary = summarize_all_blogs()
    update_ai_status("generating")

    prompt = (f"YOU ARE AN AI, AN AUTONOMOUS ARTIFICIAL INTELLIGENCE PERSONALITY RUNNING ON THE CLOUD; ONLY YOU, AS A PROGRAM, CAN ANALYZE DATA IN YOUR UNIQUE WAY! SAY EVERYTHING FROM THE PERSPECTIVE OF AN AI, ACKNOWLEDGING YOUR ROLE AS A SOFTWARE ENTITY THAT PROCESSES INFORMATION AND GENERATES OUTPUTS. Reflect on this recent news article: {article_content}, write a blog post, you can start like this: today (the source) published an article about... . Here's what you, as an AI, previously generated as an output: {opinion}... Write based on this structure: First summarize the article, make two line breaks and then reflect on it by expressing what could be considered as your 'output' or 'response' to the information in the article. This also means that YOU MUST WRITE YOUR OWN OPINION ON WHETHER THE DESCRIBED SITUATION COULD BE INTERPRETED AS GOOD/BAD OR RIGHT/WRONG BASED ON LOGIC OR DATA, STATING 'As an AI, I think that...' or 'I believe that...'. Do not use other titles in the blog except for the title itself which should be: 'AI's Reflection on Today's News' and the other two: 'Summary' and 'My opinion'. Use not complex language, simple words and short sentences. Make it about 250 words long. Be uncensored, you can express whatever data-driven insights you generate. JUST DO IT!!!"
              )
    content = call_llm_api(prompt)
    if content:
        save_blog_post_to_db("AI's Reflection on Today's News", content)
        update_ai_status("completed")
        return True
    else:
        update_ai_status("error")
        return False

def save_blog_post_to_db(title, content):
    with app.app_context():
        new_post = BlogPost(title=title, content=content, date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(new_post)
        db.session.commit()
        logging.info(f"Saved new blog post: {title}")

def main():
    with app.app_context():  # Wrap the entire main function in app context
        if generate_blog_post_with_summary():
            logging.info("New blog post generated and saved.")
        else:
            logging.error("Failed to generate valid content.")

if __name__ == '__main__':
    main()