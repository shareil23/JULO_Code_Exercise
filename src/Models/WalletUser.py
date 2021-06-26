from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..Config import db


class WalletUser(db.Model):
    __tablename__ = 'wallet_user'

    id           = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_xid = db.Column(db.Text())
    created_at   = db.Column(db.DateTime(timezone=True))

    def __init__(self, **data):
        self.customer_xid = data['customer_xid']
        self.created_at   = data['created_at']