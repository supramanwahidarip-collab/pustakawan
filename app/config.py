import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tosca-enterprise-secret-key-2026-prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'instance', 'library_baru.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Konfigurasi Aturan Bisnis Perpustakaan
    MAX_LOAN_DAYS = 7  # Durasi standar peminjaman (7 hari)
    MAX_BOOKS_PER_MEMBER = 3  # Batas buku yang boleh dipinjam bersamaan
    FINE_PER_DAY = 2000  # Denda keterlambatan: Rp 2.000 / hari
    REMEMBER_COOKIE_DURATION = timedelta(days=7)