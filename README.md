# IT System Calls 🧑🏾‍💻

Projeto CLI simples para gestão de chamados de suporte de TI usando arquivos CSV como persistênci realizado como projeto no Laboratório Interdisciplinar de Processamento e Análise de Imagens - LIPAI.

## Sumário

- **Visão Geral**
- **Estrutura do Repositório**
- **Modelos de Dados**
- **Como Rodar**
- **Fluxos Principais**
- **Persistência (CSV)**
- **Pontos Importantes / Dívida Técnica**
- **Contribuindo**
- **Próximos Passos Sugeridos**

## Visão Geral

Este projeto implementa um sistema de chamados (tickets) em linha de comando para centralizar solicitações de suporte técnico. É intencionalmente leve: não usa banco de dados, grava todos os dados em arquivos CSV dentro da pasta `data/`. O objetivo é ser um exemplo didático de um pequeno sistema CRUD com repositórios, modelos e relatórios.

Tecnologias / requisitos:

- Python 3.9+

## Estrutura do Repositório

- `src/` — código fonte principal
  - `main.py` — interface de linha de comando e fluxo principal
  - `models.py` — classes de domínio (`Usuario`, `Tecnico`, `Chamado`)
  - `repositorio_usuarios.py` — operações CRUD para usuários
  - `repositorio_tecnicos.py` — operações CRUD para técnicos
  - `repositorio_chamados.py` — operações de criação/atualização/listagem de chamados
  - `relatorios.py` — funções de leitura/filtragem para relatórios
- `data/` — arquivos CSV de persistência
  - `usuarios.csv`, `tecnicos.csv`, `chamados.csv`
- `tests/` — testes automatizados com pytest
  - `test_repositorios.py` — testes do fluxo básico de CRUD
- `scripts/` — utilitários de inicialização
  - `init_sample_data.py` — popula `data/` com registros de exemplo
- `pyproject.toml` — metadados do projeto
- `requirements.txt`, `requirements-dev.txt` — dependências

## Modelos de Dados

As três entidades principais são:

- `Usuario`: id, nome, email, setor
- `Tecnico`: id, nome, email, especialidade
- `Chamado`: id, usuario_id, titulo, descricao, prioridade, status, tecnico_id, data_abertura, data_fechamento

IDs são gerados sequencialmente lendo o CSV e retornando `max_id + 1`.

Estados válidos de `Chamado.status` (usados na CLI):

- `Aberto` (inicial)
- `Em Atendimento`
- `Resolvido`
- `Cancelado`

Ao fechar um chamado (`Resolvido` ou `Cancelado`), o campo `data_fechamento` é preenchido com timestamp no formato `dd/mm/YYYY HH:MM`.

## Como Rodar

1. Certifique-se de ter Python 3.9+ instalado.
2. Execute a aplicação CLI:

```bash
python src/main.py
```

**Observações:**

- Ao iniciar, os repositórios chamam `inicializar_arquivo()` para criar os CSV com cabeçalhos caso não existam.
- Os arquivos CSV ficam em `data/` (relativo à raiz do projeto).
- Para pré-popular dados de exemplo: `python scripts/init_sample_data.py`
- Para rodar testes: `pip install -r requirements-dev.txt && pytest -q`

## Fluxos Principais (CLI)

- Gerenciar Usuários: cadastrar e listar usuários.
- Gerenciar Técnicos: cadastrar e listar técnicos.
- Abrir Chamado: selecionar usuário, informar título, descrição e prioridade.
- Gestão de Chamados: listar chamados abertos, listar por usuário/técnico, atribuir técnico, atualizar status (resolver/cancelar).

Validações básicas na CLI incluem: tamanho mínimo de campos (nome, título, descrição), formato simples de e-mail e validação de prioridades.

## Persistência (CSV)

- Criação de novos registros: os repositórios usam append para novos registros.
- Atualizações de chamados: para atualizar um chamado existente, o repositório lê todo o CSV, substitui o registro e regrava o arquivo completo.

Formato de cabeçalhos:

- `data/usuarios.csv`: `id,nome,email,setor`
- `data/tecnicos.csv`: `id,nome,email,especialidade`
- `data/chamados.csv`: `id,usuario_id,titulo,descricao,prioridade,status,tecnico_id,data_abertura,data_fechamento`

## Pontos Importantes / Dívida Técnica

1. **Geração de ID**: é sequencial lendo o arquivo; isso produz condições de corrida se houver múltiplas instâncias concorrentes.
2. **`tecnico_id` vazio**: é salvo como string vazia `""` no CSV; o modelo converte isso para `None` internamente.
3. **Validações básicas**: e-mail usa regex simples, sem verificação robusta ou DNS.
4. **Tratamento de exceções**: repositórios possuem tratamento básico de I/O; melhorias possíveis em operações de escrita.
5. **Atomicidade de atualização**: chamados usam arquivo temporário (`FILE_PATH + '.tmp'`) para atualização atômica via `os.replace()`.

## Contribuindo

Se quiser contribuir:

- Siga o padrão existente: cada entidade tem um repositório (`repositorio_*.py`) e o modelo em `models.py`.
- Ao adicionar features que precisam alterar registros existentes, mantenha a estratégia atual (ler e regravar CSV) ou considere migrar para um pequeno banco (SQLite) se desejar concorrência/segurança.
- Adicione testes em `tests/` (use pytest) e atualize/execute via: `pytest -q`
- Para ambientes de desenvolvimento, instale: `pip install -r requirements-dev.txt`

Próximos Passos:

- Validar dados de entrada mais rigorosamente (emails, datas).
- Adicionar mensagens de feedback mais descritivas em caso de erro.
- - Adicionar GitHub Actions para executar testes automaticamente.
- - Para concorrência segura migrar persistência para SQLite ou banco relacional.
- Considerar API REST (FastAPI/Flask) para acesso programático.


## Como Rodar Testes

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Rodar testes
pytest -q

# Rodar com cobertura de código (opcional, requer pytest-cov)
pytest --cov=src tests/
```

## Inicializar Dados de Exemplo

```bash
python scripts/init_sample_data.py
```

Isso cria registros de exemplo em `data/usuarios.csv`, `data/tecnicos.csv` e `data/chamados.csv` (apenas se os arquivos estiverem vazios).
