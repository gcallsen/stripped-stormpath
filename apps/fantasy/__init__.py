from flask import Blueprint

fantasy_bp = Blueprint('fantasy', __name__)

from . import handlers
