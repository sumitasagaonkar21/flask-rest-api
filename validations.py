from marshmallow import Schema, fields, validate


class BlogPostCreateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)


class BlogPostUpdateSchema(Schema):
    title = fields.Str()
    content = fields.Str()


class ArticleCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    link = fields.Url(required=True, validate=validate.Length(max=500))
    tags = fields.Str(required=False)


class ArticleUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(min=1))
    link = fields.Url(validate=validate.Length(max=500))
    tags = fields.Str()


blog_post_create_schema = BlogPostCreateSchema()
blog_post_update_schema = BlogPostUpdateSchema()
article_create_schema = ArticleCreateSchema()
article_update_schema = ArticleUpdateSchema()
