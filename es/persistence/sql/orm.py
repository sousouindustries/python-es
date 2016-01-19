import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID


Relation = declarative_base()


class Source(Relation):
    """Maps the ``sources`` table to a Python object."""
    __tablename__ = 'sources'

    aggregate_type = Column(String,
        nullable=False,
        name='aggregate_type'
    )

    aggregate_id = Column(UUID,
        nullable=False,
        primary_key=True,
        name='aggregate_id'
    )

    object_id = Column(BigInteger,
        nullable=False,
        unique=True,
        server_default=func.nextval('mds_object_id_seq'),
        name='object_id'
    )

    version = Column(Integer,
        nullable=False,
        server_default='0',
        default=0,
        name='version'
    )

    created = Column(BigInteger,
        nullable=False,
        default=lambda: int(time.time() * 1000),
        name='created'
    )


class Event(Relation):
    """Represents an incoming event."""
    __tablename__ = 'events'

    aggregate_id = Column(ForeignKey(Source.aggregate_id),
        primary_key=True,
        name='aggregate_id'
    )

    version = Column(Integer,
        primary_key=True,
        name='version'
    )

    event_type = Column(String,
        nullable=False,
        name='event_type'
    )

    event_version = Column(Integer,
        default=1,
        server_default='1',
        nullable=False,
        name='event_version'
    )

    dispatched = Column(BigInteger,
        nullable=False,
        default=lambda: int(time.time() * 1000),
        name='dispatched'
    )

    params = Column(JSONB,
        nullable=False,
        name='parameters'
    )
