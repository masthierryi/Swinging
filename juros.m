% =============================================================================
%                       SIMULADOR DE JUROS COMPOSTOS (v2.2 - Sem Fill)
%
%           Script para calcular e visualizar a evolução de investimentos
%         com aportes mensais, comparando juros compostos e simples.
% =============================================================================

% --- Limpa o ambiente ---
clear; clc; close all;

% =============================================================================
% DADOS DE ENTRADA (ALTERE OS VALORES AQUI)
% =============================================================================
SALARIO_MENSAL = 1080;
APORTE_MENSAL = 600;
TAXA_MENSAL_PERCENTUAL = 10.0;
ANOS_APORTANDO = 2;
ANOS_TOTAIS_GRAFICO = 3;

% =============================================================================
% VALIDAÇÃO DOS DADOS DE ENTRADA (NOVA SEÇÃO)
% =============================================================================
if ANOS_APORTANDO > ANOS_TOTAIS_GRAFICO
    fprintf('AVISO: O tempo de aporte (%d anos) é maior que o tempo total do gráfico (%d anos).\n', ANOS_APORTANDO, ANOS_TOTAIS_GRAFICO);
    ANOS_APORTANDO = ANOS_TOTAIS_GRAFICO;
    fprintf('Ajustando o tempo de aporte para %d anos para a simulação.\n\n', ANOS_APORTANDO);
end

% =============================================================================
% EXECUÇÃO DO PROGRAMA
% =============================================================================

% --- Calculando os dois cenários ---
[meses, patrimonio_com, investido_com, juros_com, salario_com, juros_mensais_com] = ...
    calcular_evolucao(APORTE_MENSAL, SALARIO_MENSAL, TAXA_MENSAL_PERCENTUAL, ANOS_APORTANDO, ANOS_TOTAIS_GRAFICO, true);

[~, patrimonio_sem, ~, ~, ~, juros_mensais_sem] = ...
    calcular_evolucao(APORTE_MENSAL, SALARIO_MENSAL, TAXA_MENSAL_PERCENTUAL, ANOS_APORTANDO, ANOS_TOTAIS_GRAFICO, false);

% --- Exibindo os resultados finais no console ---
fprintf('============================================================\n');
fprintf('RESULTADOS FINAIS APÓS %d ANOS DE APORTE E %d ANOS NO TOTAL\n', ANOS_APORTANDO, ANOS_TOTAIS_GRAFICO);
fprintf('============================================================\n\n');
fprintf('Salário Bruto Acumulado no Período: R$ %.2f\n', salario_com(end));
fprintf('Total Aportado (Investido):         R$ %.2f\n\n', investido_com(end));

fprintf('--- CENÁRIO 1: COM REINVESTIMENTO (JUROS COMPOSTOS) ---\n');
fprintf('Juros Acumulados: R$ %.2f\n', juros_com(end));
fprintf('Patrimônio Final: R$ %.2f\n\n', patrimonio_com(end));

fprintf('--- CENÁRIO 2: SEM REINVESTIMENTO (JUROS SIMPLES) ---\n');
juros_sem_final = patrimonio_sem(end) - investido_com(end);
fprintf('Juros Acumulados: R$ %.2f\n', juros_sem_final);
fprintf('Patrimônio Final: R$ %.2f\n\n', patrimonio_sem(end));
fprintf('Gerando gráfico...\n');

% --- Gerando o gráfico comparativo ---
gerar_grafico(meses, patrimonio_com, patrimonio_sem, investido_com, salario_com, ...
              juros_mensais_com, juros_mensais_sem, ...
              ANOS_APORTANDO, ANOS_TOTAIS_GRAFICO);


% =============================================================================
% DEFINIÇÃO DAS FUNÇÕES
% =============================================================================

