from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from orbify_projects.db.session import SessionLocal


def get_session() -> Generator[Session, None, None]:
    """
    Helper dependency for getting DB session.
    """
    session: Session | None = None
    try:
        session = SessionLocal()
        yield session
    finally:
        if session is not None:
            session.close()


SessionDep = Annotated[Session, Depends(get_session)]
