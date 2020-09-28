from backend.system.service import BaseService
from backend.system.validator import BaseValidator
from backend.system.validator.delete_validator import DeleteValidator
from backend.system.message_generator import get_message
from .crud_messages import CrudMessageKeys
from typing import ClassVar, Dict, Type, Tuple, List, Any
from fastapi import Request, APIRouter, HTTPException
from fastapi.exceptions import RequestValidationError
from cached_property import cached_property
from urllib.parse import urlencode
from pydantic import ValidationError
from backend.system.dao.exception import DaoNotFoundException, DaoOperationNotAllowedException


class BaseCrud(object):

    service_cls: ClassVar = BaseService

    create_validator: Type[BaseValidator] = BaseValidator
    read_validator: Type[BaseValidator] = BaseValidator
    update_validator: Type[BaseValidator] = BaseValidator

    default_vocabulary = {

    }

    def __init__(self):
        self._service: BaseService = self.service_cls()

    @cached_property
    def vocabulary(self) -> Dict[str, str]:
        ret = dict()
        if hasattr(super(), 'vocabulary'):
            ret.update(super().vocabulary)
        ret.update(self.default_vocabulary)
        return ret

    @cached_property
    def service(self) -> service_cls:
        return self._service

    def read(self, model_id: int):
        validator = self.read_validator
        model = self.service.get(model_id)
        if model is None:
            raise HTTPException(
                status_code=404,
                detail=get_message(CrudMessageKeys.NOT_FOUND, self.vocabulary),
            )
        return validator.from_orm(model)

    def read_endpoint(self, *, request: Request, model_id: int):
        response_data = self.read(model_id)
        return response_data

    def index(self, page: int, limit: int) -> Tuple[List, int]:
        # TODO: apply filters
        skip = page-1
        models, count = self.service.paginate(skip=skip, limit=limit)
        data_set = [self.read_validator.from_orm(model) for model in models]
        return data_set, count

    def index_endpoint(self, *, request: Request, page: int=1, limit: int=25):
        data, total = self.index(page=page, limit=limit)
        url = request.url.components.geturl().split('?')[0]
        next_page = None
        prev_page = None
        if page * limit < total:
            next_page = url + '?' + urlencode({
                'page': page + 1,
                'limit': limit
            })
        if data and page != 1:
            prev_page = url + '?' + urlencode({
                'page': page - 1,
                'limit': limit
            })
        response_data = {
            "page": page,
            "limit": limit,
            "total": total,
            "data": data,
            "prev": prev_page,
            "next": next_page,
        }
        return response_data

    def create(self, data: Dict[str, Any]):
        model = self.service.create(data=data, commit=True)
        return model

    def create_endpoint(self, *, request: Request, data: Dict[str, Any]):
        try:
            validated_data = self.create_validator.validate(data).dict()
            model = self.create(data=validated_data)
        except ValidationError as e:
            raise RequestValidationError(errors=e.raw_errors, body=data)
        return self.read_validator.from_orm(model)

    def update(self, data: Dict[str, Any]):
        model = self.service.update(data=data, commit=True)
        return model

    def update_endpoint(self, *, request: Request, data: Dict[str, Any]):
        try:
            validated_data = self.update_validator.validate(data).dict()
            model = self.update(data=validated_data)
        except ValidationError as e:
            raise RequestValidationError(errors=e.raw_errors, body=data)
        except DaoNotFoundException as e:
            raise HTTPException(
                status_code=404,
                detail=get_message(CrudMessageKeys.NOT_FOUND, self.vocabulary),
            )
        return self.read_validator.from_orm(model)

    def delete(self, data: DeleteValidator):
        self.service.delete(data=data, commit=True)

    def delete_endpoint(self, *, request: Request, data: DeleteValidator):
        try:
            self.delete(data)
        except DaoOperationNotAllowedException as e:
            raise HTTPException(
                status_code=403,
                detail=get_message(CrudMessageKeys.OPERATION_NOT_ALLOWED, self.vocabulary),
            )
        except DaoNotFoundException as e:
            raise HTTPException(
                status_code=404,
                detail=get_message(CrudMessageKeys.NOT_FOUND, self.vocabulary),
            )
        return {
            "message": get_message(CrudMessageKeys.DELETE_SUCCESS, self.vocabulary),
            "id": data.id,
        }

    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.get('/{model_id}')(self.read_endpoint)
        router.get('/')(self.index_endpoint)
        router.post('/')(self.create_endpoint)
        router.put('/')(self.update_endpoint)
        router.delete('/')(self.delete_endpoint)
        return router





