import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def most_freq_cat(data_df, cat_name, target, answer, lim=0.9):
    
    yes = data_df[target] == answer
    
    # As categorias mais frequentes na resposta de interesse (clientes ativos)
    cat_yes_count = data_df[yes].groupby(cat_name)['y'].count()
    cat_yes = cat_yes_count/cat_yes_count.sum()
    cat_yes.sort_values(inplace=True, ascending=False)

    # Listar as mais frequentes da amostra
    freq_acum = 0.0
    list_most_freq = []

    for ii in cat_yes.index:
        if (freq_acum <= lim):
            freq_acum += cat_yes[ii]
            list_most_freq.append(ii)
            
    # Agrupar as categorias minoritárias como 'others'
    for ii in cat_yes.index:
        if ii not in list_most_freq:
            data_df[cat_name] = data_df[cat_name].replace(ii, 'others')    
    
    return data_df 


def taxa_adesao(data_df, cat_name, target, answer, ratio_yes):
    
    yes = data_df[target] == answer    
    
    # % de clientes ativos    
    cat_yes_count = data_df[yes].groupby(cat_name)['y'].count()
    cat_yes = 100*(cat_yes_count/cat_yes_count.sum())
    cat_yes.sort_values(inplace=True, ascending=False)
    
    plt.subplot(121)
    cat_yes.plot.bar()
    plt.xlabel(None)
    plt.ylabel('% de clientes ativos')
    
    
    # Taxa de adesão dos clientes    
    cat_all_count = data_df.groupby(cat_name)['y'].count()
    cat_ratio = 100*(cat_yes_count/cat_all_count)
    cat_ratio.sort_values(inplace=True, ascending=False)

    plt.subplot(122)
    cat_ratio.plot.bar()
    plt.axhline(y=ratio_yes, color='r')
    plt.xlabel(None)
    plt.ylabel('Taxa de adesão (%)')
        
    return

def plot_num_cat(data_df, cat_name, target, asnwer, xlabel=None):

    yes = data_df[target] == asnwer
    
    plt.figure(figsize=(10,5))
    sns.distplot(data_df[cat_name])
    sns.distplot(data_df[cat_name][yes])
    plt.xlabel(xlabel)
    plt.ylabel('Distribuição de probabilidade')
    plt.legend(['Pessoas contactas', 'Clientes ativos'])
    
    return