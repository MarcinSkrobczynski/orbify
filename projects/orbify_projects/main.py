from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from orbify_projects.core.config import settings


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        version=settings.version,
        debug=settings.debug,
        openapi_url=f"{settings.api_prefix}/openapi.json",
        redoc_url=None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_settings.allow_origins or ["*"],
        allow_credentials=settings.cors_settings.allow_credentials,
        allow_methods=settings.cors_settings.allow_methods or ["*"],
        allow_headers=settings.cors_settings.allow_headers or ["*"],
        max_age=settings.cors_settings.max_age,
    )

    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config="core/logging_config.yaml")
