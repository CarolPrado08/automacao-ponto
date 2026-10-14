import os
import random
import time
from playwright.sync_api import sync_playwright

URL_TANGERINO = "https://app.tangerino.com.br/Tangerino/pages/baterPonto/"

def registrar_ponto():
    # 1. Coloca a espera aleatória logo no início da função
    # Sorteia entre 10 e 120 segundos para não bater exatamente no mesmo segundo todo dia
    tempo_espera = random.randint(10, 120)
    print(f"Aguardando {tempo_espera} segundos antes de iniciar...")
    time.sleep(tempo_espera)

    # 2. Carrega as credenciais dos Secrets
    company_code = os.environ.get("SOLIDES_COMPANY_CODE", "")
    pin = os.environ.get("SOLIDES_PIN", "")

    if not company_code or not pin:
        raise ValueError("Erro: Variáveis SOLIDES_COMPANY_CODE ou SOLIDES_PIN não encontradas!")

    # 3. Abre o navegador e faz as ações no site
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            geolocation={"latitude": -23.550520, "longitude": -46.633308},
            permissions=["geolocation"]
        )
        page = context.new_page()

        print("Acessando a página de registro de ponto...")
        page.goto(URL_TANGERINO, wait_until="networkidle")

        if page.is_visible("text=Registrar Ponto"):
            page.click("text=Registrar Ponto")

        print("Preenchendo credenciais...")
        page.fill('input[placeholder*="Código"], input[name*="code"], input:nth-child(1)', company_code)
        page.fill('input[type="password"], input[name*="pin"]', pin)

        print("Clicando em Registrar...")
        page.click('button:has-text("Registrar")')

        page.wait_for_timeout(5000)
        page.screenshot(path="comprovante_ponto.png")
        print("Ponto registrado com sucesso!")

        browser.close()

if __name__ == "__main__":
    registrar_ponto()
