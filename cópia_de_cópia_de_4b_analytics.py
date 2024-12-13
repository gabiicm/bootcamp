# -*- coding: utf-8 -*-
"""Cópia de Cópia de 4B Analytics.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RNmnNWHeVI7H6s9FAuK6Fq7mPTrqwEGw
"""

# ARRUMAR XLS PARA XLSX
#!apt-get install --yes libreoffice


import pandas as pd
import os
import matplotlib.pyplot as plt


# Fazer o upload de múltiplos arquivos .xls
print("Faça o upload de um ou mais arquivos .xls:")
uploaded = files.upload()

# Processar cada arquivo carregado
for file_name, file_content in uploaded.items():
    # Salvar o arquivo original no sistema de arquivos
    with open(file_name, "wb") as f:
        f.write(file_content)

    # Converter o arquivo .xls para .xlsx usando LibreOffice
    os.system(f'libreoffice --headless --convert-to xlsx "{file_name}"')

    # Ler o arquivo convertido (agora .xlsx) e remover as 4 primeiras linhas do cabeçalho
    novo_nome = file_name.replace('.xls', '.xlsx')
    df = pd.read_excel(novo_nome) 
    '''<-inserir , skiprows=4 pra remover

    # Renomear as colunas
    df.columns = ['Data/Hora', 'Chuva', 'Nivel', 'Vazao', 'Bateria', 'Temp']

    # Tratar a coluna "Data/Hora" como data usando pd.to_datetime
    df['Data/Hora'] = pd.to_datetime(df['Data/Hora'], errors='coerce')
    '''

    # Salvar o arquivo processado como um novo .xlsx
    arquivo_processado = novo_nome.replace('.xlsx', '_atualizado.xlsx')
    df.to_excel(arquivo_processado, index=False)

    # Fazer o download do arquivo processado
    print(f"Download do arquivo atualizado ({arquivo_processado}):")
    files.download(arquivo_processado)

from google.colab import files
uploaded = files.upload()

#!pip install openpyxl

import pandas as pd

encantado = pd.read_excel('encantado.xlsx')
santa_tereza = pd.read_excel('santa_tereza.xlsx')
mucum = pd.read_excel('mucum.xlsx')

print("Dados Encantado")
print(encantado.head())

print("\nDados Santa Tereza")
print(santa_tereza.head())

print("\nDados Muçum")
print(mucum.head())

santa_tereza = pd.read_excel('santa_tereza.xlsx', parse_dates=['Data/Hora'])
mucum = pd.read_excel('mucum.xlsx', parse_dates=['Data/Hora'])
encantado = pd.read_excel('encantado.xlsx', parse_dates=['Data/Hora'])

# Valores faltantes
na_counts = santa_tereza.isna().sum()
print('Santa Tereza:\n', na_counts)

na_counts = mucum.isna().sum()
print('Muçum:\n', na_counts)

na_counts = encantado.isna().sum()
print('Encantado:\n', na_counts)

# Excluir a variável 'vazão' para Santa Tereza (não tem nada preenchido)
santa_tereza.drop(columns=['Vazao'], inplace=True, errors='ignore')

# Mesclar Dados das Estações
df = pd.merge(pd.merge(santa_tereza, mucum, on='Data/Hora', suffixes=('_santa', '_mucum')), encantado, on='Data/Hora')
df.rename(columns={'chuva': 'chuva_encantado', 'nivel': 'nivel_encantado'}, inplace=True)
df.rename(columns={'Vazao_x': 'Vazao_Mucum'}, inplace=True)
df

df.info()
descritivas = df.describe().transpose()
print(descritivas)

from tabulate import tabulate
print(tabulate(descritivas, headers='keys', tablefmt='grid'))

import matplotlib.pyplot as plt
import seaborn as sns

variaveis = ['Nivel_santa', 'Nivel_mucum', 'Nivel', 'Vazao_Mucum', 'Vazao_y']
titulos = ['Nível Santa Tereza', 'Nível Muçum', 'Nível Encantado', 'Vazão Muçum', 'Vazão Encantado']
fig, axes = plt.subplots(2, 3, figsize=(9, 6))


