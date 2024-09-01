from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# Инициализация базы данных
Base = declarative_base()
engine = create_engine('sqlite:///blog.db')

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Таблица для связи постов и тегов (многие ко многим)
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

# Модель пользователя
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    posts = relationship('Post', back_populates='author')
    
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)   

# Модель поста
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    tags = relationship('Tag', secondary=post_tags, back_populates='posts')
    author = relationship('User', back_populates='posts')

# Модель тега
class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    posts = relationship('Post', secondary=post_tags, back_populates='tags')

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Инициализация контекста шифрования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
