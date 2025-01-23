from db.db_conn import db

class Service(db.Model):
    __tablename__ = "uslugi"
    __table_args__ = {'schema': 'sklep'}
    id_uslugi = db.Column(db.Integer, primary_key=True)
    cena = db.Column(db.Numeric(10, 2), nullable=False)
    nazwa = db.Column(db.String(100), nullable=False)
    opis = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id_uslugi': self.id_uslugi,
            'cena': str(self.cena),
            'nazwa': self.nazwa,
            'opis': self.opis,
        }