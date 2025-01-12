from fastapi import FastAPI

from orbify_projects.main import create_application


def test_create_application():
    fastapi = create_application()
    assert isinstance(fastapi, FastAPI)
    assert fastapi.user_middleware != []
