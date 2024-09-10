import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def carregar_dados(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        return json.load(arquivo)

def calcular_faturamento(dados):
    df = pd.DataFrame(dados)

    df_validos = df[df['valor'] > 0]

    if df_validos.empty:
        print("Nenhum dado válido para análise.")
        return df, df_validos, None, None, None

    menor_faturamento = df_validos['valor'].min()
    maior_faturamento = df_validos['valor'].max()

    media_faturamento = df_validos['valor'].mean()

    dias_acima_da_media = df_validos[df_validos['valor'] > media_faturamento].shape[0]

    print(f"Menor valor de faturamento: R${menor_faturamento:,.2f}")
    print(f"Maior valor de faturamento: R${maior_faturamento:,.2f}")
    print(f"Número de dias com faturamento acima da média: {dias_acima_da_media}")

    return df, df_validos, menor_faturamento, maior_faturamento, media_faturamento

def gerar_graficos(df, media_faturamento, menor, maior, diretorio):
    data_atual = datetime.now().strftime("%d-%m-%Y")
    nome_arquivo = f'analise_{data_atual}.png'

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    caminho_arquivo = os.path.join(diretorio, nome_arquivo)

    plt.figure(figsize=(10, 6))
    plt.plot(df['dia'], df['valor'], label="Faturamento Diário", color="blue", marker='o')
    plt.axhline(y=media_faturamento, color='red', linestyle='--', label="Média Mensal")
    
    if menor is not None and maior is not None:
        menor_dia = df[df['valor'] == menor]['dia'].values[0]
        plt.annotate(f'Menor: R${menor:,.2f}', xy=(menor_dia, menor), xytext=(menor_dia, menor + 5000),
                     arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10, color='green')
        
        maior_dia = df[df['valor'] == maior]['dia'].values[0]
        plt.annotate(f'Maior: R${maior:,.2f}', xy=(maior_dia, maior), xytext=(maior_dia, maior - 10000),
                     arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, color='red')

    plt.title("Faturamento Diário da Distribuidora")
    plt.xlabel("Dia")
    plt.ylabel("Valor do Faturamento")
    plt.legend()
    plt.grid(True)
    plt.xticks(range(1, 31), rotation=45) 
    plt.tight_layout()

    plt.savefig(caminho_arquivo)
    
    plt.show()

def main():
    caminho_arquivo = 'dados/dados.json'  
    diretorio_salvar = 'graficos'  

    dados_faturamento = carregar_dados(caminho_arquivo)
    
    df, df_validos, menor, maior, media = calcular_faturamento(dados_faturamento)
    
    gerar_graficos(df, media, menor, maior, diretorio_salvar)

if __name__ == "__main__":
    main()