for i, var in enumerate(variaveis):
    row = i // 3
    col = i % 3

    sns.histplot(df[var], kde=True, bins=30, ax=axes[row, col])
    axes[row, col].set_title(f'Histograma de {titulos[i]}')
    axes[row, col].set_xlabel(titulos[i])
    axes[row, col].set_ylabel('Frequência')
plt.tight_layout()
plt.show()

import pandas as pd

# datetime
df['Data/Hora'] = pd.to_datetime(df['Data/Hora'], format='%d/%m/%Y %H:%M:%S', dayfirst=True, errors='coerce')


plt.figure(figsize=(9, 5))
plt.plot(df['Data/Hora'], df['Nivel'], label='Encantado', color='blue', linewidth=2)
plt.plot(df['Data/Hora'], df['Nivel_mucum'], label='Muçum', color='orange', linewidth=2)
plt.plot(df['Data/Hora'], df['Nivel_santa'], label='Santa Tereza', color='green', linewidth=2)

plt.title('Nível do Rio')
plt.xlabel('Data/Hora')
plt.ylabel('Nível do Rio (cm)')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()


plt.show()

#número de NaN
na_counts = df.isna().sum()
print(na_counts)

df['Data/Hora'] = pd.to_datetime(df['Data/Hora'])

df.set_index('Data/Hora', inplace=True)
fig, ax1 = plt.subplots(figsize=(14, 7))

# Gráfico de linha para o nível
ax1.plot(df.index, df['Nivel'], color='blue', label='Nível Encantado')
ax1.set_xlabel('Data/Hora')
ax1.set_ylabel('Nível (m)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# segundo eixo y para a vazão
ax2 = ax1.twinx()
ax2.bar(df.index, df['Vazao_y'], color='green', alpha=0.3, label='Vazão Encantado')
ax2.set_ylabel('Vazão (m³/s)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

plt.title('Nível e Vazão em Encantado ao Longo do Tempo')
fig.tight_layout()
plt.show()

# Boxplot das variáveis
import seaborn as sns
import matplotlib.pyplot as plt

variaveis = ['Vazao_Mucum', 'Nivel_mucum', 'Nivel_santa', 'Nivel', 'Vazao_y']
variaveis_renomeadas = ['Vazão Muçum', 'Nível Muçum', 'Nível Santa Tereza', 'Nível Encantado', 'Vazão encantado']

if all(var in df.columns for var in variaveis):
    df_boxplot = df[variaveis].copy()
    df_boxplot.columns = variaveis_renomeadas

    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df_boxplot, palette="Set2")
    plt.title('Boxplot das Variáveis')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("Algumas colunas não estão no DataFrame.")

# Renomeando as variáveis de acordo com as estações
df_renomeado = df.rename(columns={
    'Chuva_santa': 'Chuva Santa Tereza',
    'Nivel_santa': 'Nível Santa Tereza',
    'Bateria_santa': 'Bateria Santa Tereza',
    'Temp_santa': 'Temp. Santa Tereza',
    'Chuva_mucum': 'Chuva Muçum',
    'Nivel_mucum': 'Nível Muçum',
    'Vazao_Mucum': 'Vazão Muçum',
    'Bateria_mucum': 'Bateria Muçum',
    'Temp_mucum': 'Temp. Muçum',
    'Chuva': 'Chuva Encantado',
    'Nivel': 'Nível Encantado',
    'Vazao_y': 'Vazão Encantado',
    'Bateria': 'Bateria Encantado',
    'Temp': 'Temp. Encantado'
})

# Excluindo a coluna 'Data/Hora' antes de calcular a matriz de correlação
df_renomeado_sem_data = df_renomeado.drop(columns=['Data/Hora'])

# Matriz de correlação
plt.figure(figsize=(9, 6))
corr_matrix = df_renomeado_sem_data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Matriz de Correlação')
plt.show()

# Matriz de correlação como uma tabela
from tabulate import tabulate
print(tabulate(corr_matrix, headers='keys', tablefmt='grid'))

#correto
# Preenchendo valores ausentes de chuva com a moda
df['Chuva_santa'] = df['Chuva_santa'].fillna(df['Chuva_santa'].mode()[0])
df['Chuva_mucum'] = df['Chuva_mucum'].fillna(df['Chuva_mucum'].mode()[0])
df['Chuva'] = df['Chuva'].fillna(df['Chuva'].mode()[0])  # Para chuva em Encantado

# Aplicando interpolação para os níveis e vazões
print("Antes da imputação:")
print(df[['Nivel_santa','Nivel_mucum', 'Nivel']].describe())
df['Nivel_santa'] = df['Nivel_santa'].interpolate()
df['Nivel_mucum'] = df['Nivel_mucum'].interpolate()
df['Nivel'] = df['Nivel'].interpolate()  # Para nível em Encantado
print("Depois da imputação")
print(df[['Nivel_santa','Nivel_mucum', 'Nivel']].describe())

print("antes da imputação:")
print(df[['Vazao_Mucum']])
df['Vazao_Mucum'] = df['Vazao_Mucum'].interpolate()
print("depois da imputação:")

print(df[['Vazao_Mucum']])
if df.index.isnull().any():
    df = df[~df.index.isnull()]

# Método mais robusto
df['Vazao_y'] = df['Vazao_y'].interpolate(method='polynomial', order=2)

if df['Vazao_y'].isnull().sum() > 0:
    # Preenchendo qualquer valor ausente remanescente com a média
    df['Vazao_y'] = df['Vazao_y'].fillna(df['Vazao_y'].mean())

#NÃO RODA ESSE!!!!!!!!!!!!!!!!!!
# Preenchendo valores ausentes de chuva com a moda
df['Chuva_santa'] = df['Chuva_santa'].fillna(df['Chuva_santa'].mode()[0])
df['Chuva_mucum'] = df['Chuva_mucum'].fillna(df['Chuva_mucum'].mode()[0])
df['Chuva'] = df['Chuva'].fillna(df['Chuva'].mode()[0])  # Para chuva em Encantado

# Importando o KNNImputer
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)

