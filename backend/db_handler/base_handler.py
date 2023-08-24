from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


class BaseDBHandler:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: Any):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_column(self, db: Session, column_name: str, value: Any):
        # Dynamically access the column attribute using getattr
        column = getattr(self.model, column_name)
        return db.query(self.model).filter(column == value).first()

    def get_multi(self, db: Session, *, offset: int = 0, limit: int = 100):
        return db.query(self.model).offset(offset).limit(limit).all()

    def create(self, db: Session, *, obj_in):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj, obj_in):
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int):
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
