from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import time
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AIStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)

    @staticmethod
    def get_current_status():
        status_record = AIStatus.query.order_by(AIStatus.id.desc()).first()
        return status_record.status if status_record else "unknown"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=True)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()
    if not AIStatus.query.first():
        initial_status = AIStatus(status="thinking")
        db.session.add(initial_status)
        db.session.commit()

@app.route('/ai-status', methods=['GET'])
@cross_origin()
def get_ai_status():
    current_status = AIStatus.get_current_status()
    print(f"Sending status: {current_status}")  # Adding a log for debugging
    return jsonify(status=current_status)


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    if request.method == 'POST':
        comment_content = request.form['comment']
        comment = Comment(content=comment_content)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('home'))
    comments = Comment.query.all()
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
    source_urls = get_source_urls()  # Get source URLs from the file
    zipped_data = zip(blog_posts, source_urls)
    return render_template('index.html', data=zipped_data)


def bold_text(text):
    # This function uses regular expressions to replace **text** with <strong>text</strong>
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

app.jinja_env.filters['bold'] = bold_text

def get_source_urls():
    with open("fetched_articles.txt", "r") as file:
        return file.readlines()  # This returns a list of all URLs

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['POST'])
@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    new_message = ContactMessage(name=name, email=email, message=message)
    db.session.add(new_message)
    db.session.commit()
    return "Thank you for your message!"

@app.route('/submit-comment', methods=['POST'])
@cross_origin()
def submit_comment():
    comment_content = request.form.get('comment')
    if comment_content:
        comment = Comment(content=comment_content)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/blog')
@cross_origin()
def blog_list():
    posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
    return render_template('blog_list.html', posts=posts)

@app.route('/blog/<int:post_id>')
@cross_origin()
def blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)