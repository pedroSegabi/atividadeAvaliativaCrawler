import requests
from bs4 import BeautifulSoup
import os
import time
import re
import random

# Configurações
START_URL = "https://pt.wikipedia.org/wiki/Categoria:Pessoas_vivas"
OUTPUT_DIR = "dados_html"
MAX_PAGES = 200   # ajuste para 1000 quando for rodar de verdade
VISITED = set()
COLLECTED = 0

# Cabeçalho para simular navegador real e evitar bloqueio
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/119.0.0.0 Safari/537.36"
}

# Regex para identificar se a página é de pessoa
PERSON_REGEX = re.compile(r"(?:nascid[ao]|falecid[ao]|é um[ao]|\bé\b.*(ator|atriz|político|cantor|escritor|cientista))", re.IGNORECASE)

def is_person_page(soup):
    """Verifica se a página da Wikipédia é sobre uma pessoa."""
    content = soup.get_text(" ", strip=True)
    return bool(PERSON_REGEX.search(content))

def save_page(name, html):
    """Salva o HTML em arquivo com nome baseado na pessoa."""
    safe_name = re.sub(r"[^\w\s-]", "", name).replace(" ", "_")
    path = os.path.join(OUTPUT_DIR, f"{safe_name}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def get_links(soup):
    """Extrai links internos da Wikipédia."""
    links = []
    for a in soup.select("a[href^='/wiki/']"):
        href = a["href"]
        # filtrar links que não são artigos
        if ":" not in href and not href.startswith("/wiki/Wikipédia:"):
            links.append("https://pt.wikipedia.org" + href)
    return links

def crawl(start_url):
    global COLLECTED
    to_visit = [start_url]

    while to_visit and COLLECTED < MAX_PAGES:
        url = to_visit.pop(0)

        if url in VISITED:
            continue
        VISITED.add(url)

        try:
            print(f"🔎 Coletando: {url}")
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                print(f"❌ Erro {resp.status_code} em {url}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("h1").get_text()

            # Se for uma pessoa, salvar
            if is_person_page(soup):
                save_page(title, resp.text)
                COLLECTED += 1
                print(f"✅ Página de pessoa salva: {title} ({COLLECTED}/{MAX_PAGES})")

            # Pega novos links e embaralha (para não seguir sempre o mesmo padrão)
            links = get_links(soup)
            random.shuffle(links)
            for link in links:
                if link not in VISITED:
                    to_visit.append(link)

            # Pausa para não sobrecarregar servidor
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Erro ao processar {url}: {e}")

    print(f"\n✅ Coleta finalizada. {COLLECTED} páginas salvas em {OUTPUT_DIR}/")
    print(f"ℹ️ Páginas visitadas: {len(VISITED)}")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    crawl(START_URL)
