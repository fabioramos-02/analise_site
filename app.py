import requests
from bs4 import BeautifulSoup
import time
import csv

# Lista de URLs que serão analisadas
urls = [
    "https://www.detran.ms.gov.br/",
    "https://eservicos.sefaz.ms.gov.br/",
]

# URL base do sistema ASES
base_url = "https://asesweb.governoeletronico.gov.br/"

# Cabeçalhos da requisição
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

# Função para analisar um site
def analisar_site(url):
    session = requests.Session()  # Mantém a sessão entre requisições
    resultados = {}

    try:
        # Etapa 1: Enviar a URL para análise (POST)
        inicio = time.time()  # Inicia o cronômetro
        response = session.post(
            f"{base_url}avaliar",
            headers=headers,
            data={"url": url, "executar": "Executar"},
        )
        response.raise_for_status()

        # Etapa 2: Aguardar o carregamento dos resultados
        for _ in range(10):  # Tenta verificar o resultado até 10 vezes
            soup = BeautifulSoup(response.text, "html.parser")
            porcentagem_tag = soup.select_one("#webaxscore span")
            if porcentagem_tag:  # Se os resultados foram carregados, sai do loop
                break
            print("Aguardando o carregamento da página de resultados...")
            time.sleep(2)  # Aguarda 2 segundos antes de tentar novamente
            response = session.get(f"{base_url}avaliar")  # Atualiza a página

        # Extraindo a porcentagem
        porcentagem = porcentagem_tag.text.strip() if porcentagem_tag else "N/A"

        # Extraindo a quantidade de erros e avisos
        total_row = soup.select_one("tr#total")
        if total_row:
            erros = total_row.select_one("td[headers='erro']").text.strip() if total_row.select_one("td[headers='erro']") else "N/A"
            avisos = total_row.select_one("td[headers='aviso']").text.strip() if total_row.select_one("td[headers='aviso']") else "N/A"
        else:
            erros = "N/A"
            avisos = "N/A"

        # Calcula o tempo total de análise
        fim = time.time()
        tempo_analise = round(fim - inicio, 2)

        # Armazena os resultados
        resultados["URL"] = url
        resultados["tempo_analise"] = tempo_analise
        resultados["porcentagem"] = porcentagem
        resultados["quantidade_erros"] = erros
        resultados["quantidade_avisos"] = avisos

    except Exception as e:
        print(f"Erro ao analisar o site {url}: {e}")
        resultados = {
            "URL": url,
            "tempo_analise": "Erro",
            "porcentagem": "Erro",
            "quantidade_erros": "Erro",
            "quantidade_avisos": "Erro",
        }

    return resultados

# Função para salvar os resultados em um CSV
def salvar_csv(resultados, arquivo_csv="resultado_analise.csv"):
    with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["URL", "tempo_analise", "porcentagem", "quantidade_erros", "quantidade_avisos"],
        )
        writer.writeheader()
        writer.writerows(resultados)

# Analisando os sites
todos_resultados = []
for url in urls:
    print(f"Analisando {url}...")
    resultado = analisar_site(url)
    todos_resultados.append(resultado)

# Salvando os resultados no CSV
salvar_csv(todos_resultados)
print("Análise concluída. Resultados salvos em 'resultado_analise.csv'.")
