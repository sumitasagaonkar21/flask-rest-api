from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from model import db, BlogPost

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Create a new blog post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully!'}), 201

# Get all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    output = []
    for post in posts:
        post_data = {'id': post.id, 'title': post.title, 'content': post.content}
        output.append(post_data)
    return jsonify(output)

# Update a blog post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = BlogPost.query.get(post_id)
    if post:
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        return jsonify({'message': 'Post updated successfully!'}), 200
    return jsonify({'message': 'Post not found!'}), 404

# Delete a blog post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully!'}), 200
    return jsonify({'message': 'Post not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
