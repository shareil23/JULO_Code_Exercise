from ..Config import ma
from ..Models import WithdrawalLog


class WithdrawalLogSchemaList(ma.SQLAlchemyAutoSchema):
    class Meta:
        model      = WithdrawalLog
        include_fk = True