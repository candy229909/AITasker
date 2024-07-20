# your_package/conversations/__init__.py
from flask import Blueprint

conversations_bp = Blueprint('conversations', __name__)

from . import routes
