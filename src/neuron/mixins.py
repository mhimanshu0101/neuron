class GetRegistryMixin(object):
    def get_registry(self):
        if getattr(self, '_registry', None) is None:
            from neuron.registry import registry
            self._registry = registry
        return self._registry
