from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..Config import db
from .WalletUser import WalletUser


class DelayUpdateBalance(db.Model):
    __tablename__ = 'delay_update_balance'

    id          = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    owned_by    = db.Column(UUID(as_uuid=True), db.ForeignKey(WalletUser.id))
    time_limit  = db.Column(db.Time())
    old_balance = db.Column(db.BigInteger())

    # joined table
    wallet_user_detail = db.relationship("WalletUser", backref="delay_update_balance_to_wallet_user")

    def __init__(self, **data):
        self.owned_by    = data['owned_by']
        self.time_limit  = data['time_limit']
        self.old_balance = data['old_balance']