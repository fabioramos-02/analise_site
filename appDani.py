import requests
import pandas as pd

# Lista de URLs para analisar
sites = [
    "https://www.detran.ms.gov.br/",
    "https://www.ms.gov.br/",
    "https://www.sefaz.ms.gov.br/",
    "http://www.saude.ms.gov.br/"
]

# Sua chave da API do WAVE
apikey = "uEYUQ7r44942"

# URL da API do WAVE
wave_api_url = "https://wave.webaim.org/api/request"

# Função para analisar o site usando a API do WAVE
def analyze_with_api(url):
    """Função que realiza a requisição para a API do WAVE e retorna o JSON."""
    payload = {
        'key': apikey,
        'url': url,
        'format': 'json',  # Definir o formato de resposta como JSON
        'reporttype': 1  # Usar reporttype=1 para obter estatísticas básicas
    }
    
    response = requests.get(wave_api_url, params=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Não foi possível obter os dados da análise para {url}"}

# Função para extrair as informações necessárias da resposta da API
def extract_data_from_result(result, url):
    """Extrai as informações de interesse da resposta JSON."""
    if "error" in result:
        return {
            "url": url,
            "status": "Erro",
            "errors_count": None,
            "contrast_errors_count": None,
            "alerts_count": None,
            "features_count": None,
            "structural_elements_count": None,
            "aria_elements_count": None,
            "total_elements": None,
            "analysis_time": None
        }

    stats = result.get("statistics", {})
    categories = result.get("categories", {})

    return {
        "url": url,
        "status": "Sucesso" if result.get("status", {}).get("success") else "Falha",
        "errors_count": categories.get("error", {}).get("count", 0),
        "contrast_errors_count": categories.get("contrast", {}).get("count", 0),
        "alerts_count": categories.get("alert", {}).get("count", 0),
        "features_count": categories.get("feature", {}).get("count", 0),
        "structural_elements_count": categories.get("structure", {}).get("count", 0),
        "aria_elements_count": categories.get("aria", {}).get("count", 0),
        "total_elements": stats.get("totalelements", 0),
        "analysis_time": stats.get("time", 0)
    }

# Função para realizar a análise de todos os sites
def analyze_sites(sites):
    """Realiza a análise para uma lista de sites e retorna os dados extraídos."""
    all_results = []

    for site in sites:
        try:
            print(f"Analisando: {site}")
            result = analyze_with_api(site)
            extracted_data = extract_data_from_result(result, site)
            all_results.append(extracted_data)
        except Exception as e:
            print(f"Erro ao analisar {site}: {e}")

    return all_results

# Analisar todos os sites
all_results = analyze_sites(sites)

# Salvar os resultados em uma planilha
output_file = "wave_analysis_results.xlsx"
df = pd.DataFrame(all_results)
df.to_excel(output_file, index=False)

print(f"Resultados salvos em '{output_file}'.")
