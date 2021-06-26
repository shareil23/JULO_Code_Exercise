from ..Config import ma
from ..Models import DepositLog


class DepositLogSchemaList(ma.SQLAlchemyAutoSchema):
    class Meta:
        model      = DepositLog
        include_fk = True