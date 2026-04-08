import sqlite3
import os

# Caminho absoluto para o banco, sempre relativo a este arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, 'dados.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')


def get_db_connection():
    """Retorna uma conexão configurada com WAL mode e row_factory."""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')   # permite leitura/escrita simultânea
    conn.execute('PRAGMA busy_timeout=5000')  # espera até 5s antes de lançar erro
    conn.row_factory = sqlite3.Row            # acesso por nome de coluna
    return conn


def init_db():
    """Cria as tabelas se ainda não existirem."""
    conn = get_db_connection()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def inserir_leitura(temperatura: float, umidade: float,
                    pressao: float = None, localizacao: str = 'Lab') -> int:
    """Insere uma nova leitura e retorna o id gerado."""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO leituras (temperatura, umidade, pressao, localizacao) '
        'VALUES (?, ?, ?, ?)',
        (temperatura, umidade, pressao, localizacao)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id


def listar_leituras(limite: int = 50, offset: int = 0) -> list:
    """Retorna leituras mais recentes com paginação."""
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ? OFFSET ?',
        (limite, offset)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def buscar_leitura(id: int) -> dict | None:
    """Retorna uma leitura pelo id, ou None se não existir."""
    conn = get_db_connection()
    row = conn.execute(
        'SELECT * FROM leituras WHERE id = ?', (id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def atualizar_leitura(id: int, dados: dict) -> bool:
    """
    Atualiza os campos fornecidos em `dados` para a leitura com o id informado.
    Retorna True se alguma linha foi alterada.
    """
    campos_permitidos = {'temperatura', 'umidade', 'pressao', 'localizacao'}
    campos = {k: v for k, v in dados.items() if k in campos_permitidos}

    if not campos:
        return False

    set_clause = ', '.join(f'{k} = ?' for k in campos)
    valores = list(campos.values()) + [id]

    conn = get_db_connection()
    cursor = conn.execute(
        f'UPDATE leituras SET {set_clause} WHERE id = ?', valores
    )
    conn.commit()
    alterado = cursor.rowcount > 0
    conn.close()
    return alterado


def deletar_leitura(id: int) -> bool:
    """Remove uma leitura pelo id. Retorna True se deletou."""
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM leituras WHERE id = ?', (id,))
    conn.commit()
    deletado = cursor.rowcount > 0
    conn.close()
    return deletado


def contar_leituras() -> int:
    """Retorna o total de leituras no banco."""
    conn = get_db_connection()
    row = conn.execute('SELECT COUNT(*) as total FROM leituras').fetchone()
    conn.close()
    return row['total'] if row else 0


def obter_estatisticas() -> dict:
    """Retorna média, mínimo e máximo de temperatura, umidade e pressão."""
    conn = get_db_connection()
    row = conn.execute('''
        SELECT
            ROUND(AVG(temperatura), 2) AS temp_media,
            ROUND(MIN(temperatura), 2) AS temp_min,
            ROUND(MAX(temperatura), 2) AS temp_max,
            ROUND(AVG(umidade), 2)     AS umid_media,
            ROUND(MIN(umidade), 2)     AS umid_min,
            ROUND(MAX(umidade), 2)     AS umid_max,
            ROUND(AVG(pressao), 2)     AS pres_media,
            ROUND(MIN(pressao), 2)     AS pres_min,
            ROUND(MAX(pressao), 2)     AS pres_max,
            COUNT(*)                   AS total
        FROM leituras
    ''').fetchone()
    conn.close()
    return dict(row) if row else {}