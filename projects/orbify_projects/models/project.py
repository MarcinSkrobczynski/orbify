from datetime import date

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from orbify_projects.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    area_of_interest: Mapped[dict] = mapped_column(JSON, nullable=False)
