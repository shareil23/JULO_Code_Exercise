from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..Config import db
from .WalletUser import WalletUser


class Wallet(db.Model):
    __tablename__ = 'wallet'

    id          = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owned_by    = db.Column(UUID(as_uuid=True), db.ForeignKey(WalletUser.id))
    status      = db.Column(db.Text())
    enabled_at  = db.Column(db.DateTime(timezone=True))
    disabled_at = db.Column(db.DateTime(timezone=True))
    balance     = db.Column(db.BigInteger())

    # joined table
    wallet_user_detail = db.relationship("WalletUser", backref="wallet_to_wallet_user")

    def __init__(self, **data):
        self.owned_by = data['owned_by']
        self.status   = data['status']
        self.balance  = data['balance']