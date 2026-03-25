from marshmallow import Schema, fields

class BlogPostCreateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)

class BlogPostUpdateSchema(Schema):
    title = fields.Str()
    content = fields.Str()

blog_post_create_schema = BlogPostCreateSchema()
blog_post_update_schema = BlogPostUpdateSchema()
