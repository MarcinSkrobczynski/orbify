from typing import Literal

from geojson_pydantic.geometries import Geometry
from pydantic import BaseModel


class Feature(BaseModel):
    type: Literal["Feature"]
    geometry: Geometry