function [lista_meses, lista_patrimonio, lista_total_investido, lista_juros_acumulados, lista_salario_acumulado, lista_juros_mensais] = ...
    calcular_evolucao(aporte_mensal, salario_mensal, taxa_mensal_percentual, anos_aportando, anos_totais_simulacao, reinvestir_juros)
    
    taxa_mensal = taxa_mensal_percentual / 100.0;
    total_meses_aporte = anos_aportando * 12;
    total_meses_simulacao = anos_totais_simulacao * 12;
    
    lista_meses = 0:total_meses_simulacao;
    lista_patrimonio = zeros(1, total_meses_simulacao + 1);
    lista_total_investido = zeros(1, total_meses_simulacao + 1);
    lista_juros_acumulados = zeros(1, total_meses_simulacao + 1);
    lista_salario_acumulado = zeros(1, total_meses_simulacao + 1);
    lista_juros_mensais = zeros(1, total_meses_simulacao + 1);

    for mes = 1:total_meses_simulacao
        
        aporte_do_mes = 0.0;
        salario_do_mes = 0.0;
        idx = mes + 1;
        idx_prev = mes;

        if mes <= total_meses_aporte
            aporte_do_mes = aporte_mensal;
            salario_do_mes = salario_mensal;
        end
        
        total_investido_atual = lista_total_investido(idx_prev) + aporte_do_mes;
        
        if reinvestir_juros
            patrimonio_base_para_juros = lista_patrimonio(idx_prev) + aporte_do_mes;
        else
            patrimonio_base_para_juros = total_investido_atual;
        end
        
        juros_do_mes = patrimonio_base_para_juros * taxa_mensal;
        
        lista_total_investido(idx) = total_investido_atual;
        lista_juros_acumulados(idx) = lista_juros_acumulados(idx_prev) + juros_do_mes;
        lista_salario_acumulado(idx) = lista_salario_acumulado(idx_prev) + salario_do_mes;
        lista_juros_mensais(idx) = juros_do_mes;
        lista_patrimonio(idx) = lista_patrimonio(idx_prev) + aporte_do_mes + juros_do_mes;

    end
end

function gerar_grafico(meses, cenario_com_juros, cenario_sem_juros, total_investido, salario_acumulado, juros_mensais_com, juros_mensais_sem, anos_aportando, anos_totais_simulacao)
    
    figure;
    hold on;

    % --- Todas as curvas são plotadas no mesmo eixo Y ---
    h1 = plot(meses, cenario_com_juros, 'r-', 'LineWidth', 2.5);
    h2 = plot(meses, cenario_sem_juros, 'r--', 'LineWidth', 2);
    h3 = plot(meses, total_investido, 'k:', 'LineWidth', 1.5);
    h4 = plot(meses, salario_acumulado, 'k.-', 'LineWidth', 1.5);
    h5 = plot(meses, juros_mensais_com, 'b-.', 'LineWidth', 1.5);
    h6 = plot(meses, juros_mensais_sem, 'b--', 'LineWidth', 1); % Laranja
    
    ylabel('Valor (R$)');
    
    % As duas linhas de 'fill' foram removidas daqui.
    
    title_str = sprintf('Crescimento com %d Ano(s) de Aporte e %d Ano(s) no Total', anos_aportando, anos_totais_simulacao);
    title(title_str);
    xlabel('Meses de Investimento');
    grid on; box on;
    
    % --- Controle dos Eixos e Ticks ---
    xlim([0, max(meses)]);
    ylim([0, max(cenario_com_juros)*1.05]); % O limite Y é definido pela curva maior
    set(gca, 'XTick', 0:6:max(meses));
    
    % --- Legenda e Linha Vertical ---
    mes_final_aporte = anos_aportando * 12;
    if mes_final_aporte > 0 && mes_final_aporte < max(meses)
        h7 = line([mes_final_aporte, mes_final_aporte], get(gca, 'YLim'), 'color', [0.3, 0.3, 0.3], 'LineStyle', '-', 'LineWidth', 0.5);
        legend_handles = [h1, h2, h3, h4, h7, h5, h6];
        legend_labels = {'Patrimônio COM Reinvestimento', 'Patrimônio SEM Reinvestimento', 'Total Aportado', 'Salário Acumulado', sprintf('Fim dos Aportes (%d anos)', anos_aportando), 'Juros Mensais (Com)', 'Juros Mensais (Sem)'};
    else
        legend_handles = [h1, h2, h3, h4, h5, h6];
        legend_labels = {'Patrimônio COM Reinvestimento', 'Patrimônio SEM Reinvestimento', 'Total Aportado', 'Salário Acumulado', 'Juros Mensais (Com)', 'Juros Mensais (Sem)'};
    end
    
    legend(legend_handles, legend_labels, 'Location', 'northwest');
    hold off;
end