# Imputando as variáveis de Vazão
df[['Vazao_Mucum', 'Vazao_y']] = imputer.fit_transform(df[['Vazao_Mucum', 'Vazao_y']])
print("Antes da imputação:")
print(df[['Vazao_Mucum', 'Vazao_y']].describe())

# Estatísticas após a imputação
print("\nApós a imputação:")
print(df[['Vazao_Mucum', 'Vazao_y']].describe())


imputer = KNNImputer(n_neighbors=5)
df[['Nivel_santa', 'Nivel_mucum', 'Nivel']] = imputer.fit_transform(df[['Nivel_santa', 'Nivel_mucum', 'Nivel']])

# Verificando as estatísticas antes e depois da imputação
print("Antes da imputação:")
print(df[['Nivel_santa', 'Nivel_mucum', 'Nivel']].describe())

# Estatísticas após a imputação
print("\nApós a imputação:")
print(df[['Nivel_santa', 'Nivel_mucum', 'Nivel']].describe())

print("Valores ausentes após o tratamento:")
print(df.isnull().sum())

df = df.dropna(subset=['Data/Hora'])

plt.figure(figsize=(9, 5))
plt.plot(df['Data/Hora'], df['Nivel'], label='Encantado', color='blue', linewidth=2)
plt.plot(df['Data/Hora'], df['Nivel_mucum'], label='Muçum', color='orange', linewidth=2)
plt.plot(df['Data/Hora'], df['Nivel_santa'], label='Santa Tereza', color='green', linewidth=2)


plt.title('Nível do Rio')
plt.xlabel('Data/Hora')
plt.ylabel('Nível do Rio (cm)')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()


plt.show()

# Matriz de correlação
plt.figure(figsize=(12, 8))
corr_matrix = df_renomeado_sem_data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Matriz de Correlação')
plt.show()

df.info()
descritivas = df.describe().transpose()
print(descritivas)

from tabulate import tabulate
print(tabulate(descritivas, headers='keys', tablefmt='grid'))

plt.figure(figsize=(12, 6))
plt.plot(df['Data/Hora'], df['Nivel'], label='Nível Encantado', color='blue')
plt.plot(df['Data/Hora'], df['Vazao_y'], label='Vazão Encantado', color='orange')
plt.xlabel('Data/Hora')
plt.ylabel('Valor')
plt.legend()
plt.title('Nível vs Vazão')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt

# gráfico de dispersão entre a vazão e o nível de Encantado
plt.figure(figsize=(10, 6))
plt.scatter(df['Vazao_Mucum'], df['Nivel'], color='blue', alpha=0.5)


