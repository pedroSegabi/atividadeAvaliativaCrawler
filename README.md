# atividadeAvaliativaCrawler

Breve guia para preparar o ambiente e executar os scripts do repositório.

## Requisitos
- Python 3.10+ (testado com 3.13 no ambiente deste projeto)
- Shell: zsh (comandos abaixo são para zsh)

## 1) Preparar ambiente (virtualenv) e instalar dependências
```bash
cd /Users/pedrosegabi/Desktop/atividadeAvaliativaCrawler
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2) Estrutura esperada
- `crawler.py` — crawler que coleta páginas e salva HTML em `dados_html/`.
- `utils.py` — utilitários: `carregar_grafo()` retorna `(grafo, titulo_para_arquivo)`.
- `grafo_separacao.py` — busca menor caminho entre duas pessoas (CLI).
- `buscar_conexao.py` — ferramentas para buscar conexões entre nós (veja opções abaixo).
- `dados_html/` — HTMLs salvos (gerados pelo crawler ou colocados manualmente).

## 3) Rodar o crawler (opcional)
Atenção: respeite políticas do site, delays e limite `MAX_PAGES` em `crawler.py`.
```bash
# roda com as configurações atuais em crawler.py
python3 crawler.py
```
As páginas coletadas serão salvas em `dados_html/`.

## 4) Carregar e inspecionar o grafo (rápido)
```bash
python3 - <<'PY'
from utils import carregar_grafo
g, m = carregar_grafo()
print('nós:', len(g))
print('arestas:', sum(len(vs) for vs in g.values()))
print('nós com saída:', sum(1 for vs in g.values() if vs))
PY
```

## 5) `grafo_separacao.py` — menor caminho entre duas pessoas
```bash
# busca caminho dirigido (padrão do script)
python3 grafo_separacao.py "Nome A" "Nome B"
# buscar tratando grafo como não-direcionado
python3 grafo_separacao.py "Nome A" "Nome B" --undirected
```
O script normaliza os nomes (underscores/maiúsculas) antes da busca.

## 6) `buscar_conexao.py` — três modos principais
- Distância entre dois nomes (passar dois argumentos):
```bash
python3 buscar_conexao.py "Nome A" "Nome B"
```
- Procurar o primeiro par com grau >= N (passar número):
```bash
python3 buscar_conexao.py 3
```
- Encontrar o par com maior menor-caminho (pode ser lento):
```bash
python3 buscar_conexao.py --longest
```
Observação: no estado atual, `buscar_conexao.py` converte o grafo para NÃO-DIRECIONADO antes das buscas.

## 7) Notas e boas práticas
- O crawler atual salva muitas páginas de categoria (ex.: `Categoria:Pessoas_vivas`) que criam vários links do tipo categoria→pessoa e podem afetar análises dirigidas. Para análises "biografia→biografia" mais fiéis:
  - filtre/exclua arquivos cuja página seja categoria, ou
  - ajuste `utils.carregar_grafo()` para ignorar títulos que comecem com "categoria".
- Para projetos maiores: prefira a API da Wikipedia em vez de scraping direto.

## 8) Problemas comuns
- Erro `ModuleNotFoundError: No module named 'bs4'` — ative o virtualenv e instale dependências (`pip install -r requirements.txt`).

---
