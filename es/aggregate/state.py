

class AggregateState:
    """Manages the state of an aggregate."""

    def __init__(self, aggregate, opts):
        self.__aggregate = aggregate
        self.__opts = opts
        self.__state = {}
        self.__version = 0
        self.__uncommitted = []
        self.__invalid = False

    def is_valid(self):
        """Return a boolean indicating if the state is valid."""
        return not self.__invalid

    def mark_invalid(self):
        """Mark the aggregate state as invalid."""
        self.__invalid = True

    def __setattr__(self, attname, value):
        if attname.startswith('_'):
            return super(AggregateState, self).__setattr__(attname, value)

        if not self.__opts.is_valid_field(attname):
            raise AttributeError(attname)
        self.__state[attname] = value

    def __getattr__(self, attname):
        if attname.startswith('_'):
            return super(AggregateState, self).__getattr__(attname)

        if not self.__opts.is_valid_field(attname):
            raise AttributeError(attname)
        return self.__state.get(attname)

    def increment_version(self):
        """Increments the aggregate version."""
        self.__version += 1
