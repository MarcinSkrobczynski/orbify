from fastapi import APIRouter, status

from orbify_projects.api.dependencies import SessionDep
from orbify_projects.db.crud import Crud
from orbify_projects.models import Project as ProjectModel
from orbify_projects.schemas.projects import CreateOrUpdateProject, PartialUpdateProject, Project

project_router = APIRouter(prefix="/projects", tags=["projects"])


class CrudProject(Crud[ProjectModel, CreateOrUpdateProject, CreateOrUpdateProject, PartialUpdateProject]):
    pass


project_crud = CrudProject(ProjectModel)


@project_router.post("", status_code=status.HTTP_201_CREATED, response_model=Project)
def create(data: CreateOrUpdateProject, session: SessionDep) -> Project:
    return project_crud.create(data, session=session)


@project_router.get("/{project_id}", status_code=status.HTTP_200_OK, response_model=Project)
def get(project_id: int, session: SessionDep) -> Project:
    return project_crud.get(project_id, session=session)


@project_router.get("", status_code=status.HTTP_200_OK, response_model=list[Project])
def get_multi(session: SessionDep, skip: int = 0, limit: int = 50) -> list[Project]:
    return project_crud.get_multi(session=session, skip=skip, limit=limit)


@project_router.put("/{project_id}", status_code=status.HTTP_200_OK, response_model=Project)
def update(project_id: int, data: CreateOrUpdateProject, session: SessionDep) -> Project:
    return project_crud.update(project_id, data, session=session)


@project_router.patch("/{project_id}", status_code=status.HTTP_200_OK, response_model=Project)
def partial_update(project_id: int, data: PartialUpdateProject, session: SessionDep) -> Project:
    return project_crud.partial_update(project_id, data, session=session)


@project_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(project_id: int, session: SessionDep) -> None:
    project_crud.delete(project_id, session=session)
