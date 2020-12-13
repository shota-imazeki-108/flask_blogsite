from flask import Flask
from flask_bcrypt import Bcrypt
from flaskblog.config import Config


bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)

    from flaskblog.main.routes import main
    from flaskblog.wordcloud.routes import wordcloud
    from flaskblog.girls.routes import girls
    from flaskblog.errors.handlers import errors

    # Blueprintに登録
    app.register_blueprint(main)
    app.register_blueprint(wordcloud)
    app.register_blueprint(girls)
    app.register_blueprint(errors)

    return app
