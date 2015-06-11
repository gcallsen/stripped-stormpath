import datetime
import logging
from flask import Blueprint, abort, jsonify, request
from sqlalchemy.orm import joinedload
from flask.ext.cors import cross_origin
from flask.ext.stormpath import login_required
from apps import stormpath_manager
from . import fantasy_bp

logger = logging.getLogger(__name__)


@fantasy_bp.route('/')
@login_required
def index():
    return "Hello World! Protected..."


@fantasy_bp.route('/welcome')
def welcome_page():
    return "Hello World! This is unprotected!"


@fantasy_bp.route('/verify-email')
def verify_email():

    try:
        account = stormpath_manager.client.accounts.verify_email_token(request.args.get('sptoken'))
    except Exception, e:
        logger.error(e)
        abort(400)

    return "Successfully verified email!"
