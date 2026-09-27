from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Produto, Movimentacao

movimentacoes_bp = Blueprint("movimentacoes", __name__)


@movimentacoes_bp.get("")
def listar_movimentacoes():
    produto_id = request.args.get("produto_id", type=int)
    query = Movimentacao.query
    if produto_id:
        query = query.filter_by(produto_id=produto_id)
    movimentacoes = query.order_by(Movimentacao.criado_em.desc()).all()
    return jsonify([m.to_dict() for m in movimentacoes]), 200


@movimentacoes_bp.post("")
@jwt_required()
def registrar_movimentacao():
    dados = request.get_json() or {}
    produto_id = dados.get("produto_id")
    tipo = dados.get("tipo")
    quantidade = dados.get("quantidade")
    observacao = dados.get("observacao")

    if not produto_id or tipo not in ("entrada", "saida") or not quantidade:
        return jsonify({
            "erro": "produto_id, tipo ('entrada' ou 'saida') e quantidade são obrigatórios"
        }), 400

    if quantidade <= 0:
        return jsonify({"erro": "quantidade deve ser positiva"}), 400

    produto = Produto.query.get_or_404(produto_id)

    if tipo == "saida" and produto.quantidade < quantidade:
        return jsonify({"erro": "estoque insuficiente para essa saída"}), 400

    if tipo == "entrada":
        produto.quantidade += quantidade
    else:
        produto.quantidade -= quantidade

    movimentacao = Movimentacao(
        produto_id=produto_id,
        tipo=tipo,
        quantidade=quantidade,
        observacao=observacao,
    )

    db.session.add(movimentacao)
    db.session.commit()

    return jsonify({
        "movimentacao": movimentacao.to_dict(),
        "produto_atualizado": produto.to_dict(),
    }), 201