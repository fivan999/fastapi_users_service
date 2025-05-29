class AppException(Exception):
    detail = "server error"
    status_code = 500
