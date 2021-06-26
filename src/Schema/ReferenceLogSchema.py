from ..Config import ma
from ..Models import ReferenceLog


class ReferenceLogSchemaList(ma.SQLAlchemyAutoSchema):
    class Meta:
        model      = ReferenceLog
        include_fk = True