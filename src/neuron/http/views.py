import logging
import re
from uuid import UUID, uuid1

from django.conf import settings
from django.http.request import QueryDict
from rest_framework.exceptions import (APIException, PermissionDenied, NotAuthenticated)
from rest_framework.views import APIView

from neuron.exceptions import ServiceNotRegistered, ValidationError
from neuron.exceptions import ValidationError as NeuronValidationError
from neuron.mixins import GetRegistryMixin


API_KEYS_REGEX_LIST = [
    re.compile(
        r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z',
        flags=re.I
    ),
    re.compile(r'[a-fA-z0-9]{32}\Z', flags=re.I)
]

LOGGER = logging.getLogger(__name__)


class ApiView(GetRegistryMixin, APIView):
    """
    Simple view that routes the request to its dedicated service.
    """
    message = 'Send the correct API keys to access the endpoints.'
    api_key_message = 'Send a valid API key to access the endpoints.'
    api_secret_key_message = 'Send a valid API secret key to access the endpoints.'

    def app(self, request, api_obj=None):
        """
        Binding `app` as property to request object. So that we can access it later from it.
        """
        request.app = property(lambda self: api_obj)
        return setattr(request, 'app', api_obj)

    def app_permission_denied(self, request, message=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if not request.successful_authenticator and not message:
            raise NotAuthenticated()
        if message:
            raise PermissionDenied(detail=message)
        raise PermissionDenied(detail=message)

    def _validate_api_key(self, api_key):
        """
        Check if the api_key passed by client is valid format or not.
        """
        try:
            uuid_hex = UUID(api_key)
            regex = API_KEYS_REGEX_LIST[0]
            # re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z',
            # re.IGNORECASE|re.UNICODE)
            success = regex.search(api_key)
            if not success:
                return False
            elif uuid_hex or success:
                return True
        except ValueError:
            return False

    def _validate_api_secret_key(self, api_secret_key):
        """
        Check if the api_secret_key is in a valid UUID format or not.
        """
        regex = API_KEYS_REGEX_LIST[1]
        # regex = re.compile(r'[a-fA-z0-9]{32}\Z', re.IGNORECASE|re.UNICODE)
        success = regex.search(api_secret_key)
        if not success:
            return False
        return True

   
