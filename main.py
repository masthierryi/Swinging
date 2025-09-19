import math

# =============================================================================
# FUNÇÃO PARA CÁLCULO DE DIMENSIONAMENTO DE POSIÇÃO (ATUALIZADA)
# =============================================================================

def calcular_tamanho_posicao(capital_total, risco_por_trade_percentual, preco_entrada, preco_stop, nome_ativo, modalidade='Ações', margem_por_contrato=100, valor_por_ponto=1.0):
    """
    Calcula o tamanho da posição com base no gerenciamento de risco,
    detectando o tipo de operação e a modalidade (Ações ou Daytrade).

    Args:
        capital_total (float): O valor total do seu capital operacional.
        risco_por_trade_percentual (float): O risco aceitável em % (ex: 1 para 1%).
        preco_entrada (float): O preço/pontuação de entrada na operação.
        preco_stop (float): O preço/pontuação do stop-loss.
        nome_ativo (str): O nome do ativo para fins de exibição.
        modalidade (str): 'Ações' para operar com custo total ou 'Daytrade' para operar com margem.
        margem_por_contrato (float): A margem de garantia exigida pela corretora por contrato.
        valor_por_ponto (float): O valor financeiro de cada ponto do ativo (ex: 0.20 para WIN).
    """
    # --- PASSO 0: Detecção Automática do Tipo de Operação ---
    if preco_entrada > preco_stop:
        tipo_operacao = 'Compra'
    elif preco_stop > preco_entrada:
        tipo_operacao = 'Venda'
    else:
        print(f"--- ERRO para: {nome_ativo} ---")
        print("Preço de entrada e stop não podem ser iguais.")
        print("=" * 50 + "\n")
        return
        
    unidade = "Contratos" if modalidade == 'Daytrade' else "Ações"

    print(f"--- Análise de Risco para: {nome_ativo} ({tipo_operacao.upper()}) ---")
    print("-" * 50)

    # --- PASSO 1: Calcular o Risco Financeiro Máximo em Reais ---
    risco_financeiro_maximo = capital_total * (risco_por_trade_percentual / 100.0)

    # --- PASSO 2: Calcular o Risco Monetário por Unidade (Ação/Contrato) ---
    risco_por_unidade_pontos = abs(preco_entrada - preco_stop)
    risco_por_unidade_monetario = risco_por_unidade_pontos * valor_por_ponto
    
    if risco_por_unidade_monetario <= 0:
        print(f"ERRO: Risco por {unidade} inválido!")
        return

    # --- PASSO 3: Calcular a Quantidade Ideal de Ações/Contratos ---
    quantidade_ideal = risco_financeiro_maximo / risco_por_unidade_monetario
    quantidade_a_operar = math.floor(quantidade_ideal)
    
    if quantidade_a_operar == 0:
        print(f"AVISO: O risco por {unidade} é muito alto para o seu capital. A quantidade a operar é zero.")
        return

    # --- PASSO 4: Verificar a Viabilidade Financeira (Custo vs Margem) ---
    print(f"Capital Operacional Total: R$ {capital_total:,.2f}")
    print(f"Risco Máximo por Trade: {risco_por_trade_percentual}% = R$ {risco_financeiro_maximo:,.2f}\n")
    
    print(f"Preço de Entrada: {preco_entrada:,.2f}")
    print(f"Preço de Stop-Loss: {preco_stop:,.2f}")
    print(f"Risco por {unidade}: {risco_por_unidade_pontos:,.2f} pontos = R$ {risco_por_unidade_monetario:.2f}\n")
    
    print(">>> RESULTADO DO CÁLCULO <<<")
    print(f"Quantidade de {unidade} a Operar: {quantidade_a_operar}\n")

    if modalidade == 'Ações':
        custo_total_operacao = quantidade_a_operar * preco_entrada
        operacao_viavel = custo_total_operacao <= capital_total
        print(f"Custo Financeiro da Operação: {quantidade_a_operar} ações * R$ {preco_entrada:.2f} = R$ {custo_total_operacao:,.2f}")
        if operacao_viavel:
            print("Operação VIÁVEL (Custo da operação é menor que o capital total).\n")
        else:
            print("Operação INVIÁVEL (Custo da operação é maior que o capital total).\n")
    
    elif modalidade == 'Daytrade':
        margem_total_exigida = quantidade_a_operar * margem_por_contrato
        operacao_viavel = margem_total_exigida <= capital_total
        print(f"Margem de Garantia Exigida: {quantidade_a_operar} contratos * R$ {margem_por_contrato:.2f} = R$ {margem_total_exigida:,.2f}")
        if operacao_viavel:
            print("Operação VIÁVEL (Margem exigida é menor que o capital total).\n")
        else:
            print("Operação INVIÁVEL (Margem exigida é maior que o capital total).\n")

    perda_real_com_stop = quantidade_a_operar * risco_por_unidade_monetario
    print(f"CONFIRMAÇÃO: Se o stop for atingido, a perda será de R$ {perda_real_com_stop:,.2f} (dentro do seu limite de R$ {risco_financeiro_maximo:,.2f}).")
    print("=" * 50 + "\n")


# =============================================================================
# DADOS DE ENTRADA (ALTERE OS VALORES AQUI)
# =============================================================================

# --- Configurações Gerais ---
CAPITAL_OPERACIONAL_TOTAL = 36000
RISCO_POR_TRADE_PERCENTUAL = 1.0  # 1% de risco sobre o capital total

# --- Cenário 1: Trade com Ações (VALE3) ---
ATIVO_A = "VALE3"
PRECO_ENTRADA_A = 16.58
PRECO_STOP_A = 16.38

# --- Cenário 2: Trade com Ações (PETR4) ---
ATIVO_B = "PETR4"
PRECO_ENTRADA_B = 10.15
PRECO_STOP_B = 10.42

# --- Cenário 3: Daytrade com Contrato Futuro (Mini-Índice) ---
ATIVO_C = "WINZ25"
PRECO_ENTRADA_C = 120000
PRECO_STOP_C = 119850 # Stop de 150 pontos


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

# Calcula o dimensionamento para o Trade A (Ações)
# Modalidade 'Ações' é o padrão, não precisa ser especificada
calcular_tamanho_posicao(
    capital_total=CAPITAL_OPERACIONAL_TOTAL,
    risco_por_trade_percentual=RISCO_POR_TRADE_PERCENTUAL,
    preco_entrada=PRECO_ENTRADA_A,
    preco_stop=PRECO_STOP_A,
    nome_ativo=ATIVO_A
)

# Calcula o dimensionamento para o Trade B (Ações)
calcular_tamanho_posicao(
    capital_total=CAPITAL_OPERACIONAL_TOTAL,
    risco_por_trade_percentual=RISCO_POR_TRADE_PERCENTUAL,
    preco_entrada=PRECO_ENTRADA_B,
    preco_stop=PRECO_STOP_B,
    nome_ativo=ATIVO_B
)

# Calcula o dimensionamento para o Trade C (Daytrade com Mini-Índice)
calcular_tamanho_posicao(
    capital_total=CAPITAL_OPERACIONAL_TOTAL,
    risco_por_trade_percentual=RISCO_POR_TRADE_PERCENTUAL,
    preco_entrada=PRECO_ENTRADA_C,
    preco_stop=PRECO_STOP_C,
    nome_ativo=ATIVO_C,
    modalidade='Daytrade',      # Especifica que é uma operação com margem
    margem_por_contrato=100.0,  # Informa a margem por contrato
    valor_por_ponto=0.20        # Informa o valor de cada ponto para o WIN
)