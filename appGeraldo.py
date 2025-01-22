from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Caminho do ChromeDriver
driver_path = "C:/Users/framos.SEGOV/Downloads/chromedriver.exe"

# Configurando as opções do Chrome
options = Options()
options.add_argument("--headless")  # Executa o navegador em modo headless (opcional)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Configurando o serviço do ChromeDriver
service = Service(driver_path)

# Inicializando o WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL do Access Monitor
base_url = "https://accessmonitor.acessibilidade.gov.pt/"
urls = ["https://www.ms.gov.br/"]  # Lista de URLs para analisar

resultados = []

try:
    for url in urls:
        print(f"Analisando: {url}")
        
        # Acessar a página inicial do Access Monitor
        driver.get(base_url)
        
        # Inserir a URL no campo de entrada
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "url"))
        )
        input_box.clear()
        input_box.send_keys(url)
        
        # Clicar no botão "Validar"
        validate_button = driver.find_element(By.ID, "btn-url")
        validate_button.click()
        
        # Esperar redirecionar para a página de resultados
        WebDriverWait(driver, 20).until(
            EC.url_contains("/results/")
        )

        # Esperar a pontuação aparecer
        pontuacao = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//text[@class='ama-typography-display-6 bold']"))
        ).text
        
        # Aceitáveis
        aceitaveis_total = driver.find_element(By.XPATH, "//td[contains(text(), 'Aceitáveis')]/following-sibling::td[1]").text
        aceitaveis_a = driver.find_element(By.XPATH, "//td[contains(text(), 'Aceitáveis')]/following-sibling::td[2]").text
        aceitaveis_aa = driver.find_element(By.XPATH, "//td[contains(text(), 'Aceitáveis')]/following-sibling::td[3]").text
        aceitaveis_aaa = driver.find_element(By.XPATH, "//td[contains(text(), 'Aceitáveis')]/following-sibling::td[4]").text

        # Para ver manualmente
        manual_total = driver.find_element(By.XPATH, "//td[contains(text(), 'Para ver manualmente')]/following-sibling::td[1]").text
        manual_a = driver.find_element(By.XPATH, "//td[contains(text(), 'Para ver manualmente')]/following-sibling::td[2]").text
        manual_aa = driver.find_element(By.XPATH, "//td[contains(text(), 'Para ver manualmente')]/following-sibling::td[3]").text
        manual_aaa = driver.find_element(By.XPATH, "//td[contains(text(), 'Para ver manualmente')]/following-sibling::td[4]").text

        # Não aceitáveis
        nao_aceitaveis_total = driver.find_element(By.XPATH, "//td[contains(text(), 'Não aceitáveis')]/following-sibling::td[1]").text
        nao_aceitaveis_a = driver.find_element(By.XPATH, "//td[contains(text(), 'Não aceitáveis')]/following-sibling::td[2]").text
        nao_aceitaveis_aa = driver.find_element(By.XPATH, "//td[contains(text(), 'Não aceitáveis')]/following-sibling::td[3]").text
        nao_aceitaveis_aaa = driver.find_element(By.XPATH, "//td[contains(text(), 'Não aceitáveis')]/following-sibling::td[4]").text

        # Adiciona os resultados para a URL
        resultados.append({
            "URL": url,
            "Pontuação": pontuacao,
            "Aceitáveis - Total": aceitaveis_total,
            "Aceitáveis - A": aceitaveis_a,
            "Aceitáveis - AA": aceitaveis_aa,
            "Aceitáveis - AAA": aceitaveis_aaa,
            "Manual - Total": manual_total,
            "Manual - A": manual_a,
            "Manual - AA": manual_aa,
            "Manual - AAA": manual_aaa,
            "Não Aceitáveis - Total": nao_aceitaveis_total,
            "Não Aceitáveis - A": nao_aceitaveis_a,
            "Não Aceitáveis - AA": nao_aceitaveis_aa,
            "Não Aceitáveis - AAA": nao_aceitaveis_aaa,
        })

        print(f"Análise concluída para {url}.")
finally:
    driver.quit()

# Exibindo os resultados
for resultado in resultados:
    print(resultado)
