from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from wilson.auth import login_required
from wilson.db import get_db

bp = Blueprint('mainpage', __name__)

@bp.route('/')
def mainpage():
    return render_template('mainpage/mainpage.html')