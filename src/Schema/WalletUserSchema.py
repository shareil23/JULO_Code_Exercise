from ..Config import ma
from ..Models import WalletUser


class WalletUserSchemaList(ma.SQLAlchemyAutoSchema):
    class Meta:
        model      = WalletUser
        include_fk = True