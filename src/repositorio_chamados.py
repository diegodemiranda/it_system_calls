import csv
import os
from datetime import datetime
from models import Chamado

FILE_PATH = os.path.join('data', 'chamados.csv')


def inicializar_arquivo():
    """Inicializa o arquivo CSV de chamados com cabeçalhos se não existir."""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['id', 'usuario_id', 'titulo', 'descricao', 'prioridade', 'status', 'tecnico_id', 'data_abertura',
                     'data_fechamento'])
    except IOError as e:
        print(f"Erro ao inicializar arquivo de chamados: {e}")


def salvar_novo(chamado):
    """Salva um novo chamado no arquivo CSV."""
    try:
        with open(FILE_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Prepara tecnico_id para gravar (se for None, grava vazio)
            tec_id = chamado.tecnico_id if chamado.tecnico_id is not None else ""
            data_fechamento = chamado.data_fechamento if chamado.data_fechamento else ""

            writer.writerow([
                chamado.id, chamado.usuario_id, chamado.titulo, chamado.descricao,
                chamado.prioridade, chamado.status, tec_id,
                chamado.data_abertura, data_fechamento
            ])
    except IOError as e:
        print(f"Erro ao salvar chamado: {e}")
    except Exception as e:
        print(f"Erro inesperado ao salvar chamado: {e}")


def listar_todos():
    """Lista todos os chamados do arquivo CSV com validação robusta."""
    chamados = []
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if not row:
                        continue

                    # Garante que a linha tenha pelo menos 9 colunas (preenche com strings vazias)
                    # Campos: id, usuario_id, titulo, descricao, prioridade, status, tecnico_id, data_abertura, data_fechamento
                    if len(row) < 9:
                        row = row + [""] * (9 - len(row))

                    # Limpeza básica
                    id_str = row[0].strip()
                    usuario_str = row[1].strip()
                    titulo = row[2].strip()
                    descricao = row[3].strip()
                    prioridade = row[4].strip()
                    status = row[5].strip()
                    tecnico_str = row[6].strip()
                    data_abertura = row[7].strip() or None
                    data_fechamento = row[8].strip() or None

                    # Valida IDs básicos; pula linhas malformadas
                    try:
                        id_val = int(id_str)
                        usuario_val = int(usuario_str)
                    except (ValueError, TypeError):
                        continue

                    # tecnico_id pode ser vazio
                    tec_val = tecnico_str if tecnico_str else None

                    # Cria o objeto Chamado com valores limpos
                    c = Chamado(id_val, usuario_val, titulo, descricao, prioridade or "", status or "", tec_val, data_abertura, data_fechamento)
                    chamados.append(c)
    except IOError as e:
        print(f"Erro ao listar chamados: {e}")
    except Exception as e:
        print(f"Erro inesperado ao listar chamados: {e}")
    return chamados


def atualizar_chamado(chamado_atualizado):
    """
    Atualiza um chamado reescrevendo com segurança (arquivo temporário + replace atômico).
    Retorna True se atualizado com sucesso, False caso contrário.
    """
    try:
        todos = listar_todos()
        
        # Valida se existe
        if not any(c.id == chamado_atualizado.id for c in todos):
            return False
        
        # Escreve de forma atômica: escreve em arquivo temporário e faz replace
        temp_path = FILE_PATH + '.tmp'
        with open(temp_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'usuario_id', 'titulo', 'descricao', 'prioridade',
                            'status', 'tecnico_id', 'data_abertura', 'data_fechamento'])

            for c in todos:
                obj = chamado_atualizado if c.id == chamado_atualizado.id else c
                tec_id = obj.tecnico_id if obj.tecnico_id is not None else ""
                # Se o chamado for marcado como fechado e não tiver data, preenche timestamp
                if obj.status in ["Resolvido", "Cancelado"] and not obj.data_fechamento:
                    obj.data_fechamento = datetime.now().strftime("%d/%m/%Y %H:%M")
                data_fech = obj.data_fechamento if obj.data_fechamento else ""

                writer.writerow([obj.id, obj.usuario_id, obj.titulo, obj.descricao,
                                obj.prioridade, obj.status, tec_id, obj.data_abertura, data_fech])

        # Substitui o arquivo original de forma atômica
        os.replace(temp_path, FILE_PATH)
        return True
    except IOError as e:
        print(f"Erro ao atualizar chamado: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado ao atualizar chamado: {e}")
        return False


def buscar_por_id(id_buscado):
    """Busca um chamado por ID."""
    try:
        todos = listar_todos()
        for c in todos:
            if c.id == int(id_buscado):
                return c
    except (ValueError, TypeError) as e:
        print(f"Erro ao buscar chamado: {e}")
    return None


def gerar_novo_id():
    """
    Gera um novo ID único para um chamado.
    NOTA: Não é thread-safe; para aplicações multi-user, usar lock file ou BD.
    """
    try:
        todos = listar_todos()
        if not todos:
            return 1
        return todos[-1].id + 1
    except Exception as e:
        print(f"Erro ao gerar novo ID de chamado: {e}")
        return 1

        for c in todos:
            obj = chamado_atualizado if c.id == chamado_atualizado.id else c
            tec_id = obj.tecnico_id if obj.tecnico_id is not None else ""
            data_fech = obj.data_fechamento if obj.data_fechamento else ""

            writer.writerow([obj.id, obj.usuario_id, obj.titulo, obj.descricao,
                            obj.prioridade, obj.status, tec_id, obj.data_abertura, data_fech])

    # Substitui o arquivo original de forma atômica
    os.replace(temp_path, FILE_PATH)
    return True


def buscar_por_id(id_buscado):
    todos = listar_todos()
    for c in todos:
        if c.id == int(id_buscado):
            return c
    return None


def gerar_novo_id():
    """Gera um novo ID único para um chamado."""
    todos = listar_todos()
    if not todos:
        return 1
    return todos[-1].id + 1