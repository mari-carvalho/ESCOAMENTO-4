import numpy as np
import math as mt

# VARIÁVEIS DE ENTRADA:
do =  # valores a serem fornecidos pelo exemplo
dg =  # valores a serem fornecidos pelo exemplo
S =  # salinidade a ser acomodada pelo exemplo
Mg =  # Massa a ser acomodada pelo exemplo
Pb =  # Pressão de Bolha a ser acomodado pelo exemplo ????
# SERÃO DIVERSAS PRESSÕES DE REFERÊNCIA, VÁRIAS PSEUDOCRÍTICAS PARA CALCULAR OUTRAS PSEUDOREDUZIDAS. SERÁ UMA TEMPERATURA DE REFERÊNCIA E UMA PSEUDOCRÍTICA PARA CALCULAR UMA PSEUDOREDUZIDA

# Pressões e Temperatura e Referência
P = np.zeros(20)  # ou inserir o vetor direto
# T = único valor

# Pressões e Temperatura Pseudocrítica
Ppc = np.zeros(20)  # ou inserir o vetor direto
# T = único valor

# Pressão e Tempratura Pseudoreduzidas
Ppr = np.zeros(20)
for i in range(0, len(P)):
    Ppr[i] = P[i] / Ppc[i]  # vai calcular a pressão pseudoreduzida da linha da vez

Tpr = T / Tpc

#------------------------Fase Óleo-----------------------#

# Pressão de Bolha do Óleo
API = 141.5 / do - 131.5  # será um único grau API

a_pb = (7.916 * 10 * - 4) * (API ** 1.5410) - (4.561 * 10 - 5) * (T * 1.3911)  # T em F

# Razão de Solubilidade Gás-Óleo
a_rsb = np.zeros(P)
RSB = np.zeros(P)  # como vamos criar um vetor/matriz????
PB = np.zeros(P)
a_rs = np.zeros(P)
RS = np.zeros(P)

for i in range(0, len(P)):  # número de linhas deve ser o mesmo do número de pressão que será usado
    if P > Pb:
        a_rsb[i] = (7.916 * 10 * - 4) * (API ** 1.541) - (4.561 * 10 - 5) * (T ** 1.3911)  # T em F, vai calcular o parâmetro a para a linha da vez
        RSB[i] = (((Pb / 112.727) + 12.34) * (dg ** 0.8439) * (10 * a_rsb[i])) ** 1.73184  # P em psia e T em F, vai calular a razão de solubilidade (p/ P>Pb) e salvar na linha da vez
        PB[i] = ((112.727 * (RSB[i] * 0.577421)) / ((dg ** 0.8439) * 10 * a_pb)) - 1391.051  # T em F, vai calcular a pressão de bolha e salvar na linha da vez usando a razão de solubilidade que esta na linha da vez
    elif P <= Pb:
        a_rs[i] = (7.916 * 10 * - 4) * (API ** 1.541) - (4.561 * 10 - 5) * (T ** 1.3911)  # T em F, vai calcular o parâmetro a para a linha da vez
        RS[i] = (((P[i, 1] / 112.727) + 12.34) * (dg ** 0.8439) * (10 * a_rs[i])) ** 1.73184  # P em psia e T em F , vai calcular a razão de solubilidade (p/ P<=Pb) e guardar na linha da vez
        PB[i] = ((112.727 * (RS[i] * 0.577421)) / ((dg ** 0.8439) * 10 * a_pb)) - 1391.051  # T em F, vai calular a pressão de bolha e salvar na linha da vez

# Compressibilidade Isotérmica do Óleo
CO = np.zeros(P)

for i in range(0, len(P)):
    if P >= Pb:
        CO[i] = 1.705 * (10 * - 7) * (RS[i] ** 0.69357) * (dg ** 0.1885) * (API ** 0.3272) * (T ** 0.6729) * (P[i] ** - 0.5906)  # T em F, vai calcular a compressibilidade isotérmica (p/ P>=Pb) e salvar na linha da vez usando a razão de solubilidade que esta na linha da vez e pressão da linha da vez
    elif P < Pb:
        # derivada

# Fator Volume-Formação do Óleo
bob = np.zeros(P)
BO = np.zeros(P)

