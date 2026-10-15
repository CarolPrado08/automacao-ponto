import os
import random
import time
from playwright.sync_api import sync_playwright

URL_TANGERINO = "https://app.tangerino.com.br/Tangerino/pages/baterPonto/"

def registrar_ponto():
    # Detecta se é teste manual via GitHub Actions para NÃO esperar
    is_manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
    
    if not is_manual:
        tempo_espera = random.randint(10, 120)
        print(f"Execução agendada: Aguardando {tempo_espera} segundos...")
        time.sleep(tempo_espera)
    else:
        print("Execução manual (teste) detectada: Iniciando imediatamente sem espera.")

    company_code = os.environ.get("SOLIDES_COMPANY_CODE", "").strip()
    pin = os.environ.get("SOLIDES_PIN", "").strip()

    if not company_code or not pin:
        raise ValueError("Erro: Os Secrets SOLIDES_COMPANY_CODE ou SOLIDES_PIN não foram encontrados.")

    with sync_playwright() as p:
        print("Iniciando o navegador Chromium...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            geolocation={"latitude": -23.550520, "longitude": -46.633308},
            permissions=["geolocation"]
        )
        page = context.new_page()

        print(f"Acessando a página: {URL_TANGERINO}")
        page.goto(URL_TANGERINO, wait_until="networkidle", timeout=60000)

        # Garante que está na aba Registrar Ponto se houver abas
        if page.is_visible("text=Registrar Ponto"):
            page.click("text=Registrar Ponto")

        print("Preenchendo credenciais...")
        # Localiza o primeiro campo de entrada visível (Código do Empregador)
        inputs = page.locator('input:not([type="hidden"])')
        inputs.nth(0).fill(company_code)
        
        # Localiza o campo de senha/PIN
        page.locator('input[type="password"]').fill(pin)

        print("Clicando no botão Registrar...")
        page.click('button:has-text("Registrar")')

        print("Aguardando confirmação do registro...")
        page.wait_for_timeout(5000)

        # Salva o comprovante em imagem
        page.screenshot(path="comprovante_ponto.png")
        print("Sucesso! Comprovante salvo com sucesso.")

        browser.close()

if __name__ == "__main__":
    registrar_ponto()
