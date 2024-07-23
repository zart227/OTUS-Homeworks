from blog.models import session, Post, Tag

def get_posts_by_user_with_tags(user_id, tag_names):
    posts = session.query(Post).join(Post.tags).filter(
        Post.author_id == user_id,
        Tag.name.in_(tag_names)
    ).all()
    return posts
