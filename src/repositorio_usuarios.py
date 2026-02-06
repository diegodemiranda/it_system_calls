import csv
import os
from models import Usuario

FILE_PATH = os.path.join('data', 'usuarios.csv')

def inicializar_arquivo():
    """Inicializa o arquivo CSV com cabeçalhos se não existir."""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'nome', 'email', 'setor'])
    except IOError as e:
        print(f"Erro ao inicializar arquivo de usuários: {e}")

def salvar(usuario):
    """Salva um usuário no arquivo CSV (append)."""
    try:
        with open(FILE_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([usuario.id, usuario.nome, usuario.email, usuario.setor])
    except IOError as e:
        print(f"Erro ao salvar usuário: {e}")
    except Exception as e:
        print(f"Erro inesperado ao salvar usuário: {e}")

def listar_todos():
    """Lista todos os usuários do arquivo CSV com validação robusta."""
    usuarios = []
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Pula cabeçalho
                for row in reader:
                    if not row:
                        continue

                    # Valida comprimento e faz limpeza básica dos campos
                    if len(row) < 4:
                        continue

                    id_str = row[0].strip()
                    nome = row[1].strip()
                    email = row[2].strip()
                    setor = row[3].strip()

                    try:
                        id_val = int(id_str)
                    except ValueError:
                        continue

                    usuarios.append(Usuario(id_val, nome, email, setor))
    except IOError as e:
        print(f"Erro ao listar usuários: {e}")
    except Exception as e:
        print(f"Erro inesperado ao listar usuários: {e}")
    return usuarios

def buscar_por_id(id_buscado):
    """Busca um usuário por ID."""
    try:
        usuarios = listar_todos()
        for u in usuarios:
            if u.id == int(id_buscado):
                return u
    except (ValueError, TypeError) as e:
        print(f"Erro ao buscar usuário: {e}")
    return None

def gerar_novo_id():
    """Gera um novo ID único para um usuário."""
    try:
        usuarios = listar_todos()
        if not usuarios:
            return 1
        return usuarios[-1].id + 1
    except Exception as e:
        print(f"Erro ao gerar novo ID de usuário: {e}")
        return 1