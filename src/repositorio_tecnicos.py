import csv
import os
from models import Tecnico

FILE_PATH = os.path.join('data', 'tecnicos.csv')

def inicializar_arquivo():
    """Inicializa o arquivo CSV de técnicos com cabeçalhos se não existir."""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'nome', 'email', 'especialidade'])
    except IOError as e:
        print(f"Erro ao inicializar arquivo de técnicos: {e}")

def salvar(tecnico):
    """Salva um técnico no arquivo CSV (append)."""
    try:
        with open(FILE_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([tecnico.id, tecnico.nome, tecnico.email, tecnico.especialidade])
    except IOError as e:
        print(f"Erro ao salvar técnico: {e}")
    except Exception as e:
        print(f"Erro inesperado ao salvar técnico: {e}")

def listar_todos():
    """Lista todos os técnicos do arquivo CSV com validação robusta."""
    tecnicos = []
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if not row:
                        continue

                    # Valida comprimento
                    if len(row) < 4:
                        continue

                    id_str = row[0].strip()
                    nome = row[1].strip()
                    email = row[2].strip()
                    especialidade = row[3].strip()

                    try:
                        id_val = int(id_str)
                    except ValueError:
                        continue

                    tecnicos.append(Tecnico(id_val, nome, email, especialidade))
    except IOError as e:
        print(f"Erro ao listar técnicos: {e}")
    except Exception as e:
        print(f"Erro inesperado ao listar técnicos: {e}")
    return tecnicos

def buscar_por_id(id_buscado):
    """Busca um técnico por ID."""
    try:
        tecnicos = listar_todos()
        for t in tecnicos:
            if t.id == int(id_buscado):
                return t
    except (ValueError, TypeError) as e:
        print(f"Erro ao buscar técnico: {e}")
    return None

def gerar_novo_id():
    """Gera um novo ID único para um técnico."""
    try:
        tecnicos = listar_todos()
        if not tecnicos:
            return 1
        return tecnicos[-1].id + 1
    except Exception as e:
        print(f"Erro ao gerar novo ID de técnico: {e}")
        return 1