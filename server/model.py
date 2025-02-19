from app import db


class KeyLog(db.Model):
    __tablename__: str = 'keylogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Text)
    date = db.Column(db.Text)
    keys = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return str({'id': self.id, 'device_id': self.device_id, 'keys': self.keys})
