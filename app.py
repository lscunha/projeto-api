from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'API Flask está em execução!'

# Definição do modelo "Usuário"
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cpf = db.Column(db.String(11))

# Rotas da API
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    novo_usuario = Usuario(nome=data['nome'], telefone=data['telefone'], endereco=data['endereco'], cpf=data['cpf'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'})

@app.route('/usuarios', methods=['GET'])
def consultar_usuarios():
    usuarios = Usuario.query.all()
    resultados = []
    for usuario in usuarios:
        resultados.append({'id': usuario.id, 'nome': usuario.nome, 'telefone': usuario.telefone, 'endereco': usuario.endereco, 'cpf': usuario.cpf})
    return jsonify(resultados)

@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado!'})
    data = request.get_json()
    usuario.nome = data['nome']
    usuario.telefone = data['telefone']
    usuario.endereco = data['endereco']
    usuario.cpf = data['cpf']
    db.session.commit()
    return jsonify({'message': 'Usuário atualizado com sucesso!'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado!'})
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
