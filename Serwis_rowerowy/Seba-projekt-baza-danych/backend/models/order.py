from db.db_conn import db

class Order(db.Model):
    __tablename__ = "zlecenia"
    __table_args__ = {'schema': 'sklep'}
    id_zlecenia = db.Column(db.Integer, primary_key=True)
    rower = db.Column(db.Integer, db.ForeignKey('sklep.rowery.id_rowera'), nullable=False)
    usluga = db.Column(db.Integer, db.ForeignKey('sklep.uslugi.id_uslugi'), nullable=False)
    data_zlecenia = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False)
    __table_args__ = (
        db.CheckConstraint(
            """status IN ('Zgłoszone',
            'Przyjęte do realizacji',
            'W trakcie realizacji',
            'W trakcie realizacji - opłacono',
            'Zrealizowano - do opłacenia',
            'Zrealizowano - opłacone',
            'Zrealizowano - nieopłacone', 'Anulowane')""",
            name='check_order_status'
        ),
        {'schema': 'sklep'}
    )
    wykonawca = db.Column(db.Integer, db.ForeignKey('sklep.pracownicy.id_pracownika'), nullable=False)

    def to_dict(self):
        return {
            'id_zlecenia': self.id_zlecenia,
            'rower': self.rower,
            'usluga': self.usluga,
            'data_zlecenia': str(self.data_zlecenia),
            'status': self.status,
            'wykonawca': self.wykonawca,
        }