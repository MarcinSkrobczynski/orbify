from typing import Any, Generic, TypeVar

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from orbify_projects.db.base import Base
from orbify_projects.schemas.base import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
PartialUpdateSchemaType = TypeVar("PartialUpdateSchemaType", bound=BaseModel)


class Crud(Generic[ModelType, CreateSchemaType, UpdateSchemaType, PartialUpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def create(self, obj_in: CreateSchemaType, *, session: Session) -> ModelType:
        json_data = jsonable_encoder(obj_in)

        if session.bind and session.bind.dialect.name == "sqlite":  # for testing purposes
            json_data = obj_in.model_dump(exclude_unset=True)

        db_obj: ModelType = self.model(**json_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj

    def _get_or_404(self, obj_id: int, *, session: Session) -> ModelType:
        db_obj: ModelType | None = session.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found")

        return db_obj

    def get(self, obj_id: Any, *, session: Session) -> ModelType:
        return self._get_or_404(obj_id, session=session)

    def get_multi(self, *, session: Session, skip: int = 0, limit: int = 50) -> list[ModelType]:
        return session.query(self.model).offset(skip).limit(limit).all()

    def _update(
        self, obj_id: Any, obj_in: UpdateSchemaType | PartialUpdateSchemaType | dict[str, Any], *, session: Session
    ) -> ModelType:
        db_obj: ModelType = self._get_or_404(obj_id, session=session)
        json_data = jsonable_encoder(db_obj)
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)

        for field in json_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(self, obj_id: Any, obj_in: UpdateSchemaType, *, session: Session) -> ModelType:
        return self._update(obj_id, obj_in, session=session)

    def partial_update(self, obj_id: Any, obj_in: PartialUpdateSchemaType, *, session: Session) -> ModelType:
        return self._update(obj_id, obj_in, session=session)

    def delete(self, obj_id: Any, *, session: Session) -> None:
        db_obj: ModelType = self._get_or_404(obj_id, session=session)
        session.delete(db_obj)
        session.commit()
