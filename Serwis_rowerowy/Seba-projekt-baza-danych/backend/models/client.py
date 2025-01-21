from db.db_conn import db

class Client(db.Model):
    __tablename__ = "klienci"
    __table_args__ = {'schema': 'sklep'}
    id_klienta = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(50), nullable=False)
    nazwisko = db.Column(db.String(50), nullable=False)
    numer_telefonu = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id_klienta': self.id_klienta,
            'imie': self.imie,
            'nazwisko': self.nazwisko,
            'numer_telefonu': self.numer_telefonu,
            'email': self.email,
        }