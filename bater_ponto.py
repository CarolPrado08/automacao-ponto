import os
import random
import time
from playwright.sync_api import sync_playwright

# Sorteia uma pequena variação (entre 10 e 120 segundos) para não registrar no exato mesmo segundo todos os dias
time.sleep(random.randint(10, 120))

# Link do Tangerino / Sólides Ponto
URL_TANGERINO = "https://app.tangerino.com.br/Tangerino/pages/baterPonto/"

def registrar_ponto():
    company_code = os.environ.get("SOLIDES_COMPANY_CODE", "")
    pin = os.environ.get("SOLIDES_PIN", "")

    if not company_code or not pin:
        raise ValueError("Erro: As variáveis SOLIDES_COMPANY_CODE ou SOLIDES_PIN não foram configuradas nos Secrets do GitHub!")

    with sync_playwright() as p:
        # Abre o navegador em modo headless (segundo plano)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            geolocation={"latitude": -23.550520, "longitude": -46.633308},
            permissions=["geolocation"]
        )
        page = context.new_page()

        # 1. Acessa a página do Tangerino
        print("Acessando a página de registro de ponto...")
        page.goto(URL_TANGERINO, wait_until="networkidle")

        # 2. Garante que a aba 'Registrar Ponto' esteja selecionada, se visível
        if page.is_visible("text=Registrar Ponto"):
            page.click("text=Registrar Ponto")

        # 3. Preenche o Código do Empregador e o PIN
        print("Preenchendo o Código do Empregador e PIN...")
        page.fill('input[placeholder*="Código"], input[name*="code"], input:nth-child(1)', company_code)
        page.fill('input[type="password"], input[name*="pin"]', pin)

        # 4. Clica no botão Registrar
        print("Clicando em Registrar...")
        page.click('button:has-text("Registrar")')

        # 5. Aguarda a confirmação e tira print
        page.wait_for_timeout(5000)
        page.screenshot(path="comprovante_ponto.png")
        print("Ponto registrado com sucesso! Comprovante salvo.")

        browser.close()

if __name__ == "__main__":
    registrar_ponto()
