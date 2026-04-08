from flask import Flask, request, jsonify, render_template, redirect, url_for, abort
from database import (
    init_db, inserir_leitura, listar_leituras, contar_leituras,
    buscar_leitura, atualizar_leitura, deletar_leitura, obter_estatisticas
)

app = Flask(__name__)

# Inicializa o banco ao subir a aplicação
with app.app_context():
    init_db()


# HELPERS

def quer_json():
    """Retorna True se o cliente pediu JSON (parâmetro ?formato=json ou Accept header)."""
    return (request.args.get('formato') == 'json' or
            request.accept_mimetypes.best == 'application/json')


# ROTAS HTML / API

@app.route('/')
def index():
    """Painel principal — últimas 10 leituras."""
    leituras = listar_leituras(limite=10)
    stats    = obter_estatisticas()

    if quer_json():
        return jsonify({'leituras': leituras, 'estatisticas': stats})

    return render_template('index.html', leituras=leituras, stats=stats)


@app.route('/leituras', methods=['GET'])
def listar():
    """Histórico completo com paginação."""
    pagina  = int(request.args.get('pagina', 1))
    limite  = int(request.args.get('limite', 20))
    offset  = (pagina - 1) * limite
    leituras = listar_leituras(limite=limite, offset=offset)
    total = contar_leituras()
    total_paginas = (total + limite - 1) // limite  # Calcula o teto da divisão

    if quer_json():
        return jsonify({'pagina': pagina, 'limite': limite, 'leituras': leituras, 'total': total})

    return render_template('historico.html', leituras=leituras,
                           pagina=pagina, limite=limite, total=total, total_paginas=total_paginas)


@app.route('/leituras', methods=['POST'])
def criar():
    """Recebe JSON do Arduino / simulador e salva no banco."""
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'JSON inválido ou ausente'}), 400

    if 'temperatura' not in dados or 'umidade' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: temperatura, umidade'}), 422

    novo_id = inserir_leitura(
        temperatura=float(dados['temperatura']),
        umidade=float(dados['umidade']),
        pressao=dados.get('pressao'),
        localizacao=dados.get('localizacao', 'Lab')
    )
    return jsonify({'id': novo_id, 'status': 'criado'}), 201


@app.route('/leituras/<int:id>', methods=['GET'])
def detalhe(id):
    """Exibe uma leitura específica."""
    leitura = buscar_leitura(id)
    if not leitura:
        abort(404)

    if quer_json():
        return jsonify(leitura)

    return render_template('detalhe.html', leitura=leitura)


@app.route('/leituras/<int:id>', methods=['PUT', 'PATCH'])
def atualizar(id):
    """Atualiza campos de uma leitura."""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400

    ok = atualizar_leitura(id, dados)
    if not ok:
        return jsonify({'erro': 'Leitura não encontrada ou nenhum campo válido'}), 404

    return jsonify({'status': 'atualizado', 'id': id})


@app.route('/leituras/<int:id>/editar', methods=['GET'])
def editar_form(id):
    """Exibe formulário de edição."""
    leitura = buscar_leitura(id)
    if not leitura:
        abort(404)
    return render_template('editar.html', leitura=leitura)


@app.route('/leituras/<int:id>', methods=['DELETE'])
def deletar(id):
    """Remove uma leitura do banco."""
    ok = deletar_leitura(id)
    if not ok:
        return jsonify({'erro': 'Leitura não encontrada'}), 404
    return jsonify({'status': 'deletado', 'id': id})


@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    """Média, mínimo e máximo do período."""
    stats = obter_estatisticas()
    return jsonify(stats)


# TRATAMENTO DE ERROS

@app.errorhandler(404)
def nao_encontrado(e):
    if quer_json():
        return jsonify({'erro': 'Recurso não encontrado'}), 404
    return render_template('404.html'), 404


# ENTRY POINT

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)