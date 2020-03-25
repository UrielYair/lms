import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect  # type: ignore
from peewee import SqliteDatabase, PostgresqlDatabase
from playhouse.flask_utils import FlaskDB

project_dir = os.path.abspath(os.path.curdir)
template_dir = os.path.join(project_dir, 'templates')
static_dir = os.path.join(project_dir, 'static')
webapp = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir,
)
webapp.config.from_pyfile('config.py')
if webapp.debug:
    _database = SqliteDatabase('db.sqlite')
else:
    db_config = {
        'database': webapp.config['DB_NAME'],
        'user': webapp.config['DB_USER'],
        'port': webapp.config['DB_PORT'],
        'host': webapp.config['DB_HOST_IP'],
        'password': webapp.config['DB_PASSWORD'],
    }
    _database = PostgresqlDatabase(**db_config)

db_wrapper = FlaskDB(webapp, _database)
database = db_wrapper.database
csrf = CSRFProtect(webapp)

# Must import files after app's creation
from lms.lmsweb import models, views  # NOQA: F401
