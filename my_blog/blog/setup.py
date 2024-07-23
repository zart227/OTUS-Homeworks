from blog.models import User, Post, Tag, session

def setup_data():
    user1 = User(username='alice')
    user2 = User(username='bob')

    tag1 = Tag(name='Python')
    tag2 = Tag(name='Django')
    tag3 = Tag(name='Flask')
    tag4 = Tag(name='SQLAlchemy')

    post1 = Post(title='Introduction to Python', content='Content about Python', author=user1, tags=[tag1])
    post2 = Post(title='Web Development with Django', content='Content about Django', author=user1, tags=[tag2])
    post3 = Post(title='Building APIs with Flask', content='Content about Flask', author=user2, tags=[tag3])
    post4 = Post(title='ORM with SQLAlchemy', content='Content about SQLAlchemy', author=user2, tags=[tag1, tag4])

    session.add_all([user1, user2, tag1, tag2, tag3, tag4, post1, post2, post3, post4])
    session.commit()

if __name__ == '__main__':
    setup_data()
