from datetime import date
from typing import Annotated

from annotated_types import MaxLen

from orbify_projects.schemas.base import BaseModel, IntId
from orbify_projects.schemas.geojson import Feature


class CreateOrUpdateProject(BaseModel):
    name: Annotated[str, MaxLen(max_length=32)]
    description: str | None = None
    start_date: date
    end_date: date
    area_of_interest: Feature


class Project(CreateOrUpdateProject, IntId):
    pass


class PartialUpdateProject(BaseModel):
    name: Annotated[str, MaxLen(max_length=32)] | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    area_of_interest: Feature | None = None