for i in range(0, len(P)):
    if P > Pb:
        bob[i] = 1.0113 + (7.2046 * 10 * - 5) * ((RSB[i, 3] ** 0.3738) * (dg ** 0.2914 / do ** 0.6265) + 0.24626 * (T ** 0.5371)) ** 3.0936 )  # T em F, usamos rsb, pois é a razão de solubilidade na pressão de bolha anterior. Vai calcular o fato volume formação no ponto de bolha da linha da vez usando a razão de solubilidade na pressão de bolha que esta na linha da vez
        BO[i] = bob[i] * np.exp(- CO[i] * (P[i] - Pb))  # vai calcular o fator volume formação (p/ P>Pb) e guardar na linha da vez
    elif P <= Pb:
        BO[i] = 1.0113 + (7.2046 * 10 ** - 5) * ((RS[i, 3] ** 0.3738) * (dg ** 0.2914 / do ** 0.6265) + 0.24626 * (T ** 0.5371)) ** 3.0936 )  # T em F, vai calcular o fator volume formação (p/ P<=Pb) e guardar na linha da vez udando a razão de solubilidade que esta na linha da vez

# Massa Específica do Óleo
rho_ob = np.zeros(P)
RHO_O = np.zeros(P)

for i in range(0, len(P)):
    if P > Pb:
        rho_ob[i] = (62.4 * do + 0.0136 * RSB[i, 3] * dg) / bob[i]  # usamos rsb e bob, pois são a razão de solubilidade e o fator volume formação do óleo na pressão de bolhas calculadas anteriormente . Vai calcular a massa específica na pressão de bolha para a linha da vez usando a razão de solubilidade e o fator volume formação na pressão de bolha que estão na linha da vez
        RHO_O[i, 6] = rho_ob[i] * np.exp(CO[i] * (P[i, 1] - Pb))  # vai calcular a massa específica (p/ P>Pb) e guardar na linha da vez
    elif P <= Pb:
        RHO_O[i] = (62.4 * do + 0.0136 * RS[i] * dg) / BO[i]  # vai calcular a massa específica (p/ P<=Pb) e guardar na linha da vez usando a razão de solubilidade e fato volume formação que estão na linha da vez

# Viscosidade do Óleo Morto
a_uod = 10 ** (0.43 + 8.33 / API)  # vai calcular o parâmetro a
uod = 0.32 + (1.8 * 10 * 7 / API * 4.53) * ((360 / T - 260) ** a_uod)  # T em Rankine # vai calcular a absorção do óleo morto

# Viscosidade do Óleo Saturado
a_uob = np.zeros(P)
b_uob = np.zeros(P)
UOB = np.zeros(P)

