from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..Config import db
from .WalletUser import WalletUser
from .ReferenceLog import ReferenceLog


class DepositLog(db.Model):
    __tablename__ = 'deposit_log'

    id           = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deposit_by   = db.Column(UUID(as_uuid=True), db.ForeignKey(WalletUser.id))
    reference_id = db.Column(UUID(as_uuid=True), db.ForeignKey(ReferenceLog.id))
    deposited_at = db.Column(db.DateTime(timezone=True))
    amount       = db.Column(db.BigInteger())
    status       = db.Column(db.Text())

    # joined table
    wallet_user_detail = db.relationship("WalletUser", backref="deposit_log_to_wallet_user")
    reference_detail   = db.relationship("ReferenceLog", backref="deposit_log_to_reference_log")

    def __init__(self, **data):
        self.deposit_by   = data['deposit_by']
        self.reference_id = data['reference_id']
        self.deposited_at = data['deposited_at']
        self.amount       = data['amount']
        self.status       = data['status']