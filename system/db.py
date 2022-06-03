from flask_sqlalchemy import SQLAlchemy
import config
import system

system.app.config.update({
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
        config.db.user,
        config.db.password,
        config.db.host,
        config.db.port,
        config.db.database),
})

db = SQLAlchemy(system.app)