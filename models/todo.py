from system import db

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.task