from flask import Blueprint

member_bp = Blueprint('member', __name__, url_prefix='/member')

from app.blueprints.member import routes