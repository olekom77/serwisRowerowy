from db.db_conn import db

class Bike(db.Model):
    __tablename__ = "rowery"
    __table_args__ = {'schema': 'sklep'}
    id_rowera = db.Column(db.Integer, primary_key=True)
    typ_roweru = db.Column(db.String(50), nullable=False)
    marka = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    klient_id = db.Column(db.Integer, db.ForeignKey('sklep.klienci.id_klienta'), nullable=False)

    def to_dict(self):
        return {
            'id_rowera': self.id_rowera,
            'typ_roweru': self.typ_roweru,
            'marka': self.marka,
            'model': self.model,
            'klient_id': self.klient_id
        }