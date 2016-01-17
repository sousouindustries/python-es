from es.aggregate.options import AggregateOptions
from es.publisher import EventPublisher
from es.publisher import EventHandler
from es.fields import Field


class AggregateMeta(type):
    ProgrammingError = type('ProgrammingError', (Exception,), {})

    def __new__(cls, name, bases, attrs):
        super_new = super(AggregateMeta, cls).__new__
        if name == 'Aggregate':
            return super_new(cls, name, bases, attrs)

        module = attrs.pop('__module__')
        publisher = EventPublisher()
        meta = AggregateOptions(attrs.pop('Meta', None))
        new_class = super_new(cls, name, bases, {'__module__': module})
        new_class.add_to_class('_meta', meta)
        new_class.add_to_class('_publisher', publisher)
        
        for attname, value in list(attrs.items()):
            if issubclass(type(value), Field):
                meta.add_field(attname, value)
                del attrs[attname]

            if isinstance(value, EventHandler):
                value.add_to_publisher(publisher)
                del attrs[attname]

        for attname, value in attrs.items():
            new_class.add_to_class(attname, value)

        return new_class

    def add_to_class(self, attname, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(attname, self)
        else:
            setattr(self, attname, value)
