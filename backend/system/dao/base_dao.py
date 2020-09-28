from backend.system.model import BaseModel
from backend.system.context import GlobalContext
from sqlalchemy.orm import Session, Query
from sqlalchemy import func
from typing import List, Type, Dict, Any, Union
from .exception import DaoNotFoundException, DaoOperationNotAllowedException
from backend.system.validator.delete_validator import DeleteValidator


class BaseDao(object):

    model_cls: Type[BaseModel] = BaseModel

    __ALLOW_HARD_DELETE__: bool = False

    def __init__(self):
        self._session: Session = GlobalContext.get_instance().session

    @property
    def session(self) -> Session:
        return self._session

    def get(self, pk: int, *, include_deleted: bool=False) -> model_cls:
        query = self.query()
        if not include_deleted:
            query = query.filter(self.model_cls.deleted == False)
        return query.filter(self.model_cls.id == pk).first()

    def all(self) -> List[model_cls]:
        return self.session.query(self.model_cls).all()

    def query(self, select: List=[]) -> Query:
        # TODO: implement filters
        if not select:
            select = [self.model_cls]
        return self.session.query(*select)

    def paginate(self, skip: int, limit: int, *, include_deleted: bool = False):
        # TODO: implement filters
        offset = skip * limit
        query = self.query()
        if not include_deleted:
            query = query.filter(self.model_cls.deleted == False)
        query = query.offset(offset).limit(limit)
        return query.all()

    def count(self, *, include_deleted: bool=False) -> int:
        # TODO: implement filters
        query = self.query([func.count(self.model_cls.id)])
        if not include_deleted:
            query = query.filter(self.model_cls.deleted == False)
        return query.scalar()

    def save(self, data: Dict[str, Any], commit: bool=True) -> model_cls:
        model = self.model_cls()
        model.update_from_dict(data=data)
        self._session.add(model)
        self._session.flush()
        if commit:
            self.session.commit()
        return model

    def update(self, data: Dict[str, Any], commit: bool=True):
        model_id = data.get('id')
        model = self.get(model_id)
        if not model:
            raise DaoNotFoundException()
        model.update_from_dict(data)
        self.session.flush()
        if commit:
            self.session.commit()
        return model

    def delete(self, data: DeleteValidator, commit: bool=True):
        model = self.get(data.id)
        if not model:
            raise DaoNotFoundException()
        if data.hard_delete:
            if self.__ALLOW_HARD_DELETE__:
                self._hard_delete(model=model, commit=commit)
            elif not data.stop_at_fail:
                self._soft_delete(model=model, commit=commit)
            else:
                raise DaoOperationNotAllowedException()
        else:
            self._soft_delete(model=model, commit=commit)

    def _hard_delete(self, model: model_cls, commit: bool):
        self.session.delete(model)
        self.session.flush()
        if commit:
            self.session.commit()

    def _soft_delete(self, model: model_cls, commit: bool):
        model.deleted = True
        self.session.flush()
        if commit:
            self.session.commit()





