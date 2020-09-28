from .base_context import BaseContext
from backend.system.db import get_session
from sqlalchemy.orm import Session


class GlobalContext(BaseContext):
    initial_data = {
        'session': get_session(),
    }

    @property
    def session(self) -> Session:
        return self.get('session')
