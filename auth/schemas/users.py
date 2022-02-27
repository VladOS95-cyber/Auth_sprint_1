from models.roles import Role
from extensions import ma


class UserDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role


user_data_schema = UserDataSchema()
