import uuid

from libsousou.meta import hybrid_property
from es.aggregate.meta import AggregateMeta
from es.aggregate.state import AggregateState


class Aggregate(metaclass=AggregateMeta):

    @hybrid_property
    def aggregate_type(cls):
        return cls._meta.aggregate_type

    @property
    def aggregate_id(self):
        return self._id

    def __init__(self, aggregate_id=None):
        self._state = AggregateState(self, self._meta)
        self._id = aggregate_id or uuid.uuid4().hex

    def dump(self):
        """Serializes the current state of the aggregate as a Python
        dictionary.
        """
        return self._meta.dump(self._state)

    def apply_event(self, event, replay=False, version=None):
        """Applies an event to the :class:`Aggregate`."""
        self._publisher.publish(self, self._state, event,
            replay=replay, version=version)

    def get_uncommitted(self):
        """Return a generator yielding all uncommitted events and their
        version number.
        """
        state = self._state
        while state.is_dirty():
            yield state.pop()
