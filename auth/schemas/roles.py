from models.roles import Role, UserRole
from extensions import ma


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role
        fields = ('id', 'code', 'description')


class UserRoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserRole
        fields = ('id', 'user_id', 'role_id')


role_schema = RoleSchema()
user_role_schema = UserRoleSchema()
