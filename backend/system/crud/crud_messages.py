class CrudMessageKeys:
    NOT_FOUND = 'crud.not_found',
    OPERATION_NOT_ALLOWED = 'crud.operation_not_allowed'
    DELETE_SUCCESS = 'crud.delete_success'


crud_default_vocabulary = {
    'model': 'model'
}

crud_messages = {
    CrudMessageKeys.NOT_FOUND: '{model} not found',
    CrudMessageKeys.OPERATION_NOT_ALLOWED: 'Operation not allowed',
    CrudMessageKeys.DELETE_SUCCESS: '{model} deleted successfully',
}
