import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def calcular_percentuais(faturamento_por_estado):
    df = pd.DataFrame(faturamento_por_estado.items(), columns=['Estado', 'Faturamento'])
    
    total_faturamento = df['Faturamento'].sum()
    
    df['Percentual'] = (df['Faturamento'] / total_faturamento) * 100

    print(df)

    return df, total_faturamento

def gerar_grafico_pizza(df, total_faturamento, diretorio):
    data_atual = datetime.now().strftime("%d-%m-%Y")
    nome_arquivo = f'percentuais_{data_atual}.png'

    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    caminho_arquivo = os.path.join(diretorio, nome_arquivo)

    plt.figure(figsize=(10, 7))
    plt.pie(df['Percentual'], labels=df['Estado'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(df))))
    plt.title(f'Percentual de Faturamento por Estado - Total: R${total_faturamento:,.2f}')
    plt.axis('equal')  

    plt.savefig(caminho_arquivo)
    
    plt.show()

def main():
    faturamento_por_estado = {
        'SP': 67836.43,
        'RJ': 36678.66,
        'MG': 29229.88,
        'ES': 27165.48,
        'Outros': 19849.53
    }
    
    diretorio_salvar = 'graficos' 

    df, total_faturamento = calcular_percentuais(faturamento_por_estado)
    
    gerar_grafico_pizza(df, total_faturamento, diretorio_salvar)

if __name__ == "__main__":
    main()
