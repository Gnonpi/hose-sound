import time
from urllib.parse import urlparse, urljoin

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user

from hose_app.models import LogHoseUser
from hose_core.models import Session

login_view = Blueprint('login_view', __name__, )

LOGIN_TEMPLATE = 'login.jinja2'


@login_view.route(rule='/', methods=['GET'])
def main_login():
    return render_template(LOGIN_TEMPLATE)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@login_view.route(rule='/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    db_session = Session()
    user = db_session.query(LogHoseUser).filter_by(email=email).first()
    if user is not None and user.check_password(password):
        login_user(user)
        next = request.args.get('next')
        if not is_safe_url(next):
            return jsonify({'data': None, 'error': 'Url redirect is not safe'}), 400
        return jsonify({'data': f"User {user.name} logged with success", "error": None}), 200
    else:
        time.sleep(1)
        return jsonify({'data': None, 'error': 'Could not login user'}), 400


@login_view.route(rule='/logout', methods=['POST'])
def logout():
    return 'Implement me', 500


@login_view.route(rule='/register', methods=['POST'])
def register():
    return 'Implement me', 500
