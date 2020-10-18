import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["DATABASE"] = os.path.join(app.instance_path, 'rocket_api.sqlite')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import db
    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    return app