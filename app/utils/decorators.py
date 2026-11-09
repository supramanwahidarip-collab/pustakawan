from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def librarian_required(f):
    """Membatasi akses rute hanya untuk Pustakawan."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_librarian:
            flash('Akses ditolak. Halaman tersebut khusus untuk Pustakawan.', 'danger')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated_function

def member_required(f):
    """Membatasi akses rute khusus untuk Peminjam/Anggota."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.is_librarian:
            flash('Anda masuk sebagai Pustakawan. Dialihkan ke panel manajemen.', 'info')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated_function