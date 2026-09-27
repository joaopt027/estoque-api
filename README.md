# API de Controle de Estoque

🔗 **[Ver API funcionando](https://estoque-api-mvx0.onrender.com)** · **[Documentação interativa (Swagger)](https://estoque-api-mvx0.onrender.com/apidocs)**

API REST para gerenciamento de produtos e movimentações de estoque (entradas e saídas), construída com **Flask**, **SQLAlchemy** e **PostgreSQL** (MySQL em ambiente local), com autenticação via **JWT** e documentação interativa via **Swagger**.

## Funcionalidades

- Cadastro e login de usuários com autenticação JWT
- CRUD completo de produtos
- Registro de entradas e saídas de estoque com histórico (auditoria)
- Validação de estoque insuficiente em saídas
- Documentação interativa via Swagger (`/apidocs`)

## Tecnologias

- Python 3 + Flask
- SQLAlchemy (ORM) + Flask-Migrate
- PostgreSQL em produção (Render) / MySQL em desenvolvimento local
- Flask-JWT-Extended
- Flasgger (Swagger/OpenAPI)
- Deploy: Render

## Decisões de arquitetura

- **Movimentações separadas de produtos:** em vez de simplesmente alterar o campo `quantidade` do produto, cada entrada/saída gera um registro na tabela `movimentacoes`. Isso permite auditoria, relatórios por período e é o padrão usado por sistemas de estoque reais.
- **Portabilidade entre bancos via ORM:** o projeto foi desenvolvido com MySQL localmente, mas o uso do SQLAlchemy permitiu migrar para PostgreSQL no deploy (Render) sem alterar a lógica da aplicação — só a string de conexão.
- **Padrão de fábrica de aplicação (`create_app`)**: facilita trocar configurações entre ambiente de desenvolvimento, produção e testes.
- **Blueprints**: rotas organizadas por domínio (`auth`, `produtos`, `movimentacoes`).

## Como rodar localmente

1. Clone o projeto e crie um ambiente virtual:
```bash
   python -m venv venv
   venv\Scripts\activate  # Linux/Mac: source venv/bin/activate
   pip install -r requirements.txt
```

2. Copie `.env.example` (ou crie um `.env`) e ajuste `DATABASE_URL` e `JWT_SECRET_KEY`.

3. Crie as tabelas:
```bash
   python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
```

4. Rode a aplicação:
```bash
   python run.py
```
   A API sobe em `http://localhost:5000`, com documentação em `http://localhost:5000/apidocs`.

## Endpoints principais

| Método | Rota                        | Autenticação | Descrição                          |
|--------|-----------------------------|:------------:|--------------------------------------|
| POST   | `/auth/register`            | Não          | Cria um novo usuário                 |
| POST   | `/auth/login`               | Não          | Retorna um token JWT                 |
| GET    | `/produtos`                 | Não          | Lista produtos (filtro `?categoria=`)|
| GET    | `/produtos/<id>`            | Não          | Detalha um produto                   |
| POST   | `/produtos`                 | Sim          | Cria um produto                      |
| PUT    | `/produtos/<id>`            | Sim          | Atualiza dados do produto            |
| DELETE | `/produtos/<id>`            | Sim          | Remove um produto                    |
| GET    | `/movimentacoes`            | Não          | Lista movimentações (filtro `?produto_id=`)|
| POST   | `/movimentacoes`            | Sim          | Registra entrada/saída de estoque    |

Teste todas as rotas direto pelo navegador, sem precisar do Postman, em: **https://estoque-api-mvx0.onrender.com/apidocs**

## Possíveis evoluções

- Paginação nas listagens
- Papéis de usuário (admin vs operador)
- Testes automatizados com pytest