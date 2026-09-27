from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Produto

produtos_bp = Blueprint("produtos", __name__)


@produtos_bp.get("")
def listar_produtos():
    """
    Lista todos os produtos
    ---
    tags:
      - Produtos
    parameters:
      - in: query
        name: categoria
        type: string
        required: false
        description: Filtra produtos por categoria
    responses:
      200:
        description: Lista de produtos
    """
    categoria = request.args.get("categoria")
    query = Produto.query
    if categoria:
        query = query.filter_by(categoria=categoria)
    produtos = query.order_by(Produto.nome).all()
    return jsonify([p.to_dict() for p in produtos]), 200


@produtos_bp.get("/<int:produto_id>")
def obter_produto(produto_id):
    """
    Detalha um produto específico
    ---
    tags:
      - Produtos
    parameters:
      - in: path
        name: produto_id
        type: integer
        required: true
    responses:
      200:
        description: Dados do produto
      404:
        description: Produto não encontrado
    """
    produto = Produto.query.get_or_404(produto_id)
    return jsonify(produto.to_dict()), 200


@produtos_bp.post("")
@jwt_required()
def criar_produto():
    """
    Cria um novo produto
    ---
    tags:
      - Produtos
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Teclado Mecânico
            descricao:
              type: string
            categoria:
              type: string
            preco:
              type: number
              example: 250.0
            quantidade:
              type: integer
              example: 10
    responses:
      201:
        description: Produto criado
      400:
        description: Nome é obrigatório
      401:
        description: Token ausente ou inválido
    """
    dados = request.get_json() or {}
    nome = dados.get("nome")

    if not nome:
        return jsonify({"erro": "nome é obrigatório"}), 400

    produto = Produto(
        nome=nome,
        descricao=dados.get("descricao"),
        categoria=dados.get("categoria"),
        preco=dados.get("preco", 0),
        quantidade=dados.get("quantidade", 0),
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify(produto.to_dict()), 201


@produtos_bp.put("/<int:produto_id>")
@jwt_required()
def atualizar_produto(produto_id):
    """
    Atualiza os dados de um produto
    ---
    tags:
      - Produtos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: produto_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome:
              type: string
            descricao:
              type: string
            categoria:
              type: string
            preco:
              type: number
    responses:
      200:
        description: Produto atualizado
      401:
        description: Token ausente ou inválido
      404:
        description: Produto não encontrado
    """
    produto = Produto.query.get_or_404(produto_id)
    dados = request.get_json() or {}

    for campo in ["nome", "descricao", "categoria", "preco"]:
        if campo in dados:
            setattr(produto, campo, dados[campo])

    db.session.commit()
    return jsonify(produto.to_dict()), 200


@produtos_bp.delete("/<int:produto_id>")
@jwt_required()
def remover_produto(produto_id):
    """
    Remove um produto
    ---
    tags:
      - Produtos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: produto_id
        type: integer
        required: true
    responses:
      200:
        description: Produto removido
      401:
        description: Token ausente ou inválido
      404:
        description: Produto não encontrado
    """
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({"mensagem": "produto removido"}), 200