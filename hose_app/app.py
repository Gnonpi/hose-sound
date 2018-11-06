import os

from flask import Flask

from hose_app.extensions import login_manager, bcrypt
from hose_app.models import LogHoseUser


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
))


def register_extensions(app: Flask):
    bcrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return LogHoseUser.query.filter_by(id_user=user_id)

    login_manager.init_app(app)


def register_blueprint(app: Flask):
    from hose_app.views.hoses_view import hoses_view
    from hose_app.views.login_view import login_view

    app.register_blueprint(login_view, url_prefix='/entry')
    app.register_blueprint(hoses_view, url_prefix='/hose')


def create_app():
    app = CustomFlask(__name__)
    app.config['SERVER_NAME'] = os.environ['SERVICE_HOST'] + ':' + os.environ['SERVICE_PORT']

    register_extensions(app)
    register_blueprint(app)

    return app
