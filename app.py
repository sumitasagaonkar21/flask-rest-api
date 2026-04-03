from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from model import db, BlogPost, Article
from validations import (
    blog_post_create_schema,
    blog_post_update_schema,
    article_create_schema,
    article_update_schema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# Create a new blog post
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json() or {}
    errors = blog_post_create_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    new_post = BlogPost(title=data["title"], content=data["content"])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully!", "id": new_post.id}), 201


# Get all blog posts
@app.route("/posts", methods=["GET"])
def get_posts():
    posts = BlogPost.query.all()
    output = []
    for post in posts:
        post_data = {"id": post.id, "title": post.title, "content": post.content}
        output.append(post_data)
    return jsonify(output)


# Update a blog post
@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json() or {}
    errors = blog_post_update_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    post = BlogPost.query.get(post_id)
    if post:
        if "title" in data:
            post.title = data["title"]
        if "content" in data:
            post.content = data["content"]
        db.session.commit()
        return jsonify({"message": "Post updated successfully!"}), 200
    return jsonify({"message": "Post not found!"}), 404


# Delete a blog post
@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted successfully!"}), 200
    return jsonify({"message": "Post not found!"}), 404


# Create a new article
@app.route("/articles", methods=["POST"])
def create_article():
    data = request.get_json() or {}
    errors = article_create_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    new_article = Article(
        name=data["name"],
        description=data["description"],
        link=data["link"],
        tags=data.get("tags", ""),
    )
    db.session.add(new_article)
    db.session.commit()
    return (
        jsonify({"message": "Article created successfully!", "id": new_article.id}),
        201,
    )


# Get all articles
@app.route("/articles", methods=["GET"])
def get_articles():
    articles = Article.query.all()
    output = []
    for article in articles:
        article_data = {
            "id": article.id,
            "name": article.name,
            "description": article.description,
            "link": article.link,
            "tags": article.tags,
        }
        output.append(article_data)
    return jsonify(output)


# Get a single article by ID
@app.route("/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    article = Article.query.get(article_id)
    if article:
        article_data = {
            "id": article.id,
            "name": article.name,
            "description": article.description,
            "link": article.link,
            "tags": article.tags,
        }
        return jsonify(article_data), 200
    return jsonify({"message": "Article not found!"}), 404


# Update an article
@app.route("/articles/<int:article_id>", methods=["PUT"])
def update_article(article_id):
    data = request.get_json() or {}
    errors = article_update_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    article = Article.query.get(article_id)
    if article:
        if "name" in data:
            article.name = data["name"]
        if "description" in data:
            article.description = data["description"]
        if "link" in data:
            article.link = data["link"]
        if "tags" in data:
            article.tags = data["tags"]
        db.session.commit()
        return jsonify({"message": "Article updated successfully!"}), 200
    return jsonify({"message": "Article not found!"}), 404


# Delete an article
@app.route("/articles/<int:article_id>", methods=["DELETE"])
def delete_article(article_id):
    article = Article.query.get(article_id)
    if article:
        db.session.delete(article)
        db.session.commit()
        return jsonify({"message": "Article deleted successfully!"}), 200
    return jsonify({"message": "Article not found!"}), 404


if __name__ == "__main__":
    app.run(debug=True)
