from ..Config import ma
from ..Models import DelayUpdateBalance


class DelayUpdateBalanceSchemaList(ma.SQLAlchemyAutoSchema):
    class Meta:
        model      = DelayUpdateBalance
        include_fk = True