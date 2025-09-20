import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# =============================================================================
# FUNÇÃO PARA CALCULAR A EVOLUÇÃO DO INVESTIMENTO (ATUALIZADA)
# =============================================================================

def calcular_evolucao(aporte_mensal, salario_mensal, taxa_mensal_percentual, anos_aportando, anos_totais_simulacao, reinvestir_juros=True):
    """
    Calcula a evolução de um investimento, separando o período de aportes
    do período de apenas rendimento e incluindo o salário acumulado.

    Args:
        aporte_mensal (float): Valor do aporte feito a cada mês.
        salario_mensal (float): Valor do salário bruto mensal no período de aporte.
        taxa_mensal_percentual (float): Taxa de juros mensal em porcentagem (ex: 10 para 10%).
        anos_aportando (int): Número de anos fazendo aportes.
        anos_totais_simulacao (int): Total de anos para a simulação (gráfico).
        reinvestir_juros (bool): True para juros compostos, False para juros simples.

    Returns:
        tuple: Contendo as listas de meses, patrimônio total, total investido, juros acumulados e salário acumulado.
    """
    # --- Configurações Iniciais ---
    taxa_mensal = taxa_mensal_percentual / 100.0
    total_meses_aporte = anos_aportando * 12
    total_meses_simulacao = anos_totais_simulacao * 12
    
    # --- Listas para armazenar o histórico ---
    lista_meses = [0]
    lista_patrimonio = [0.0]
    lista_total_investido = [0.0]
    lista_juros_acumulados = [0.0]
    lista_salario_acumulado = [0.0]

    # --- Variáveis de controle ---
    patrimonio_atual = 0.0
    total_investido = 0.0
    salario_acumulado = 0.0
    
    # --- Loop de Simulação Mês a Mês ---
    for mes in range(1, total_meses_simulacao + 1):
        
        aporte_do_mes = 0.0
        salario_do_mes = 0.0
        
        # 1. Verifica se ainda está no período de aportes
        if mes <= total_meses_aporte:
            aporte_do_mes = aporte_mensal
            salario_do_mes = salario_mensal
        
        # Adiciona os valores do mês aos acumuladores
        patrimonio_atual += aporte_do_mes
        total_investido += aporte_do_mes
        salario_acumulado += salario_do_mes
        
        # 2. Calcula os juros do mês
        if reinvestir_juros:
            juros_do_mes = patrimonio_atual * taxa_mensal
            patrimonio_atual += juros_do_mes
        else:
            juros_do_mes = total_investido * taxa_mensal
            patrimonio_atual = total_investido + lista_juros_acumulados[-1] + juros_do_mes

        # 3. Armazena os resultados do mês
        lista_meses.append(mes)
        lista_patrimonio.append(patrimonio_atual)
        lista_total_investido.append(total_investido)
        lista_juros_acumulados.append(lista_juros_acumulados[-1] + juros_do_mes)
        lista_salario_acumulado.append(salario_acumulado)
        
    return lista_meses, lista_patrimonio, lista_total_investido, lista_juros_acumulados, lista_salario_acumulado

# =============================================================================
# FUNÇÃO PARA GERAR O GRÁFICO (ATUALIZADA)
# =============================================================================

