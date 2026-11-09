from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# Konfigurasi halaman login default untuk Flask-Login
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan masuk terlebih dahulu untuk mengakses halaman ini.'
login_manager.login_message_category = 'warning'

# Mengaktifkan Foreign Key & WAL Mode di SQLite untuk performa setara produksi
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.close()