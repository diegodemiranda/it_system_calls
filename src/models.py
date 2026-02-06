from datetime import datetime


class Usuario:
    def __init__(self, id, nome, email, setor):
        self.id = int(id)
        self.nome = nome
        self.email = email
        self.setor = setor

    def __str__(self):
        return f"[ID: {self.id}] {self.nome} - {self.setor}"


class Tecnico:
    def __init__(self, id, nome, email, especialidade):
        self.id = int(id)
        self.nome = nome
        self.email = email
        self.especialidade = especialidade

    def __str__(self):
        return f"[ID: {self.id}] {self.nome} - Esp: {self.especialidade}"


class Chamado:
    def __init__(self, id, usuario_id, titulo, descricao, prioridade, status="Aberto", tecnico_id=None,
                 data_abertura=None, data_fechamento=None):
        self.id = int(id)
        self.usuario_id = int(usuario_id)  # Relacionamento por ID
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = status

        # Tratamento para tecnico_id que pode vir como string vazia do CSV ou None
        if tecnico_id and str(tecnico_id).strip():
            self.tecnico_id = int(tecnico_id)
        else:
            self.tecnico_id = None

        # Define data atual se não for passada
        self.data_abertura = data_abertura if data_abertura else datetime.now().strftime("%d/%m/%Y %H:%M")
        self.data_fechamento = data_fechamento

    def __str__(self):
        tec_str = f"Téc ID: {self.tecnico_id}" if self.tecnico_id else "Não atribuído"
        return (f"Chamado #{self.id} | Status: {self.status.upper()} | Prioridade: {self.prioridade}\n"
                f"   Título: {self.titulo}\n"
                f"   Usuário ID: {self.usuario_id} | {tec_str}\n"
                f"   Aberto em: {self.data_abertura}")