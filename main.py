import math

# =============================================================================
# FUNÇÃO PARA CÁLCULO DE DIMENSIONAMENTO DE POSIÇÃO
# =============================================================================

def calcular_tamanho_posicao(capital_total, risco_por_trade_percentual, preco_entrada, preco_stop, tipo_operacao, nome_ativo):
    """
    Calcula o tamanho da posição (quantidade de ações/contratos) com base
    no gerenciamento de risco definido.

    Args:
        capital_total (float): O valor total do seu capital operacional.
        risco_por_trade_percentual (float): O risco aceitável em porcentagem (ex: 1 para 1%).
        preco_entrada (float): O preço de entrada na operação.
        preco_stop (float): O preço do stop-loss.
        tipo_operacao (str): 'compra' ou 'venda'.
        nome_ativo (str): O nome do ativo para fins de exibição.
    """
    print(f"--- Análise de Risco para: {nome_ativo} ({tipo_operacao.upper()}) ---")
    print("-" * 50)

    # --- PASSO 1: Calcular o Risco Financeiro Máximo em Reais ---
    risco_financeiro_maximo = capital_total * (risco_por_trade_percentual / 100.0)

    # --- PASSO 2: Calcular o Risco por Ação ---
    if tipo_operacao.lower() == 'compra':
        risco_por_acao = preco_entrada - preco_stop
    elif tipo_operacao.lower() == 'venda':
        risco_por_acao = preco_stop - preco_entrada
    else:
        print("ERRO: Tipo de operação inválido. Use 'compra' ou 'venda'.")
        return

    # Validação para garantir que o stop está posicionado corretamente
    if risco_por_acao <= 0:
        print(f"ERRO: Stop-loss inválido! Para uma {tipo_operacao}, o stop deve ser, respectivamente, menor/maior que a entrada.")
        return

    # --- PASSO 3: Calcular a Quantidade Ideal de Ações ---
    # Evita divisão por zero, embora a validação anterior já ajude
    if risco_por_acao == 0:
        print("ERRO: Risco por ação é zero. Preço de entrada e stop não podem ser iguais.")
        return
        
    quantidade_ideal = risco_financeiro_maximo / risco_por_acao
    # Arredondamos para baixo para garantir que nunca arriscaremos mais que o planejado
    quantidade_a_operar = math.floor(quantidade_ideal)
    
    if quantidade_a_operar == 0:
        print("AVISO: O risco por ação é muito alto para o seu capital. A quantidade de ações a operar é zero.")
        return

    # --- PASSO 4: Verificar a Viabilidade Financeira ---
    custo_total_operacao = quantidade_a_operar * preco_entrada
    operacao_viavel = custo_total_operacao <= capital_total
    
    # --- RESULTADOS ---
    print(f"Capital Operacional Total: R$ {capital_total:,.2f}")
    print(f"Risco Máximo por Trade: {risco_por_trade_percentual}% = R$ {risco_financeiro_maximo:,.2f}\n")
    
    print(f"Preço de Entrada: R$ {preco_entrada:.2f}")
    print(f"Preço de Stop-Loss: R$ {preco_stop:.2f}")
    print(f"Risco por Ação: R$ {risco_por_acao:.2f}\n")
    
    print(">>> RESULTADO DO CÁLCULO <<<")
    print(f"Quantidade de Ações a Operar: {quantidade_a_operar}\n")

    print(f"Custo Financeiro da Operação: {quantidade_a_operar} ações * R$ {preco_entrada:.2f} = R$ {custo_total_operacao:,.2f}")
    
    if operacao_viavel:
        print("Operação VIÁVEL (Custo da operação é menor que o capital total).\n")
    else:
        print("Operação INVIÁVEL (Custo da operação é maior que o capital total).\n")

    perda_real_com_stop = quantidade_a_operar * risco_por_acao
    print(f"CONFIRMAÇÃO: Se o stop for atingido, a perda será de R$ {perda_real_com_stop:,.2f} (dentro do seu limite de R$ {risco_financeiro_maximo:,.2f}).")
    print("=" * 50 + "\n")


# =============================================================================
# DADOS DE ENTRADA (ALTERE OS VALORES AQUI)
# =============================================================================

# --- Configurações Gerais ---
CAPITAL_OPERACIONAL_TOTAL = 36000.00
RISCO_POR_TRADE_PERCENTUAL = 1.0  # 1% de risco sobre o capital total

# --- Cenário 1: Trade A (Compra), conforme a imagem ---
ATIVO_A = "VALE3"
TIPO_OPERACAO_A = "compra"
PRECO_ENTRADA_A = 16.58
PRECO_STOP_A = 16.38

# --- Cenário 2: Trade B (Venda), conforme a imagem ---
ATIVO_B = "PETR4"
TIPO_OPERACAO_B = "venda"
PRECO_ENTRADA_B = 10.15
PRECO_STOP_B = 10.42


# =============================================================================
# EXECUÇÃO DO PROGRAMA
# =============================================================================

# Calcula o dimensionamento para o Trade A
calcular_tamanho_posicao(
    capital_total=CAPITAL_OPERACIONAL_TOTAL,
    risco_por_trade_percentual=RISCO_POR_TRADE_PERCENTUAL,
    preco_entrada=PRECO_ENTRADA_A,
    preco_stop=PRECO_STOP_A,
    tipo_operacao=TIPO_OPERACAO_A,
    nome_ativo=ATIVO_A
)

# Calcula o dimensionamento para o Trade B
calcular_tamanho_posicao(
    capital_total=CAPITAL_OPERACIONAL_TOTAL,
    risco_por_trade_percentual=RISCO_POR_TRADE_PERCENTUAL,
    preco_entrada=PRECO_ENTRADA_B,
    preco_stop=PRECO_STOP_B,
    tipo_operacao=TIPO_OPERACAO_B,
    nome_ativo=ATIVO_B
)
