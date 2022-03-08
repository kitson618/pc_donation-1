import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import login as login
from flask import Flask, request, current_app, session, render_template
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import AlwaysOnSampler
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from flask_babel import lazy_gettext as _l

login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
db = SQLAlchemy()

migrate = Migrate()
login = LoginManager()
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    # logger = logging.getLogger(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    GoogleMaps(app)
    csrf.init_app(app)
    # FlaskMiddleware(app, exporter=AzureExporter(
    #     connection_string="InstrumentationKey={}".format(app.config['APPINSIGHTS_INSTRUMENTATIONKEY'])),
    #                 sampler=ProbabilitySampler(rate=1.0))
    FlaskMiddleware(app,
                    exporter=AzureExporter(
                        connection_string="InstrumentationKey={}".format(
                            app.config['APPINSIGHTS_INSTRUMENTATIONKEY'])),
                    sampler=AlwaysOnSampler())

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/student')

    from app.support import bp as support_bp
    app.register_blueprint(support_bp, url_prefix='/support')

    from app.teacher import bp as teacher_bp
    app.register_blueprint(teacher_bp, url_prefix='/teacher')

    from app.donate import bp as donate_bp
    app.register_blueprint(donate_bp, url_prefix='/donate')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='Pc_donation Failure',
                credentials=auth,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/pc_donation.log',
                                           maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                              '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # logger = logging.getLogger(__name__)
        # handler = AzureEventHandler(
        #     connection_string="InstrumentationKey={}".format(app.config['APPINSIGHTS_INSTRUMENTATIONKEY']))
        handler = AzureLogHandler(
            connection_string="InstrumentationKey={}".format(
                app.config['APPINSIGHTS_INSTRUMENTATIONKEY']))
        handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                              '[in %(pathname)s:%(lineno)d]'))
        handler.setLevel(logging.ERROR)
        app.logger.addHandler(handler)
        app.register_error_handler(404, page_not_found)

        # for logHandler in app.logger.handlers:
        #     logHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
        #                                               '[in %(pathname)s:%(lineno)d]'))
        # logger.addHandler(
        #     AzureLogHandler(
        #         connection_string="InstrumentationKey={}".format(app.config['APPINSIGHTS_INSTRUMENTATIONKEY'])
        #     )
        # )

        app.logger.setLevel(logging.INFO)
        app.logger.info('pc_donate startup')

    return app


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # return "zh"
    language = request.accept_languages.best_match(
        current_app.config['LANGUAGES'])
    if session.get('language') is not None:
        language = session['language']
    return language


def page_not_found(e):
    return render_template('errors/404.html'), 404
