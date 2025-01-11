from fastapi import APIRouter, status

from orbify_projects.schemas.health import HealthCheck

health_router = APIRouter()


@health_router.get(
    "/health",
    tags=["healthcheck"],
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")
