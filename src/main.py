import os
import re
from datetime import datetime
from models import Usuario, Tecnico, Chamado
import repositorio_usuarios
import repositorio_tecnicos
import repositorio_chamados
import relatorios

# Validações simples usadas pela CLI
ALLOWED_PRIORITIES = ["Baixa", "Media", "Alta"]
ALLOWED_STATUS = ["Resolvido", "Cancelado", "Em Atendimento"]

# Padrão básico de email
EMAIL_PATTERN = r"^[^@]+@[^@]+\.[^@]+$"


# Funções de validação
def validar_nome(nome):
    """Valida nome: não vazio, mínimo 3 caracteres."""
    nome = nome.strip()
    if not nome or len(nome) < 3:
        print("Erro: Nome deve ter pelo menos 3 caracteres.")
        return None
    return nome


def validar_email(email):
    """Valida email com padrão básico."""
    email = email.strip().lower()
    if not re.match(EMAIL_PATTERN, email):
        print("Erro: Email inválido (ex: usuario@dominio.com).")
        return None
    return email


def validar_setor(setor):
    """Valida setor: não vazio, mínimo 2 caracteres."""
    setor = setor.strip()
    if not setor or len(setor) < 2:
        print("Erro: Setor deve ter pelo menos 2 caracteres.")
        return None
    return setor


