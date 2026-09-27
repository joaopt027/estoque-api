from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    dados = request.get_json() or {}
    username = dados.get("username")
    senha = dados.get("senha")

    if not username or not senha:
        return jsonify({"erro": "username e senha são obrigatórios"}), 400

    if Usuario.query.filter_by(username=username).first():
        return jsonify({"erro": "usuário já existe"}), 409

    usuario = Usuario(username=username)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"mensagem": "usuário criado com sucesso"}), 201


@auth_bp.post("/login")
def login():
    dados = request.get_json() or {}
    username = dados.get("username")
    senha = dados.get("senha")

    usuario = Usuario.query.filter_by(username=username).first()

    if not usuario or not usuario.checar_senha(senha):
        return jsonify({"erro": "credenciais inválidas"}), 401

    token = create_access_token(identity=str(usuario.id))
    return jsonify({"access_token": token}), 200