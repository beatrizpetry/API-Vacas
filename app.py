from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
swagger = Swagger(app)

class Vaca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raca = db.Column(db.String(100), nullable=False)
    vacinada = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/vacas', methods=['POST'])
def criar_vaca():
    """Cria uma nova vaca
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            raca:
              type: string
            vacinada:
              type: boolean
    responses:
      200:
        description: Vaca criada com sucesso
    """
    data = request.get_json()
    nova_vaca = Vaca(raca=data['raca'], vacinada=data['vacinada'])
    db.session.add(nova_vaca)
    db.session.commit()
    return jsonify({"mensagem": "Vaca criada com sucesso!"})

@app.route('/vacas', methods=['GET'])
def listar_vacas():
    """Lista todas as vacas
    ---
    responses:
      200:
        description: Lista de vacas
    """
    vacas = Vaca.query.all()
    return jsonify([{'id': v.id, 'raca': v.raca, 'vacinada': v.vacinada} for v in vacas])

@app.route('/vacas/<int:id>', methods=['PUT'])
def atualizar_vaca(id):
    """Atualiza uma vaca existente
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          properties:
            raca:
              type: string
            vacinada:
              type: boolean
    responses:
      200:
        description: Vaca atualizada
    """
    data = request.get_json()
    vaca = Vaca.query.get_or_404(id)
    vaca.raca = data['raca']
    vaca.vacinada = data['vacinada']
    db.session.commit()
    return jsonify({"mensagem": "Vaca atualizada com sucesso!"})

@app.route('/vacas/<int:id>', methods=['DELETE'])
def deletar_vaca(id):
    """Deleta uma vaca
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Vaca deletada
    """
    vaca = Vaca.query.get_or_404(id)
    db.session.delete(vaca)
    db.session.commit()
    return jsonify({"mensagem": "Vaca deletada com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
