from flask import Flask, render_template
from flask.helpers import request
from flask_bootstrap import Bootstrap5
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap = Bootstrap5(app)

    # Initialize Flask extensions here

    # Register blueprints here

    @app.route('/')
    def index():
        return render_template('index.html')

    return app