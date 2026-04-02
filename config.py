import os
from dotenv import load_dotenv

# Load environment variables from .env file (local development only)
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # Use SQLite for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    
class ProductionConfig(Config):
    """Production configuration (Railway)"""
    DEBUG = False
    # Railway provides DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url and database_url.startswith('postgres://'):
        # SQLAlchemy 1.4+ requires postgresql:// instead of postgres://
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}