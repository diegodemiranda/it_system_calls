import sys
from pathlib import Path


def _ensure_src_in_path():
    # insere a pasta src no sys.path para permitir imports locais
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / "src"
    sys.path.insert(0, str(src_path))


_ensure_src_in_path()

import repositorio_usuarios as ru
import repositorio_tecnicos as rt
import repositorio_chamados as rc
from models import Usuario, Tecnico, Chamado


def test_repositorios_basic_flow(tmp_path, monkeypatch):
    # isola execução no diretório temporário
    monkeypatch.chdir(tmp_path)

    # inicializa arquivos
    ru.inicializar_arquivo()
    rt.inicializar_arquivo()
    rc.inicializar_arquivo()

    assert (tmp_path / "data" / "usuarios.csv").exists()
    assert (tmp_path / "data" / "tecnicos.csv").exists()
    assert (tmp_path / "data" / "chamados.csv").exists()

    # cria usuário
    uid = ru.gerar_novo_id()
    u = Usuario(uid, "Test User", "test@example.com", "TI")
    ru.salvar(u)
    usuarios = ru.listar_todos()
    assert len(usuarios) == 1
    assert usuarios[0].email == "test@example.com"

    # cria técnico
    tid = rt.gerar_novo_id()
    t = Tecnico(tid, "Tech", "tech@example.com", "Rede")
    rt.salvar(t)
    tecnicos = rt.listar_todos()
    assert len(tecnicos) == 1
    assert tecnicos[0].especialidade == "Rede"

    # cria chamado
    cid = rc.gerar_novo_id()
    c = Chamado(
        cid, uid, "Titulo do Problema", "Descrição detalhada suficiente", "Alta"
    )
    rc.salvar_novo(c)
    chamados = rc.listar_todos()
    assert len(chamados) == 1

    # atribui técnico e atualiza chamado
    ch = chamados[0]
    ch.tecnico_id = tid
    ch.status = "Em Atendimento"
    assert rc.atualizar_chamado(ch) is True

    buscado = rc.buscar_por_id(cid)
    assert buscado is not None
    assert buscado.tecnico_id == tid
    assert buscado.status == "Em Atendimento"

    # fecha chamado
    buscado.status = "Resolvido"
    rc.atualizar_chamado(buscado)
    fechado = rc.buscar_por_id(cid)
    assert fechado.status == "Resolvido"
    assert fechado.data_fechamento is not None
