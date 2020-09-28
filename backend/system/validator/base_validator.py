from pydantic import BaseModel
from typing import Sequence, Set, Any


class BaseValidator(BaseModel):

    exclude_fields: Set[str] = set()

    def dict(
        self,
        *,
        include: Sequence = None,
        exclude: Sequence = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ):
        exclude_set = self.exclude_fields.copy()
        exclude_set.update({'exclude_fields', })
        if exclude:
            exclude_set.update(exclude)
        return super().dict(
            include=include,
            exclude=exclude_set,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )

    class Config:
        orm_mode = True
