from ..Config import ma
from ..Models import Wallet
from datetime import datetime


class WalletSchemaList(ma.SQLAlchemyAutoSchema):
    class Meta:
        model      = Wallet
        include_fk = True
        exclude    = ("disabled_at", )


class WalletSchemaListDisabled(ma.SQLAlchemyAutoSchema):
    class Meta:
        model      = Wallet
        include_fk = True
        exclude    = ("enabled_at", )