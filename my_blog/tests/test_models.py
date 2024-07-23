from blog.models import session, User, Post, Tag

def test_user_creation(setup_database):
    user = session.query(User).filter_by(username='alice').first()
    assert user is not None

def test_post_creation(setup_database):
    post = session.query(Post).filter_by(title='Introduction to Python').first()
    assert post is not None

def test_tag_creation(setup_database):
    tag = session.query(Tag).filter_by(name='Python').first()
    assert tag is not None
