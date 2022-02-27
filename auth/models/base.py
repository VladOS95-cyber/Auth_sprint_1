import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), nullable=False, unique=True, primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())  # noqa

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
