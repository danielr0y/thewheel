from flask import Flask 
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    app.env = 'development'
    app.debug = True
    app.secret_key = 'h78gf43083740h3'
    
    bootstrap = Bootstrap(app)
    
    # import views
    from . import views
    app.register_blueprint(views.bp)
    
    return app



