import logging
import re
from uuid import UUID, uuid1

from django.conf import settings
from django.http.request import QueryDict
from neuron.models import APIKey
from rest_framework.exceptions import (APIException, PermissionDenied, NotAuthenticated)
from rest_framework.views import APIView

from neuron.exceptions import ServiceNotRegistered, ValidationError
from neuron.exceptions import ValidationError as NeuronValidationError
from neuron.mixins import GetRegistryMixin
from neuron.http.response import response


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

    def check_api_keys(self, request):
        """
        Takes request object; checks if the API keys are present in the request or not.
        If valid API keys are present in the request then it provides access to the endpoint,
        otherwise, it rejects the request to access the endpoint.
        """
        api_key, api_obj = request.META.get('HTTP_API_KEY'), None
        api_secret_key = request.META.get('HTTP_SECRET_KEY')
        if api_key and api_secret_key:
            # validate the API and secret keys.
            api_key_bool = self._validate_api_key(api_key)
            if not api_key_bool:
                return False, self.api_key_message
            secret_key_bool = self._validate_api_secret_key(api_secret_key)
            if not secret_key_bool:
                return False, self.api_secret_key_message
            try:
                api_obj = APIKey.objects.get(
                    api_key=api_key,
                    api_secret_key=api_secret_key,
                    is_active=True,
                )
                if api_obj:
                    self.app(request, api_obj)
                    return True, ''
            except APIKey.DoesNotExist:
                self.app(request, api_obj)
                return False, self.message
        else:
            self.app(request, api_obj)
            return False, self.message

    def call_service(self, *args, **kwargs):
        "Fetch service class from registry and call it."
        try:
            service_class = self.get_registry()[kwargs['service']]
        except ServiceNotRegistered:
            return response.NotFound()

            # TODO - Complete this call_service with GlueRequest, 

    def initial(self, request, *args, **kwargs):
        "Runs anything that needs to occur prior to calling the method handler"
        bool_value, message =self.check_api_keys(request)
        if bool_value:
            super(APIView, self).initial(request, *args, **kwargs)
        else:
            self.app_permission_denied(request, message)

    def get(self, *args, **kwargs):
        return self.call_service(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.call_service(*args, **kwargs)


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

   