def gerar_grafico(meses, cenario_com_juros, cenario_sem_juros, total_investido, salario_acumulado, anos_aportando, anos_totais_simulacao):
    """Gera um gráfico comparativo dos cenários de investimento."""
    
    plt.style.use('seaborn-v0_8-whitegrid')
    # Ajustado para um aspecto mais "quadrado"
    fig, ax = plt.subplots(figsize=(10, 8))

    # --- Plotando as curvas ---
    ax.plot(meses, cenario_com_juros, label='Patrimônio COM Reinvestimento (Juros Compostos)', color='green', linewidth=2.5)
    ax.plot(meses, cenario_sem_juros, label='Patrimônio SEM Reinvestimento (Juros Simples)', color='red', linewidth=2)
    ax.plot(meses, total_investido, label='Total Aportado (Investido)', color='black', linestyle='--', dashes=(5, 5))
    ax.plot(meses, salario_acumulado, label='Salário Acumulado (Bruto)', color='purple', linestyle=':', dashes=(4, 4))

    # --- Adicionando linha vertical para marcar o fim dos aportes ---
    mes_final_aporte = anos_aportando * 12
    if mes_final_aporte > 0 and mes_final_aporte < len(meses)-1:
        ax.axvline(x=mes_final_aporte, color='blue', linestyle='-.', linewidth=1.5, label=f'Fim dos Aportes ({anos_aportando} anos)')

    # --- Formatando o gráfico ---
    ax.set_title(f'Crescimento com {anos_aportando} Anos de Aporte e {anos_totais_simulacao} Anos Totais', fontsize=16)
    ax.set_xlabel('Meses de Investimento', fontsize=12)
    ax.set_ylabel('Valor Acumulado (R$)', fontsize=12)
    ax.legend(fontsize=10)
    
    # --- CONTROLE DOS EIXOS E TICKS ---
    ax.set_xlim(left=0, right=max(meses))
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(6)) # Ticks a cada 6 meses

    # Formata o eixo Y para moeda brasileira
    formatter = mticker.FuncFormatter(lambda x, p: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
    ax.yaxis.set_major_formatter(formatter)
    
    # Adiciona preenchimento para destacar os juros
    ax.fill_between(meses, cenario_com_juros, total_investido, color='green', alpha=0.1)
    ax.fill_between(meses, cenario_sem_juros, total_investido, color='red', alpha=0.1)

    plt.tight_layout()
    plt.show()

# =============================================================================
# DADOS DE ENTRADA (ALTERE OS VALORES AQUI)
# =============================================================================
SALARIO_MENSAL = 1080         # << NOVO: Salário bruto no período de aportes
APORTE_MENSAL = 600
TAXA_MENSAL_PERCENTUAL = 10.0 # 10% ao mês
ANOS_APORTANDO = 2
ANOS_TOTAIS_GRAFICO = 4

# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

# --- Calculando os dois cenários ---
# A curva de salário e aporte só precisa ser calculada uma vez
meses, patrimonio_com, investido_com, juros_com, salario_com = calcular_evolucao(
    APORTE_MENSAL, SALARIO_MENSAL, TAXA_MENSAL_PERCENTUAL, ANOS_APORTANDO, ANOS_TOTAIS_GRAFICO, reinvestir_juros=True
)

_, patrimonio_sem, _, _, _ = calcular_evolucao(
    APORTE_MENSAL, SALARIO_MENSAL, TAXA_MENSAL_PERCENTUAL, ANOS_APORTANDO, ANOS_TOTAIS_GRAFICO, reinvestir_juros=False
)

# --- Exibindo os resultados finais no console ---
print("=" * 60)
print(f"RESULTADOS FINAIS APÓS {ANOS_APORTANDO} ANOS DE APORTE E {ANOS_TOTAIS_GRAFICO} ANOS NO TOTAL")
print("=" * 60)
print(f"\nSalário Bruto Acumulado no Período: R$ {salario_com[-1]:,.2f}")
print(f"Total Aportado (Investido): R$ {investido_com[-1]:,.2f}\n")

print("--- CENÁRIO 1: COM REINVESTIMENTO (JUROS COMPOSTOS) ---")
print(f"Juros Acumulados: R$ {juros_com[-1]:,.2f}")
print(f"Patrimônio Final: R$ {patrimonio_com[-1]:,.2f}")

print("\n--- CENÁRIO 2: SEM REINVESTIMENTO (JUROS SIMPLES) ---")
juros_sem_final = patrimonio_sem[-1] - investido_com[-1]
print(f"Juros Acumulados: R$ {juros_sem_final:,.2f}")
print(f"Patrimônio Final: R$ {patrimonio_sem[-1]:,.2f}")
print("\nGerando gráfico...")

# --- Gerando o gráfico comparativo ---
gerar_grafico(meses, patrimonio_com, patrimonio_sem, investido_com, salario_com, ANOS_APORTANDO, ANOS_TOTAIS_GRAFICO)