def validar_texto(texto, min_len=5, nome_campo="Texto"):
    """Valida texto genérico (ex: título, descrição)."""
    texto = texto.strip()
    if not texto or len(texto) < min_len:
        print(f"Erro: {nome_campo} deve ter pelo menos {min_len} caracteres.")
        return None
    return texto


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def menu_principal():
    while True:
        print("\n=== SISTEMA DE SUPORTE DE TI ===")
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Técnicos")
        print("3. Abrir Chamado")
        print("4. Gerenciar Chamados (Atender/Listar)")
        print("0. Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            menu_usuarios()
        elif opcao == "2":
            menu_tecnicos()
        elif opcao == "3":
            abrir_chamado()
        elif opcao == "4":
            menu_gestao_chamados()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def menu_usuarios():
    print("\n--- Usuários ---")
    print("1. Cadastrar")
    print("2. Listar")
    op = input("Opção: ")
    if op == "1":
        nome = validar_nome(input("Nome: "))
        if not nome:
            return

        email = validar_email(input("Email: "))
        if not email:
            return

        setor = validar_setor(input("Setor: "))
        if not setor:
            return

        novo_id = repositorio_usuarios.gerar_novo_id()
        u = Usuario(novo_id, nome, email, setor)
        repositorio_usuarios.salvar(u)
        print(f"Usuário {nome} cadastrado com ID {novo_id}!")
    elif op == "2":
        lista = repositorio_usuarios.listar_todos()
        if not lista:
            print("Nenhum usuário cadastrado.")
        for u in lista:
            print(u)


def menu_tecnicos():
    print("\n--- Técnicos ---")
    print("1. Cadastrar")
    print("2. Listar")
    op = input("Opção: ")
    if op == "1":
        nome = validar_nome(input("Nome: "))
        if not nome:
            return

        email = validar_email(input("Email: "))
        if not email:
            return

        esp = validar_texto(
            input("Especialidade: "), min_len=3, nome_campo="Especialidade"
        )
        if not esp:
            return

        novo_id = repositorio_tecnicos.gerar_novo_id()
        t = Tecnico(novo_id, nome, email, esp)
        repositorio_tecnicos.salvar(t)
        print(f"Técnico {nome} cadastrado com ID {novo_id}!")
    elif op == "2":
        lista = repositorio_tecnicos.listar_todos()
        if not lista:
            print("Nenhum técnico cadastrado.")
        for t in lista:
            print(t)


def abrir_chamado():
    print("\n--- Novo Chamado ---")
    # Listar usuários para facilitar
    lista_usuarios = repositorio_usuarios.listar_todos()
    if not lista_usuarios:
        print("Nenhum usuário cadastrado. Cadastre um usuário primeiro.")
        return

    print("Selecione o Usuário:")
    for u in lista_usuarios:
        print(u)

    try:
        user_id = int(input("ID do Usuário: "))
        if not repositorio_usuarios.buscar_por_id(user_id):
            print("Usuário não encontrado.")
            return

        titulo = validar_texto(
            input("Título do Problema: "), min_len=5, nome_campo="Título"
        )
        if not titulo:
            return

        desc = validar_texto(
            input("Descrição detalhada: "), min_len=10, nome_campo="Descrição"
        )
        if not desc:
            return

        prioridade = input("Prioridade (Baixa/Media/Alta): ")
        prio_norm = prioridade.strip().capitalize()
        if prio_norm not in ALLOWED_PRIORITIES:
            print("Prioridade inválida. Use: Baixa, Media ou Alta.")
            return

        novo_id = repositorio_chamados.gerar_novo_id()
        c = Chamado(novo_id, user_id, titulo, desc, prio_norm)
        repositorio_chamados.salvar_novo(c)
        print(f"Chamado #{novo_id} aberto com sucesso!")

    except ValueError:
        print("Erro: Digite um ID numérico válido.")


def menu_gestao_chamados():
    while True:
        print("\n--- Gestão de Chamados ---")
        print("1. Listar TODOS Abertos")
        print("2. Listar por Usuário")
        print("3. Listar por Técnico")
        print("4. Atribuir Técnico a um Chamado")
        print("5. Atualizar Status (Resolver/Cancelar)")
        print("0. Voltar")

        op = input("Opção: ")

        if op == "1":
            lista = relatorios.listar_chamados_abertos()
            if not lista:
                print("Nenhum chamado aberto.")
            for c in lista:
                print("-" * 30 + "\n" + str(c))

        elif op == "2":
            uid = input("ID do Usuário: ")
            try:
                uid_int = int(uid)
            except ValueError:
                print("ID inválido. Digite um número.")
                continue
            lista = relatorios.listar_por_usuario(uid_int)
            for c in lista:
                print("-" * 30 + "\n" + str(c))

        elif op == "3":
            tid = input("ID do Técnico: ")
            try:
                tid_int = int(tid)
            except ValueError:
                print("ID inválido. Digite um número.")
                continue
            lista = relatorios.listar_por_tecnico(tid_int)
            for c in lista:
                print("-" * 30 + "\n" + str(c))

        elif op == "4":
            cid = input("ID do Chamado: ")
            try:
                cid_int = int(cid)
            except ValueError:
                print("ID inválido. Digite um número.")
                continue

            chamado = repositorio_chamados.buscar_por_id(cid_int)
            if chamado:
                print("Técnicos disponíveis:")
                for t in repositorio_tecnicos.listar_todos():
                    print(t)
                tid = input("ID do Técnico para atribuir: ")
                try:
                    tid_int = int(tid)
                except ValueError:
                    print("ID de técnico inválido.")
                    continue

                if repositorio_tecnicos.buscar_por_id(tid_int):
                    chamado.tecnico_id = tid_int
                    chamado.status = "Em Atendimento"
                    repositorio_chamados.atualizar_chamado(chamado)
                    print("Técnico atribuído com sucesso!")
                else:
                    print("Técnico inválido.")
            else:
                print("Chamado não encontrado.")

        elif op == "5":
            cid = input("ID do Chamado: ")
            try:
                cid_int = int(cid)
            except ValueError:
                print("ID inválido. Digite um número.")
                continue

            chamado = repositorio_chamados.buscar_por_id(cid_int)
            if chamado:
                print(f"Status atual: {chamado.status}")
                novo_status = input(
                    "Novo Status (Resolvido/Cancelado/Em Atendimento): "
                )

                # Normaliza e valida o status (case-insensitive)
                match = None
                for s in ALLOWED_STATUS:
                    if s.lower() == novo_status.strip().lower():
                        match = s
                        break

                if not match:
                    print(
                        "Status inválido. Use: Resolvido, Cancelado ou Em Atendimento."
                    )
                    continue

                chamado.status = match
                if match in ["Resolvido", "Cancelado"]:
                    chamado.data_fechamento = datetime.now().strftime("%d/%m/%Y %H:%M")
                else:
                    chamado.data_fechamento = None

                repositorio_chamados.atualizar_chamado(chamado)
                print("Status atualizado!")
            else:
                print("Chamado não encontrado.")

        elif op == "0":
            break


if __name__ == "__main__":
    # Inicialização das tabelas
    repositorio_usuarios.inicializar_arquivo()
    repositorio_tecnicos.inicializar_arquivo()
    repositorio_chamados.inicializar_arquivo()
    menu_principal()
