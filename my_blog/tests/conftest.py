import pytest
from blog.models import engine, Base, session
from blog.setup import setup_data

@pytest.fixture(scope='module')
def setup_database():
    Base.metadata.create_all(engine)
    setup_data()
    yield session
    Base.metadata.drop_all(engine)
