from datetime import datetime
from app.extensions import db


class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    loan_code = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    librarian_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relasi bersih menggunakan back_populates tanpa bentrok
    user = db.relationship('User', foreign_keys=[user_id])
    librarian = db.relationship('User', foreign_keys=[librarian_id])
    book = db.relationship('Book', back_populates='loans')

    status = db.Column(db.String(20), default='PENDING')
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    borrow_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)