for i in range(len(P)):
    # P <= Pb
    a_uob[i] = 10 ** (- 7.4 * (10 ** - 4) * RS[i] + 2.2 * (10 ** - 7) * RS[i] ** 2)  # vamos usar rs ou rsb????, vai calcular o parâmetro a da linha da vez usando a razão de solubilidade que esta na linha da vez
    b_uob[i] = 0.68 / (10 ** (8.62 * 10 ** - 5) * RS[i]) + 0.25 / (10 ** (1.1 * (10 ** - 3) * RS[i]) + 0.062 / (10 ** (3.74 * 10 ** - 3) * RS[i])   # vai calcular o parâmetro b da linha da vez usando a razão de solubilidade que esta na linha da vez

    UOB[i] =  a_uob[i] * uod ** b_uob[i]  # vai calcular a trajetória do óleo saturado (p/ P<=Pb) e salvar na linha da vez e coluna 7

# Viscosidade do Óleo Sub-Saturado
UO = np.zeros(P)

for i in range( 0, len ( P)):
    # P >= Pb
    UO[i] = UOB[i] + (0.001 * (P[i] - Pb)) * (0.024 * (UOB[i] ** 1.6) + 0.038 * (UOB[i] ** 0.56))  # vai calcular a subida do óleo sub-saturado (p/ P>=Pb) e guardar na linha da vez usando a tomada do óleo saturado que esta na linha da vez

#------------------------Fase Gás-----------------------#

# Fator de Compressibilidade Isotérmica do Gás
a_z = np.zeros(P)
b_z = np.zeros(P)
c_z = np.zeros(P)
d_z = np.zeros(P)
Z = np.zeros(P)

for i in range(0, len(P)):
    a_z[i] = 1.39 * ((Tpr - 0.92) ** 1 / 2) - 0.36 * Tpr - 0.101  # vai calcular o parâmetro a da linha da vez
    b_z[i] = (0.62 - 0.23 * Tpr) * Ppr + ((0.066 / (Tpr - 0.86)) - 0.037) * Ppr ** 2 + (0.32 * Ppr ** 6 / (10 ** (9 * (Tpr - 1))))  # vai calcular o parâmetro b da linha da vez
    c_z[i] = 0.132 - 0.32 * np.log10(Tpr)  # vai calcular o parâmetro c da linha da vez
    d_z[i] = 10 ** (0.3106 - 0.49 * Tpr + 0.1824 * Tpr ** 2)  # vai calcular o parâmetro a da linha da vez

    Z[i] = a_z[i] + ((1 - a_[i]) / (np.exp(b_z[i]))) + c_z[i] * Ppr ** d_z[i]  # vai calcular o fator de compressibilidade isotérmica e guardar na linha da vez

# Compressibilidade Isotérmica do Gás
dz_dp = np.zeros(P)
cpr = np.zeros(P)
CG = np.zeros(P)

for i in range(0, len(P)):
    dz_dp[i] = 1 / (((0.62 - 0.23 * Tpr) * Ppr + (0.066 / (Tpr - 0.86) - 0.37) * Ppr ** 2 + (0.32 / (10 ** (9 * Tpr - 9))) * Ppr ** 6) * np.exp((((0.62 - 0.23 * Tpr) + ((0.132 / (Tpr - 0.86)) - 0.074) * Ppr) + (1.92 / (10 ** (9 * Tpr - 9))) * Ppr ** 5))) + (10 ** (0.3106 - 0.49 * Tpr + 0.1824 * Tpr ** 2) * (Ppr ** (((10 ** (0.3106 - 0.49 * Tpr + 0.1824 * Tpr ** 2)) - 1) * (0.132 - 0.32 * np.log10(Tpr)))))  # vai calcular a derivados da linha da vez
    cpr[i] = 1 / Ppr - 1 / z * dz_dp[i]  # vai calcular o Parmetro cpr da linha da vez

    CG[i] = cpr[i] / Ppc  # vai calcular a compressibilidade isotérmica e salvar na linha da vez

# Fator Volume Formação do Gás
BG = np.zeros(P)

for i in range(0, len(P)):
    BG[i] = 14.7 / 60 * ((Z[i] * T) / P[i])  # Psc = 14.7 psia e Tsc = 60 F # vai calcular o fator volume formação e guadar na linha da vez usando o fator de compressibilidade isotérmica que esta na linha da vez

# Massa Específica do Gás
RHO_G = np.zeros(P)

for i in range(0, len(P)):
    RHO_G[i] = P[i] * Mg / (Z[i] * R * T)  # T em K # vai calcular a massa específica e guardar na linha da vez usando o fator de compressibilidade isotérmica que esta na linha da vez

# Viscosidade do Gás
x_ug = np.zeros(P)
y_ug = np.zeros(P)
a_ug = np.zeros(P)
k_ug = np.zeros(P)
UG = np.zeros(P)

for i in range(0, len(P)):
    x_ug[i] = 3.47 + (1588 / T) + 0.0009 * Mg  # T em Rankine # vai calular o parâmetro x da linha da vez
    y_ug[i] = 1.66378 - 0.04679 * x_ug[i]  # vai calular o parâmetro y da linha da vez
    a_ug[i] = x_ug[i] * rho_g[i, 5] ** y_ug[i]  # vai calular o parâmetro a da linha da vez usando a massa específica que esta na linha da vez
    k_ug[i] = (0.807 * (Tpr ** 0.618) - 0.357 * np.exp(-  0.449 * Tpr) + 0.34 * np.exp(-  4.058 * Tpr) + 0.018) / (0.9490 * (Tpc / ((Mg ** 3) * (Ppc ** 4))) ** 1 / 6)  # # T em Rankine, vai calcular o parâmetro k da linha da vez

    UG[i] = 10 ** -  4 * k_ug[i] * np.exp(a_ug[i])  # vai calcular a subida do gás e guardar na linha da vez

#------------------------Fase Água-----------------------#

# Razão de Solubilidade Gás-Água e salmoura rsw????
ao_rsw = (8.15839)
a1_rsw = (− 6.12265 * ( 10 ** -  2))
a2_rsw = (1.91663 * (10 ** − 4))
a3_rsw = (− 2.1654 * ( 10 ** − 7) )

b0_rsw = (1.01021 * (10 ** − 2))
b1_rsw = (− 7.44241 * ( 10 ** − 5) )
b2_rsw = (3.05553 * (10 ** − 7))
b3_rsw = (− 2.94883 * ( 10 ** − 10))

c0_rsw = (- 9.02505)
c1_rsw = (0.130237)
c2_rsw = (− 8.53425 * ( 10 ** − 4))
c3_rsw = (2.34122 * (10 ** − 6))
c4_rsw = (− 2.37049 * ( 10 ** − 9))

a_rsw = a0_rsw + a1_rsw * T + a2_rsw * T * 2 + a3_rsw * T * 3
b_rsw = b0_rsw + b1_rsw * T + b2_rsw * T * 2 + b3_rsw * T * 3
c_rsw = (c0_rsw + c1_rsw * T + c2_rsw * T * 2 + c3_rsw * T3 + c4_rsw * T4) * 10 * - 7  # T em F

RSW = np.zeros(P)

for i in range(0, len(P)):
    RSW[i] = a_rsw + b_rsw * P[i] + c_rsw * P[i] ** 2  # vai calcular a razão de compressibilidade e guardar na linha da vez

# Compressibilidade Isotérmica da Água
a1_cw = 7.033
a2_cw = 0.5415
a3_cw = - 537.0
a4_cw = 403.3

CW = np.zeros(P)

for i in range(0, len(P)):
    CW[i] = 1 / (a1_cw * P[i] + a2_cw * S + a3_cw * T + a4_cw)  # T em F, vai calcular a compressibilidade isotérmica e guardar na linha da vez

# Fator Volume Formação da Água
Vwt = np.zeros(P)
Vwp = np.zeros(P)
BW = np.zeros(P)

for i in range(0, len(P)):
    Vwt[i] = (- 1.0001 * 10 ** - 2) + (1.33391 * 10 ** - 4) * T + (5.50654 * 10 ** - 7) * T ** 2  # vai calular o parêmtro vwt da linha da vez
    Vwp[i] = (- 1.95301 * 10 ** - 9) * P[i] * T - (1.72834 * 10 ** - 13) * (P[i] ** 2) * T - (3.58922 * 10 ** - 7) *P[i] - (2.25341 * 10 ** - 10) * P[i, 1] ** 2  # T em F, vai calcular o parâmetro vwp da linha da vez

    BW[i] = (1 + Vwt[i]) * (1 + Vwp[i])  # vai calcular o fator volume formação e guardar na linha da vez

# Massa Específica da Água onde vamos guardar??????

PW = 62.368 + 0.438603 * S + (1.60074 * 10 ** - 3) * S ** 2

# Viscosidade da Água
a0_uw1 = (109.527)
a1_uw1 = (- 8.40564)
a2_uw1 = (0.313314)
a3_uw1 = (8.72213 * (10 ** − 3))

b0_uw1 = (- 1.12166)
b1_uw1 = (2.63951 * (10 ** − 2))
b2_uw1 = (− 6.79461 * ( 10 ** − 4))
b3_uw1 = (− 5.47119 * ( 10 ** − 5))
b4_uw1 = (− 1.55586 * ( 10 ** − 6))

a_uw1 = a0_uw1 + a1_uw1 * S + a2_uw1 * S ** 2 + a3_uw1 * S ** 3
b_uw1 = b0_uw1 + b1_uw1 * S + b2_uw1 * S ** 2 + b3_uw1 * S ** 3 + b4_uw1 * S ** 4

uw1 = a_uw1 * T ** b_uw1  # T em F

UW = np.zeros(P)

for i in range(0, len(Pvec)):
    UW[i] = uw1 * (0.9994 + (4.0295 * 10 ** - 5) * P[i] + (3.1062 * 10 ** - 9) * P[i] * 2)  # vai calcular a tomada da água e guardar na linha da vez


# ----------------------------------------------TABELAS----------------------------------------------#

#------------------------TABELA FASE ÓLEO-----------------------#

#------------------------TABELA FASE GÁS------------------------#

#------------------------TABELA FASE ÁGUA-----------------------#


# ----------------------------------------------GRÁFICOS----------------------------------------------#

#------------------------GRÁFICOS FASE ÓLEO-----------------------#

# Pressão de Bolha do Óleo
# Razão de Solubilidade Gás-Óleo
# Compressibilidade Isotérmica do Óleo
# Fator Volume-Formação do Óleo
# Massa Específica do Óleo
# Viscosidade Óleo Saturado
# Viscosidade Óleo Sub-Saturado

#------------------------GRÁFICOS FASE GÁS------------------------#

# Fator de Compressibilidade Isotérmica do Gás
# Compressibilidade Isotérmica do Gás
# Fator Volume-Formação do Gás
# Massa Específica do Gás
# Viscosidade do Gás

#------------------------GRÁFICOS FASE ÁGUA-----------------------#

# Razão de Solubilidade Gás-Água
# Compressibilidade Isotérmica da Água
# Fator Volume-Formação da Água
# Massa Específica da Água
# Viscosidade da Água