plt.title('Relação entre Vazão e Nível do Rio Encantado', fontsize=14)
plt.xlabel('Vazão (m³/s)', fontsize=12)
plt.ylabel('Nível do Rio Encantado (cm)', fontsize=12)
plt.tight_layout()
plt.show()

#SALVA BASE DE DADOS
#df.to_excel('/content/drive/My Drive/df.xlsx', index=False)

#A PARTIR DAQUI ##################################################################
#df = pd.read_excel('/content/drive/My Drive/df.xlsx')

#ARRUMANDO DADOS


df.reset_index(inplace=True)
try:
    # Tentativa de remover as colunas
    df.drop(columns=['level_0', 'index'], inplace=True)
except KeyError:
    # Caso as colunas não existam
    print("Não tinha as colunas 'level_0' ou 'index'.")
else:
  print("top")

from prophet import Prophet
import pandas as pd


#separa data e hora e cria media da altura do rio por dia


df['Data/Hora'] = pd.to_datetime(df['Data/Hora'], format='%d/%m/%Y %H:%M:%S', dayfirst=True, errors='coerce')
df['Data'] = df['Data/Hora'].dt.date
df['Hora'] = df['Data/Hora'].dt.time


df = df.dropna(subset=['Data/Hora'])

################# fazer aqui para o cenario otimista e pessimista
df['media_nivel_dia_mucum'] = df.groupby('Data')['Nivel_mucum'].transform('mean')
df['media_nivel_dia_encantado'] = df.groupby('Data')['Nivel'].transform('mean')
df['media_nivel_dia_santa'] = df.groupby('Data')['Nivel_santa'].transform('mean')

df['media_vazao_dia_mucum'] = df.groupby('Data')['Vazao_Mucum'].transform('mean')
df['media_vazao_dia_encantado'] = df.groupby('Data')['Vazao_y'].transform('mean')

df['soma_chuva_dia_mucum'] = df.groupby('Data')['Chuva_mucum'].transform('sum')
df['soma_chuva_dia_encantado'] = df.groupby('Data')['Chuva'].transform('sum')
df['soma_chuva_dia_santa'] = df.groupby('Data')['Chuva_santa'].transform('sum')

df['media_temp_dia_mucum'] = df.groupby('Data')['Temp_mucum'].transform('mean')
df['media_temp_dia_encantado'] = df.groupby('Data')['Temp'].transform('mean')
df['media_temp_dia_santa'] = df.groupby('Data')['Temp_santa'].transform('mean')

#df.drop(columns=['Data/Hora'], inplace=True)


df_sem_duplicado = df.drop_duplicates(subset='Data') #altera tudo pra deslocar as independependentes
df_compara = df.drop_duplicates(subset='Data') #nao sofreu nenhuma alteracao ate uma hora tirar o ultimo valor
original = df.drop_duplicates(subset='Data') # backup

#Todos os niveis - por dia
plt.figure(figsize=(12, 6))
plt.plot(df_sem_duplicado['Data'], df_sem_duplicado['media_nivel_encantado'], label='Nível Encantado', color='blue')
plt.plot(df_sem_duplicado['Data'], df_sem_duplicado['media_nivel_mucum'], label='Nível Muçum', color='orange')
plt.plot(df_sem_duplicado['Data'], df_sem_duplicado['media_nivel_santa'], label='Nível Santa Tereza', color='pink')
plt.xlabel('Data/Hora')
plt.ylabel('Valor')
plt.legend()
plt.title('Níveis de todas as cidades por dia')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

#Entre todos os niveis e chuvas - por dia
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plota o Nível Encantado no eixo y da esquerda (ax1)
ax1.plot(df_sem_duplicado['Data'], df_sem_duplicado['media_nivel_encantado'], label='Nível Encantado', color='#0CF')
ax1.plot(df_sem_duplicado['Data'], df_sem_duplicado['media_nivel_mucum'], label='Nível Muçum', color='#0C6')
ax1.plot(df_sem_duplicado['Data'], df_sem_duplicado['media_nivel_santa'], label='Nível Santa Tereza', color='#C9F')
ax1.set_xlabel('Data')
ax1.set_ylabel('Nível', color='#0C6')
ax1.tick_params(axis='y', labelcolor='#0C6')

