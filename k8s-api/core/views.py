import logging

from django.conf import settings
from django.db import connections, OperationalError
from rest_framework import decorators, permissions
from rest_framework.response import Response

from .exceptions import ServiceUnavailable
from .services import Async


logger = logging.getLogger(__name__)


@decorators.api_view()
@decorators.permission_classes([permissions.AllowAny])
def alive(_) -> Response:
    if not Async.alive():
        raise ServiceUnavailable('Service `async` dead.')

    for key in settings.DATABASES:
        try:
            connections[key].cursor()
        except OperationalError:
            message = f'Database `{key}` dead.'
            logger.exception(message)

            raise ServiceUnavailable(message)

    return Response(status=204)
