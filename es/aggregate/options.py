from es.fields import Adapter


class AggregateOptions:

    def __init__(self, meta):
        self.meta = meta
        self.base_fields = {}
        self.adapter_class = None

    def add_field(self, name, field):
        """Adds a new field to the aggregate state."""
        self.base_fields[name] = field

    def is_valid_field(self, name):
        return name in self.base_fields

    def contribute_to_class(self, attname, cls):
        # Create the Adapter.
        self.adapter_class = type(
            cls.__name__ + 'Adapter', (Adapter,), self.base_fields)
        self.adapter = self.adapter_class()

        # Get the aggregate namespace and name from the Meta class,
        # or build it from the class module.
        self.aggregate_name = getattr(
            self.meta, 'aggregate_name', cls.__name__)
        self.namespace = getattr(self.meta, 'namespace', None)
        if self.namespace is None:
            self.namespace = cls.__module__.split('.')[-2]
        self.aggregate_type = "{0}:{1}".format(
            self.namespace, self.aggregate_name.lower())

        setattr(cls, attname, self)
