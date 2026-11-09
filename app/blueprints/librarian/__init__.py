from flask import Blueprint

librarian_bp = Blueprint('librarian', __name__, url_prefix='/librarian')

from app.blueprints.librarian import routes