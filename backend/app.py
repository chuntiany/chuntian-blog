from flask import Flask
from config import Config
from extensions import db, migrate, login_manager, cors
import models # Ensure models are imported

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.article import article_bp
    from routes.category import category_bp
    from routes.comment import comment_bp
    from routes.settings import settings_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(settings_bp)
    
    @app.route('/')
    def index():
        return "Blog Backend API"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
