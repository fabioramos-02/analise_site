import pandas as pd

# Dados de entrada
data = {
    "site": ["Site A", "Site B", "Site C"],
    "performance": [60, 70, 55],
    "acessibilidade": [70, 65, 75],
    "boas_praticas": [75, 60, 80],
    "seo": [70, 65, 90]
}

# Pesos das métricas
pesos = {
    "performance": 0.1,
    "acessibilidade": 0.6,
    "boas_praticas": 0.1,
    "seo": 0.2
}

# Criar DataFrame
df = pd.DataFrame(data)

# Normalizar os valores e calcular o indicador final
df["indicador_final"] = (
    (df["performance"] / 100 * pesos["performance"]) +
    (df["acessibilidade"] / 100 * pesos["acessibilidade"]) +
    (df["boas_praticas"] / 100 * pesos["boas_praticas"]) +
    (df["seo"] / 100 * pesos["seo"])
)

# Converter para porcentagem
df["indicador_final"] = df["indicador_final"] * 100

print(df)
