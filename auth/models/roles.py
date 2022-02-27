import uuid

from sqlalchemy.dialects.postgresql import UUID

from extensions import db
from models.base import BaseModel


class Role(BaseModel):
    __tablename__ = 'roles'

    code = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    description = db.Column(db.Text, default='')

    def __repr__(self):
        return f'({self.code}) {self.description}'


class UserRole(BaseModel):
    __tablename__ = 'users_roles'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, default=uuid.uuid4)  # noqa
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, default=uuid.uuid4)  # noqa
