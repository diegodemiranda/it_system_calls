import repositorio_chamados

def listar_chamados_abertos():
    todos = repositorio_chamados.listar_todos()
    return [c for c in todos if c.status not in ["Resolvido", "Cancelado"]]

def listar_por_usuario(usuario_id):
    todos = repositorio_chamados.listar_todos()
    return [c for c in todos if c.usuario_id == int(usuario_id)]

def listar_por_tecnico(tecnico_id):
    todos = repositorio_chamados.listar_todos()
    return [c for c in todos if c.tecnico_id == int(tecnico_id)]