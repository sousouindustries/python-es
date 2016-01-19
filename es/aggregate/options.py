from es.fields import Adapter


class AggregateOptions:

    def __init__(self, meta):
        self.meta = meta
        self.base_fields = {}
        self.fields = []
        self.adapter_class = None

    def dump(self, state):
        """Serializes the current state of the aggregate as a Python
        dictionary.
        """
        return self.adapter.dump(state._AggregateState__state)[0]

    def add_field(self, name, field):
        """Adds a new field to the aggregate state."""
        self.base_fields[name] = field
        self.fields.append(name)

    def is_valid_field(self, name):
        return name in self.fields

    def contribute_to_class(self, attname, cls):
        # Create the Adapter.
        assert self.base_fields, self.base_fields
        self.adapter_class = type(
            cls.__name__ + 'Adapter', (Adapter,), self.base_fields)
        self.adapter = self.adapter_class(strict=True)

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
