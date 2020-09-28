from backend.system.db import Base
from sqlalchemy import Column, Integer, Boolean
from typing import Dict, Any


class BaseModel(Base):

    __abstract__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    deleted: bool = Column(Boolean, default=False, server_default='False')

    def update_from_dict(self, data: Dict[str, Any]) -> 'BaseModel':
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
