import os

from flask import Flask


def create_app(test_config=None):
    """Create an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from app import db
    db.init_app(app)

    # apply the blueprints to the app
    from app import actors, movies, streams, index
    app.register_blueprint(actors.bp)
    app.register_blueprint(movies.bp)
    app.register_blueprint(streams.bp)
    app.register_blueprint(index.bp)

    return app
