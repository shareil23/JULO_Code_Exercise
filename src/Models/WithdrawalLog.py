from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..Config import db
from .WalletUser import WalletUser
from .ReferenceLog import ReferenceLog


class WithdrawalLog(db.Model):
    __tablename__ = 'withdrawal_log'

    id           = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    withdrawn_by = db.Column(UUID(as_uuid=True), db.ForeignKey(WalletUser.id))
    reference_id = db.Column(UUID(as_uuid=True), db.ForeignKey(ReferenceLog.id))
    withdrawn_at = db.Column(db.DateTime(timezone=True))
    amount       = db.Column(db.BigInteger())
    status       = db.Column(db.Text())

    # joined table
    wallet_user_detail = db.relationship("WalletUser", backref="withdrawal_log_to_wallet_user")
    reference_detail   = db.relationship("ReferenceLog", backref="withdrawal_log_to_reference_log")

    def __init__(self, **data):
        self.withdrawn_by = data['withdrawn_by']
        self.reference_id = data['reference_id']
        self.withdrawn_at = data['withdrawn_at']
        self.amount       = data['amount']
        self.status       = data['status']