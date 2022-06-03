from system import db

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    desc = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Client %r>' % self.username