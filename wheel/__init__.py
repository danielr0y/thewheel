from flask import Flask, render_template, request 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.env = 'development'
    app.debug = True
    # app.secret_key = 'h78gf43083740h3'
    app.config['SECRET_KEY'] = 'h78gf43083740h3'
    app.config['TRAP_HTTP_EXCEPTIONS'] = True 
    
    #initialize db 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wheel.sqlite'
    db.init_app(app)

    bootstrap = Bootstrap(app)
    
    #initialize the login manager

    login_manager = LoginManager()

    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User 
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(int(user_id))

    

    # import views
    from . import views
    app.register_blueprint(views.main)
    app.register_blueprint(views.events)

    from . import auth
    app.register_blueprint(auth.auth)
    

    @app.errorhandler(404)
    def handle_404(e):
        path = request.path
        # return a default response
        return render_template('404.html'), 404

    @app.errorhandler(405)
    def handle_405(e):
        path = request.path
        # return a default response
        return render_template('405.html'), 405

    @app.errorhandler(500)
    def handle_500(e):
        path = request.path
        # return a default response
        return render_template('500.html'), 500

    return app



