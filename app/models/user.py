from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    member_id_code = db.Column(db.String(20), unique=True, nullable=False) # Contoh: LIB-001 atau MBR-202601
    role = db.Column(db.String(20), nullable=False, default='member')      # 'librarian' atau 'member'
    phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke tabel peminjaman
    # Di dalam kelas User, cukup tuliskan seperti ini:
    loans = db.relationship('Loan', foreign_keys='Loan.user_id', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_librarian(self):
        return self.role == 'librarian'

    @property
    def active_loans_count(self):
        return self.loans.filter(Loan.status.in_(['PENDING', 'BORROWED', 'OVERDUE'])).count()

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))