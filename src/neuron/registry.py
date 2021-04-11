import json
import requests
from .exceptions import ServiceNotRegistered


class NeuroRegistry(dict):
    """
    Creates realtime dictionary/registry in memory for all serives with dedicated namespace(as a key).
    i.e
    {
        'signup': SignUpService,
        'login': LoginService
    }
    """
    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', 'default')
        super(NeuroRegistry, self).__init__(self, *args, **kwargs)
        # super will call its parent dict class __init__ with multi inheritance.

    def __getitem__(self, name) -> _VT:
        """
        Returns the class registered for this name. If not return ServiceNotRegistered error.
        """
        try:
            super(NeuroRegistry, self).__getitem__(name)
        except KeyError:
            return ServiceNotRegistered(name, self)

    def register(self, *args, **kwargs):
        "Registers a service with given name."
        service = kwargs.get('service') # other service as client
        # service will be service classe instance ..SignUpService, LoginService
        name = kwargs.get('name', service.__name__) # get it from kwargs or from client service.
        
        print(f'Registered services: {name}')
        service = type(str(name), (service,), kwargs)
        self[service.__name__] = service
        
        return service

    def set_namespace(self, namespace):
        self.namespace = namespace

    def unregister(self, name):
        "Delete Service class from register dict object."
        del self[name]

    
registry = NeuroRegistry()