from db.db_conn import db

class Employee(db.Model):
    __tablename__ = "pracownicy"
    __table_args__ = {'schema': 'sklep'}
    id_pracownika = db.Column(db.Integer, primary_key=True)
    stanowisko = db.Column(db.String(50), nullable=False)
    __table_args__ = (
        db.CheckConstraint(
            """stanowisko IN ('Mechanik',
            'Księgowość',
            'Kierownik',
            'Sprzedawca',
            'Magazynier')""",
            name='check_stanowisko'
        ),
        {'schema': 'sklep'}
    )
    imie = db.Column(db.String(50), nullable=False)
    nazwisko = db.Column(db.String(50), nullable=False)
    wynagrodzenie = db.Column(db.Numeric(10, 2), nullable=False)
    numer_telefonu = db.Column(db.String(25), nullable=False)
    zlecenia = db.relationship('Order', backref='sklep.wykonawca', lazy=True)

    def to_dict(self):
        return {
            'id_pracownika': self.id_pracownika,
            'stanowisko': self.stanowisko,
            'imie': self.imie,
            'nazwisko': self.nazwisko,
            'wynagrodzenie': str(self.wynagrodzenie),
            'numer_telefonu': self.numer_telefonu,
        }