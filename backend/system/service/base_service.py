from backend.system.dao import BaseDao
from backend.system.model import BaseModel
from typing import ClassVar, Tuple, List, Dict, Any
from backend.system.validator.delete_validator import DeleteValidator


class BaseService(object):
    dao_cls: ClassVar = BaseDao

    def __init__(self):
        self._dao = self.dao_cls()

    @property
    def dao(self):
        return self._dao

    def get(self, key: int):
        return self._dao.get(key)

    def paginate(self, skip: int=0, limit: int=25) -> Tuple[List[BaseModel], int]:
        # TODO: apply filters
        return self.dao.paginate(skip=skip, limit=limit), self.dao.count()

    def before_write(self, data: dict):
        return data

    def after_write(self, model: BaseModel):
        return model

    def create(self, data: Dict[str, Any], commit: bool=True):
        data = self.before_write(data)
        model = self.dao.save(data=data, commit=commit)
        model = self.after_write(model)
        return model

    def update(self, data: Dict[str, Any], commit: bool=True):
        data = self.before_write(data)
        model = self.dao.update(data=data, commit=commit)
        model = self.after_write(model)
        return model

    def delete(self, data: DeleteValidator, commit: bool=True):
        self.dao.delete(data=data, commit=commit)
