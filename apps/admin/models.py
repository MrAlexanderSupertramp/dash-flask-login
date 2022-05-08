# posts/models.py

# import sql-alchemy db instance created with factory application
from main.database import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(96), nullable=False)

    def __repr__(self):
        return f"post id: {self.id}"