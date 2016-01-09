

class IEventStore:
    """Specifies the basic interface for an event store,
    the backend used to persist events.
    """
    default_user = 1
    default_service = 1
    ConcurrencyException = type('ConcurrencyException', (Exception,), {})

    def persist_event(self, aggregrate_id, version, event_type, event_data,
        user_id=None, service_id=None, transaction_id=None):
        """Persist an event in the storage backend. Return an unsigned long
        integer identifying the event.

        Args:
            aggregrate_id: a string identifying the aggregate in which
                the event took place.
            version: the aggregate version that dispatched the event.
            event_type: a string specifying the event type.
            event_data: the event parameters.
            user_id: an unsigned long integer identifying the user that
                triggered the event.
            service_id: an unsigned long integer identifying the service
                through which the event was triggered.

        Returns:
            unsigned long integer
        """
        raise NotImplementedError("Subclasses must override this method.")

    def get_default_user(self):
        """Return the identifier of the default user."""
        return self.default_user

    def get_default_service(self):
        """Return the identifier of the default service."""
        return self.default_service
