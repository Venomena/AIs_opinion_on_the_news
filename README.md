# AI's Opinion on the News

This project is designed to let an AI analyze and reflect on the latest news.

## Description

The application consists of several components that work together to fetch, analyze, and summarize news articles. The `blog_utils.py` and `generate_blog.py` scripts process articles to create insightful blog posts that offer reflections on current events. Additionally, the `generate_sum.py` script provides concise summaries of articles for quick consumption.

## Getting Started

### Dependencies

- Python 3.x
- Flask
- Requests
- Groq API client
- See all dependencies in `requirements.txt`

### Installing

1. **Clone the repository:**
```
git clone https://github.com/Venomena/AIs_opinion_on_the_news/
```

3. **Environment Setup:**
- Set up the Groq API key as an environment variable to enhance security and ease of use:
  ```bash
  export GROQ_API_KEY=<your-api-key-here>
  ```

4. **Install the Groq Python library:**
```
pip install groq
```
This script fetches the latest news, analyzes it using the Groq API, and generates a blog post with both a summary and an AI's reflection on the content.

### Additional Information

- Ensure your Groq API key is correctly set in your environment variables to authenticate API requests.
- The application uses environment variables to manage API keys securely, preventing sensitive data from being hard-coded into the source code.
