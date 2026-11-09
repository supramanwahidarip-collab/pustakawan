from datetime import datetime
from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    slug = db.Column(db.String(70), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)

    books = db.relationship('Book', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(120), nullable=False, index=True)
    publisher = db.Column(db.String(100), nullable=False)
    publish_year = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False)

    synopsis = db.Column(db.Text, nullable=True)
    shelf_location = db.Column(db.String(30), nullable=False, default='RAK-A1')
    cover_url = db.Column(db.String(255), nullable=True)

    stock_total = db.Column(db.Integer, nullable=False, default=1)
    stock_available = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    loans = db.relationship('Loan', back_populates='book', lazy='dynamic')

    @property
    def is_available(self):
        return self.stock_available > 0

    def __repr__(self):
        return f'<Book {self.title} ({self.stock_available}/{self.stock_total})>'