from flask import Flask, jsonify, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from model import db, BlogPost
from validations import blog_post_create_schema, blog_post_update_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Health check API
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connectivity
        post_count = BlogPost.query.count()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected',
            'post_count': post_count,
            'message': 'Flask REST API is running successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'disconnected',
            'error': str(e),
            'message': 'Flask REST API is experiencing issues'
        }), 503

# Create a new blog post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json() or {}
    errors = blog_post_create_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    new_post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully!', 'id': new_post.id}), 201

# Get all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    output = []
    for post in posts:
        post_data = {'id': post.id, 'title': post.title, 'content': post.content}
        output.append(post_data)
    return jsonify(output)

# Get a single blog post by ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        post_data = {'id': post.id, 'title': post.title, 'content': post.content}
        return jsonify(post_data)
    return jsonify({'message': 'Post not found!'}), 404

# Update a blog post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json() or {}
    errors = blog_post_update_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    post = BlogPost.query.get(post_id)
    if post:
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
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