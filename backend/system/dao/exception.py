class DaoException(Exception):
    pass


class DaoNotFoundException(DaoException):
    pass


class DaoOperationNotAllowedException(DaoException):
    pass
