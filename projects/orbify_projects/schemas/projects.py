from datetime import date
from typing import Annotated, Self

from annotated_types import Len
from pydantic import model_validator

from orbify_projects.schemas.base import BaseModel, IntId
from orbify_projects.schemas.geojson import Feature


class CreateOrUpdateProject(BaseModel):
    name: Annotated[str, Len(1, 32)]
    description: str | None = None
    start_date: date
    end_date: date
    area_of_interest: Feature

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before end date.")
        return self


class Project(CreateOrUpdateProject, IntId):
    pass


class PartialUpdateProject(BaseModel):
    name: Annotated[str, Len(1, 32)] | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    area_of_interest: Feature | None = None
