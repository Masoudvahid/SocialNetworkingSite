import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

# Load environment variables from .env file
load_dotenv()

# Access environment variables
db_hostname = os.environ.get('POSTGRES_HOSTNAME')
db_username = os.environ.get('POSTGRES_USERNAME')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_port = os.environ.get('POSTGRES_PORT')
db_name = os.environ.get('DB_NAME')
print(db_hostname, db_username, db_password, db_port, db_name)
database_uri = f'postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}'

engine = create_engine(database_uri, echo=True)
Base = declarative_base()

if database_exists(engine.url):
    # Drop all tables
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
else:
    create_database(engine.url)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    phone = Column(String(16), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(40), nullable=False)
    first_name = Column(String(20), nullable=False, default='')
    last_name = Column(String(20), nullable=False, default='')
    blocked = Column(Boolean, nullable=False, default=False)
    bio = Column(Text, nullable=False, default='')
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    business_account = Column(Boolean, nullable=False)


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    message = Column(String(255), nullable=False, default='')
    created_at = Column(DateTime, nullable=False)
    promoted_post = Column(Integer, nullable=True)


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    message = Column(String(255), nullable=False, default='')
    created_at = Column(DateTime, nullable=False)


class Friends(Base):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    friend_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime, nullable=False)


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String(255), nullable=False, default='')
    created_at = Column(DateTime, nullable=False)


class FriendshipRequests(Base):
    __tablename__ = 'friendship_requests'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    receiver_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


# Create metadata
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Use the session factory to create a new session
session = Session()
