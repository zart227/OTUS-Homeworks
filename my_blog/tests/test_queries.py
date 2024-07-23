import pytest
from blog.queries import get_posts_by_user_with_tags
from blog.models import session, User, Tag

def test_get_posts_by_user_with_tags(setup_database):
    user = session.query(User).filter_by(username='alice').first()
    posts = get_posts_by_user_with_tags(user_id=user.id, tag_names=['Python', 'Django'])
    assert len(posts) == 2
    assert all(tag.name in ['Python', 'Django'] for post in posts for tag in post.tags)
