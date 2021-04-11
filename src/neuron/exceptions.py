class NeuronException(Exception):
    """ Base Exception for all exceptions of this module. """
    pass


class ServiceNotRegistered(NeuronException):
    def __init__(self, name, registry):
        if registry.keys():
            msg = '%s not registered, you have registered: %s' % (name,
                                                                  list(registry.keys()))
        else:
            msg = '%s not registered (registry is empty)' % name

        super(ServiceNotRegistered, self).__init__(msg)


class ValidationError(NeuronException):
    pass
