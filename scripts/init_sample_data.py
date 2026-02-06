#!/usr/bin/env python3
"""Script de inicialização que popula a pasta `data/` com registros de exemplo.

Uso:
    python scripts/init_sample_data.py
"""
import sys
from pathlib import Path


def _ensure_src_in_path():
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / 'src'
    sys.path.insert(0, str(src_path))


_ensure_src_in_path()

import repositorio_usuarios as ru
import repositorio_tecnicos as rt
import repositorio_chamados as rc
from models import Usuario, Tecnico, Chamado


def main():
    ru.inicializar_arquivo()
    rt.inicializar_arquivo()
    rc.inicializar_arquivo()

    # Popula usuários se vazio
    if not ru.listar_todos():
        u1 = Usuario(ru.gerar_novo_id(), 'Alice Silva', 'alice@example.com', 'Financeiro')
        ru.salvar(u1)
        u2 = Usuario(ru.gerar_novo_id(), 'Bruno Lima', 'bruno@example.com', 'TI')
        ru.salvar(u2)

    # Popula técnicos se vazio
    if not rt.listar_todos():
        t1 = Tecnico(rt.gerar_novo_id(), 'Carlos Tech', 'carlos@example.com', 'Redes')
        rt.salvar(t1)
        t2 = Tecnico(rt.gerar_novo_id(), 'Daniela Sys', 'daniela@example.com', 'Sistemas')
        rt.salvar(t2)

    # Popula chamados se vazio
    if not rc.listar_todos():
        users = ru.listar_todos()
        user_id = users[0].id if users else 1
        c1 = Chamado(rc.gerar_novo_id(), user_id, 'Impressora não funciona', 'A impressora do setor X não imprime mais.', 'Alta')
        rc.salvar_novo(c1)

    print('Dados de exemplo criados em data/')


if __name__ == '__main__':
    main()
