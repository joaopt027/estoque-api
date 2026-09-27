from flask import Flask
from app.config import Config
from app.extensions import db, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

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

    @app.get("/setup-db")
    def setup_db():
        db.create_all()
        return {"mensagem": "Tabelas criadas com sucesso"}

    return app