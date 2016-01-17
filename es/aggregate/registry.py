

class AggregateRegistry:
    AggregateDoesNotExist = type('AggregateDoesNotExist', (LookupError,), {})

    def __init__(self):
        self.__aggregates = {}

    def register(self, cls):
        self.__aggregates[namespace][aggregate_name] = cls

    def get(self, aggregate_type):
        namespace, aggregate_name = aggregate_type.split('.')
        cls = self.__aggregates.get(namespace, {}).get(aggregate_name)
        if cls is None:
            raise self.AggregateDoesNotExist
        return cls


_registry = AggregateRegistry()
register = _registry.register
get = _registry.get


del AggregateRegistry
