This project is designed let an Ai analyse and reflect on the latest news. 

## Description

The application consists of several components that work together to fetch, analyze, and summarize news articles. The `generate_blog.py` script processes articles to create blog posts, while the `generate_sum.py` script provides summaries of articles for quick reading.

## Getting Started

### Dependencies

- Python 3.x
- Flask
- Other dependencies at `requirements.txt`
- You need Ollama to be installed

### Installing

- Clone the repository: https://github.com/Venomena/AIs_opinion_on_the_news/
- Install the required dependencies:
  pip install -r requirements.txt
- run "ollama run llama3:8b"
  this will install the model.
- run "ollama serve"
  this starts the local API access to ollama. 

Run with ./run.sh
