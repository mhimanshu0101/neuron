from rest_framework.exceptions import APIException

from .exceptions import ValidationError


class BaseService(object):
    is_global = False

    def __init__(self, **kwargs):
        self.request = kwargs['request']
        self.validated_data = {}
        super(BaseService, self).__init__()

    def validate(self, **kwargs):
        return True

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def dispatch(self):
        """
            This is wrapper method that will execute other methods in sequence
        """
        try:
            if not self.validate():
                raise ValidationError('Validation error in service')
            return self.run()
        except Exception as exc:
            if issubclass(exc.__class__, APIException):
                return {'detail': exc.detail, 'status_code': exc.status_code}
            raise
