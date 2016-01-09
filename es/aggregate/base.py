from es.aggregate.meta import AggregateMeta
from es.aggregate.state import AggregateState


class Aggregate(metaclass=AggregateMeta):

    def __init__(self):
        self._state = AggregateState(self, self._meta)

    def apply_event(self, event, replay=False, version=None):
        """Applies an event to the :class:`Aggregate`."""
        self._publisher.publish(self, self._state, event,
            replay=replay, version=version)