# Cria o segundo eixo y (ax2) compartilhando o eixo x
ax2 = ax1.twinx()
# Plota a Chuva Encantado no eixo y da direita (ax2)
ax2.plot(df_sem_duplicado['Data'], df_sem_duplicado['soma_chuva_dia_encantado'], label='Chuva Encantado', color='#F90')
ax2.plot(df_sem_duplicado['Data'], df_sem_duplicado['soma_chuva_dia_mucum'], label='Chuva Muçum', color='#F00')
ax2.plot(df_sem_duplicado['Data'], df_sem_duplicado['soma_chuva_dia_santa'], label='Chuva Santa Tereza', color='#606')
ax2.set_ylabel('Chuva', color='#606')
ax2.tick_params(axis='y', labelcolor='#606')

# Adiciona título e legenda
plt.title('Nível vs Chuva de Encantado por dia')
fig.tight_layout()

# Adiciona uma grade e ajusta a rotação dos rótulos do eixo x
ax1.grid(True)
plt.xticks(rotation=45)

# Exibe o gráfico
plt.show()

df_com_data_hora

# Entre todos os niveis e chuvas - por data/hora
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plota o Nível Encantado no eixo y da esquerda (ax1)
ax1.plot(df_com_data_hora['Data/Hora'], df_com_data_hora['Nivel'], label='Nível Encantado', color='#0CF')
ax1.plot(df_com_data_hora['Data/Hora'], df_com_data_hora['Nivel_mucum'], label='Nível Muçum', color='#0C6')
ax1.plot(df_com_data_hora['Data/Hora'], df_com_data_hora['Nivel_santa'], label='Nível Santa Tereza', color='#C9F')
ax1.set_xlabel('Data/Hora')
ax1.set_ylabel('Nível', color='#0C6')
ax1.tick_params(axis='y', labelcolor='#0C6')

# Cria o segundo eixo y (ax2) compartilhando o eixo x
ax2 = ax1.twinx()
# Plota a Chuva Encantado no eixo y da direita (ax2)
ax2.plot(df_com_data_hora['Data/Hora'], df_com_data_hora['Chuva'], label='Chuva Encantado', color='#F90')
ax2.plot(df_com_data_hora['Data/Hora'], df_com_data_hora['Chuva_mucum'], label='Chuva Muçum', color='#F00')
ax2.plot(df_com_data_hora['Data/Hora'], df_com_data_hora['Chuva_santa'], label='Chuva Santa Tereza', color='#606')
ax2.set_ylabel('Chuva', color='#606')
ax2.tick_params(axis='y', labelcolor='#606')

# Adiciona título e legenda
plt.title('Nível vs Chuva de todas as cidades - por data/hora')
fig.tight_layout()

# Adiciona uma grade e ajusta a rotação dos rótulos do eixo x
ax1.grid(True)
plt.xticks(rotation=45)

# Exibe o gráfico
plt.show()

import matplotlib.pyplot as plt

