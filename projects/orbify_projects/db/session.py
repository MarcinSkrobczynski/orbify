from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orbify_projects.core.config import settings

engine = create_engine(settings.database_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
