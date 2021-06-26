from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..Config import db


class ReferenceLog(db.Model):
    __tablename__ = 'reference_log'

    id           = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference_id = db.Column(UUID(as_uuid=True))
    category     = db.Column(db.Text())
    created_at   = db.Column(db.DateTime(timezone=True))

    def __init__(self, **data):
        self.reference_id = data['reference_id']
        self.category     = data['category']
        self.created_at   = data['created_at']