desc = 'The API to the GPT4All Datalake'

endpoint_paths = {'health': '/health'}


class ErrorStrings:
    ERROR = 'Internal server error..'
    UNAVAILABLE = 'Unavailable..'


error_responses = {
    500: {
        'description': 'Server Error',
        'content': {'application/json': {'example': {'detail': ErrorStrings.ERROR}}},
    },
    400: {
        'description': 'Bad Request',
        'content': {'application/json': {'example': {'detail': 'Bad Request'}}},
    },
    401: {
        'description': 'Unauthorized',
        'content': {'application/json': {'example': {'detail': 'Not authenticated'}}},
    },
    409: {
        'description': 'Conflict',
        'content': {'application/json': {'example': {'detail': 'Conflict in resource creation/modification.'}}},
    },
}
