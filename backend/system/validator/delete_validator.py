from .base_validator import BaseValidator


class DeleteValidator(BaseValidator):
    id: int
    hard_delete: bool = False
    stop_at_fail: bool = False
