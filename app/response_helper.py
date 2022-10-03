from fastapi.responses import JSONResponse


def create_response(error, data, message, status_code):
    res = JSONResponse(
        content=
        {
            'error': error,
            'message': message,
            'data': data
        }
    )
    res.status_code = status_code
    return res