# Cria a figura e o primeiro eixo
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plota o Nível Encantado no eixo y da esquerda (ax1)
ax1.plot(df_sem_duplicado['Data'], df_sem_duplicado['media_nivel_encantado'], label='Nível Encantado', color='blue')
ax1.set_xlabel('Data')
ax1.set_ylabel('Nível', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Cria o segundo eixo y (ax2) compartilhando o eixo x
ax2 = ax1.twinx()
# Plota a Chuva Muçum no eixo y da direita (ax2)
ax2.plot(df_sem_duplicado['Data'], df_sem_duplicado['soma_chuva_mucum'], label='Chuva Muçum', color='orange')
ax2.set_ylabel('Soma Chuva Muçum', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Adiciona título e legenda
plt.title('Nível Encantado vs Chuva Muçum - por dia')
fig.tight_layout()

# Adiciona uma grade e ajusta a rotação dos rótulos do eixo x
ax1.grid(True)
plt.xticks(rotation=45)

# Exibe o gráfico
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Filtrando os dados para o mês de junho de 2024
start_date = '2024-06-01'
end_date = '2024-06-30'

df_filtrado = df_sem_duplicado[(df_sem_duplicado['Data'] >= start_date) & (df_sem_duplicado['Data'] <= end_date)]

# Cria a figura e o primeiro eixo
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plota o Nível Encantado no eixo y da esquerda (ax1)
ax1.plot(df_filtrado['Data'], df_filtrado['media_nivel_encantado'], label='Nível Encantado', color='blue')
ax1.set_xlabel('Data')
ax1.set_ylabel('Nível', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Cria o segundo eixo y (ax2) compartilhando o eixo x
ax2 = ax1.twinx()
# Plota a Chuva Muçum no eixo y da direita (ax2)
ax2.plot(df_filtrado['Data'], df_filtrado['soma_chuva_mucum'], label='Chuva Muçum', color='orange')
ax2.set_ylabel('Chuva Muçum', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Adiciona título e legenda
plt.title('Nível Encantado vs Chuva Muçum (Junho de 2024)')
fig.tight_layout()

# Adiciona uma grade e ajusta a rotação dos rótulos do eixo x
ax1.grid(True)
plt.xticks(rotation=45)

# Exibe o gráfico
plt.show()

"""# Prophet"""

##########################################################################################################################
media_encantado = df_sem_duplicado[['Data', 'media_nivel_dia_encantado']].copy() #data como variavel

df_sem_duplicado.set_index('Data', inplace=True) #data como index

df_sem_duplicado = df_sem_duplicado.drop('media_nivel_dia_encantado', axis=1)

from datetime import timedelta
import pandas as pd

df_sem_duplicado.index = pd.to_datetime(df_sem_duplicado.index)

last_index = pd.to_datetime(df_sem_duplicado.index[0])
new_index = last_index + timedelta(days=1)

new_row = {col: float('nan') for col in df_sem_duplicado.columns}
df_sem_duplicado.loc[new_index] = new_row
#agora sem_duplicado tem uma linha inteira vazia mas com data no index


media_encantado['Data'] = pd.to_datetime(media_encantado['Data'], format='%d/%m/%Y')
media_encantado.set_index('Data', inplace=True)



new_row = {col: float('nan') for col in media_encantado.columns}
media_encantado.loc[new_index] = new_row

media_encantado = media_encantado.sort_index()
df_sem_duplicado = df_sem_duplicado.sort_index()
#colocando em ordem

df_sem_duplicado.iloc[:, :] = df_sem_duplicado.iloc[:, :].shift(1)

df_merged = pd.merge(df_sem_duplicado, media_encantado, left_index=True, right_index=True, how='outer')
df_merged

# Tira data do index e coloca de volta como variavel
df_merged = df_merged.reset_index()
df_merged['Data'] = pd.to_datetime(df_merged['Data']).dt.strftime('%Y-%m-%d')
df_merged

# ## CONFERENCIAS


# df_compara = df_compara.sort_values(by='Data')
# df_sem_duplicado = df_sem_duplicado.sort_values(by='Data')

# print(df_sem_duplicado[['Data','media_nivel_dia_encantado','media_nivel_dia_mucum']].head(2),print(df_compara[['Data','media_nivel_dia_encantado','media_nivel_dia_mucum']].head(2)))
# # Salvar o DataFrame
# #from google.colab import drive

# # Montar o Google Drive no Colab
# #drive.mount('/content/drive')
# df_compara.to_excel('/content/drive/My Drive/dados_completos_df_compara.xlsx', index=False)

#tira a linha que tem missing das independentes (primeira linha)
df_merged = df_merged.drop(0)
df_merged #do dia 29 ao 29

df_compara = df_compara.sort_values(by='Data') #do dia 28 ao 28
#nao sofreu nenhuma alteracao alem de colocar em ordem

original = original.sort_values(by='Data')

#tira o ultimo dia pra comparar depois

#df_compara = df_compara.drop(df_compara.index[-1])
#df_merged = df_merged.drop(df_merged.index[-1])

na_counts = original.isna().sum()
print(na_counts)

#Prophet

#Para teste, da pra colocar todas as outras vars como independentes também
banco_analise = pd.DataFrame({
    'mucum': df_compara['media_nivel_dia_mucum'],
    'tereza': df_compara['media_nivel_dia_santa'],
    'y': df_compara['media_nivel_dia_encantado'],
    'ds':df_compara['Data'],
})

# Alinhar as datas entre os dois DataFrames (por exemplo, usando merge ou join)
future = future.merge(original[['Data', 'media_nivel_dia_mucum']], left_on='ds', right_on='Data', how='left')
future['mucum'] = future['media_nivel_dia_mucum']

# Remover a coluna 'Data' e a coluna 'media_nivel_dia_mucum' se não precisar delas
future = future.drop(columns=['Data', 'media_nivel_dia_mucum'])
future

model = Prophet()

model = Prophet(interval_width=0.95)

model.add_regressor('mucum')
model.add_regressor('tereza')

model.fit(banco_analise)

future = model.make_future_dataframe(periods=1)

future = future.merge(original[['Data', 'media_nivel_dia_mucum']], left_on='ds', right_on='Data', how='left')
future['mucum'] = future['media_nivel_dia_mucum']
future = future.drop(columns=['Data', 'media_nivel_dia_mucum'])


future = future.merge(original[['Data', 'media_nivel_dia_santa']], left_on='ds', right_on='Data', how='left')
future['tereza'] = future['media_nivel_dia_santa']
future = future.drop(columns=['Data', 'media_nivel_dia_santa'])


forecast = model.predict(future)


#forecast_basico = model.predict(future) #df_compara
#forecast_data_deslocada = model.predict(future) #df_merged

print('Prevendo o dia 28')
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
print('\n')

print('REAL')
print(original[['Data','media_nivel_dia_encantado']].tail(1))

model = Prophet()

model = Prophet(interval_width=0.95)

model.add_regressor('mucum')

model.fit(banco_analise)

future = model.make_future_dataframe(periods=1)

future = future.merge(original[['Data', 'media_nivel_dia_mucum']], left_on='ds', right_on='Data', how='left')
future['mucum'] = future['media_nivel_dia_mucum']
future = future.drop(columns=['Data', 'media_nivel_dia_mucum'])



forecast = model.predict(future)

print('Prevendo o dia 28')
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
print('\n')

print('REAL')
print(original[['Data','media_nivel_dia_encantado']].tail(1))

#!pip install streamlit

import streamlit as st

# Título da aplicação
st.title("Análise de Séries Temporais com Prophet e Dados Hidrológicos")

# Upload de arquivos pelo usuário
uploaded_files = st.file_uploader("Faça o upload de arquivos Excel com os dados:", type=['xlsx'], accept_multiple_files=True)

dataframes = {}
if uploaded_files:
    for uploaded_file in uploaded_files:
        df = pd.read_excel(uploaded_file, parse_dates=['Data/Hora'], dayfirst=True)
        dataframes[uploaded_file.name] = df
        st.write(f"Visualização dos dados do arquivo `{uploaded_file.name}`:")
        st.write(df.head())

    # Selecionar um dataset para análise
    dataset_name = st.selectbox("Selecione um dataset para análise:", list(dataframes.keys()))

    if dataset_name:
        df = dataframes[dataset_name]

        # Limpeza e preparação dos dados
        st.subheader("Preenchendo valores ausentes")
        df['Nivel'] = df['Nivel'].interpolate()
        df['Vazao'] = df['Vazao'].interpolate()
        st.write("Dados após interpolação de valores:")
        st.write(df.describe())

        # Gráficos exploratórios
        st.subheader("Gráficos")
        st.write("Gráfico de Nível do Rio ao longo do tempo:")
        plt.figure(figsize=(10, 5))
        plt.plot(df['Data/Hora'], df['Nivel'], label='Nível', color='blue')
        plt.xlabel('Data/Hora')
        plt.ylabel('Nível (cm)')
        plt.title('Nível do Rio')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # Previsão com Prophet
        st.subheader("Previsão com Prophet")
        df_prophet = df[['Data/Hora', 'Nivel']].rename(columns={'Data/Hora': 'ds', 'Nivel': 'y'})

        # Treinamento do modelo
        model = Prophet()
        model.fit(df_prophet)

        # Período de previsão
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        # Resultados
        st.write("Previsão para os próximos 30 dias:")
        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

        # Gráficos de previsão
        st.write("Gráfico de Previsão:")
        fig1 = model.plot(forecast)
        st.pyplot(fig1)

        st.write("Componentes da Previsão:")
        fig2 = model.plot_components(forecast)
        st.pyplot(fig2)

#streamlit run app.py & npx localtunnel --port 8501
