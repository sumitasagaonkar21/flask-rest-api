from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<BlogPost {self.title}>"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Article {self.name}>"
