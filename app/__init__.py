from flask import Flask
from flasgger import Swagger
from app.config import Config
from app.extensions import db, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config["SWAGGER"] = {
        "title": "API de Controle de Estoque",
        "uiversion": 3,
    }

    swagger_template = {
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Digite: Bearer <seu_token>",
            }
        }
    }

    Swagger(app, template=swagger_template)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth_bp
    from app.routes.produtos import produtos_bp
    from app.routes.movimentacoes import movimentacoes_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(produtos_bp, url_prefix="/produtos")
    app.register_blueprint(movimentacoes_bp, url_prefix="/movimentacoes")

    @app.get("/")
    def health_check():
        return {"status": "ok", "servico": "estoque-api"}

    return app