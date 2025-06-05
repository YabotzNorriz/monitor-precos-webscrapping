import requests
from bs4 import BeautifulSoup


def monitorar_preco(url, limite_alerta):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        nome = soup.select_one("#productTitle")
        if nome:
            nome = nome.get_text().strip()
        else:
            nome = "Nome não encontrado (mudou o seletor?)"

        preco_element = soup.select_one(".a-price-whole")
        if preco_element:
            preco = float(preco_element.get_text().replace(".", "").replace(",", "."))
        else:
            preco = 0.0
            print(
                "Preço não encontrado. Verifique o seletor ou se a página foi bloqueada."
            )

        print(f"Produto: {nome} | Preço: R${preco:.2f}")

        if preco <= limite_alerta:
            enviar_alerta(nome, preco, url)

    except Exception as e:
        print(f"Erro ao acessar a página: {e}")


def enviar_alerta(nome, preco, url):
    print(f"ALERTA DE PREÇO: {nome} por R${preco:.2f} | URL: {url}")


url = "https://www.amazon.com.br/Notebook-Lenovo-Ryzen-7335U-Windows/dp/B0DWBS2FCN"
monitorar_preco(url, 4000.00)
