import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import random

st.set_page_config(
    page_title="Energy Trading Simulator",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0e1a;
    color: #e2e8f0;
}

.block-container { padding: 1.5rem 2.5rem; }

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.stButton > button {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    border-radius: 4px;
    border: 1px solid #334155;
    background: #1e293b;
    color: #94a3b8;
    transition: all 0.2s;
    text-transform: uppercase;
}
.stButton > button:hover {
    border-color: #00d4aa;
    color: #00d4aa;
    background: rgba(0, 212, 170, 0.05);
}
.stButton > button[kind="primary"] {
    background: #00d4aa;
    color: #0a0e1a;
    border-color: #00d4aa;
    font-weight: 700;
}
.stButton > button[kind="primary"]:hover {
    background: #00f0c0;
    border-color: #00f0c0;
    color: #0a0e1a;
}

[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * { color: #94a3b8; }

.stSelectbox > div > div, .stNumberInput > div > div > input,
.stTextInput > div > div > input, .stDateInput > div > div > input {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    border-color: #334155 !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
}

.stSlider > div > div > div { background-color: #334155; }
.stSlider > div > div > div > div { background-color: #00d4aa; }

[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem !important;
    font-weight: 700;
    color: #e2e8f0;
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748b;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
}

div[data-testid="stDataFrame"] {
    border-radius: 6px;
    border: 1px solid #1e293b;
    overflow: hidden;
}

.card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.tag-compra {
    background: rgba(0, 212, 170, 0.15);
    color: #00d4aa;
    border: 1px solid rgba(0, 212, 170, 0.3);
    padding: 2px 10px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
}
.tag-venda {
    background: rgba(251, 113, 133, 0.15);
    color: #fb7185;
    border: 1px solid rgba(251, 113, 133, 0.3);
    padding: 2px 10px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
}

.info-box {
    background: rgba(0, 212, 170, 0.05);
    border-left: 3px solid #00d4aa;
    padding: 0.75rem 1rem;
    border-radius: 0 6px 6px 0;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: #94a3b8;
}

.warn-box {
    background: rgba(251, 191, 36, 0.05);
    border-left: 3px solid #fbbf24;
    padding: 0.75rem 1rem;
    border-radius: 0 6px 6px 0;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: #94a3b8;
}

.mono { font-family: 'JetBrains Mono', monospace; }

hr { border-color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# ── Estado inicial ────────────────────────────────────────────────────────────
if 'contratos' not in st.session_state:
    st.session_state['contratos'] = []
if 'pld_historico' not in st.session_state:
    # Gera PLD simulado dos últimos 24 meses
    base_date = date.today().replace(day=1)
    datas = [base_date - relativedelta(months=i) for i in range(23, -1, -1)]
    plds = []
    pld_atual = 80.0
    for _ in datas:
        pld_atual = max(30, min(500, pld_atual + random.gauss(0, 15)))
        plds.append(round(pld_atual, 2))
    st.session_state['pld_historico'] = pd.DataFrame({'Data': datas, 'PLD (R$/MWh)': plds})
if 'pld_atual' not in st.session_state:
    st.session_state['pld_atual'] = st.session_state['pld_historico']['PLD (R$/MWh)'].iloc[-1]
if 'saldo_caixa' not in st.session_state:
    st.session_state['saldo_caixa'] = 0.0
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'tutorial'
if 'tutorial_etapa' not in st.session_state:
    st.session_state['tutorial_etapa'] = 0
if 'tutorial_concluido' not in st.session_state:
    st.session_state['tutorial_concluido'] = False
if 'missoes_concluidas' not in st.session_state:
    st.session_state['missoes_concluidas'] = set()
if 'quiz_respostas' not in st.session_state:
    st.session_state['quiz_respostas'] = {}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1rem;'>
        <div style='font-family: Syne, sans-serif; font-size: 1.2rem; font-weight: 800;
                    color: #00d4aa; letter-spacing: -0.02em;'>⚡ EnergyTrader</div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.65rem;
                    color: #475569; text-transform: uppercase; letter-spacing: 0.1em;
                    margin-top: 2px;'>Simulador · Mercado Livre</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    pld = st.session_state['pld_atual']
    st.markdown(f"""
    <div style='background:#111827; border:1px solid #1e293b; border-radius:6px;
                padding: 0.75rem 1rem; margin-bottom: 1rem;'>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.6rem;
                    color: #475569; text-transform: uppercase; letter-spacing: 0.1em;'>
            PLD Atual (SE/CO)
        </div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 1.4rem;
                    font-weight: 700; color: #00d4aa; margin-top: 4px;'>
            R$ {pld:.2f}
        </div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.65rem;
                    color: #475569;'>R$/MWh · Simulado</div>
    </div>
    """, unsafe_allow_html=True)

    n_contratos = len(st.session_state['contratos'])
    pnl_total   = sum(c.get('pnl_atual', 0) for c in st.session_state['contratos'])
    st.markdown(f"""
    <div style='display: flex; gap: 8px; margin-bottom: 1rem;'>
        <div style='flex:1; background:#111827; border:1px solid #1e293b; border-radius:6px;
                    padding: 0.6rem 0.75rem;'>
            <div style='font-family: JetBrains Mono, monospace; font-size: 0.55rem;
                        color: #475569; text-transform: uppercase;'>Contratos</div>
            <div style='font-family: JetBrains Mono, monospace; font-size: 1.1rem;
                        font-weight: 700; color: #e2e8f0;'>{n_contratos}</div>
        </div>
        <div style='flex:1; background:#111827; border:1px solid #1e293b; border-radius:6px;
                    padding: 0.6rem 0.75rem;'>
            <div style='font-family: JetBrains Mono, monospace; font-size: 0.55rem;
                        color: #475569; text-transform: uppercase;'>PnL Total</div>
            <div style='font-family: JetBrains Mono, monospace; font-size: 1.1rem;
                        font-weight: 700; color: {"#00d4aa" if pnl_total >= 0 else "#fb7185"};'>
                {"+" if pnl_total >= 0 else ""}R${pnl_total/1000:.1f}k
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    def nav(label, key):
        ativo = st.session_state['pagina'] == key
        style = "color: #00d4aa; font-weight: 700;" if ativo else ""
        st.markdown(f"<div style='{style}'>", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state['pagina'] = key
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    nav("🎓  Tutorial",             "tutorial")
    nav("📊  Painel de Mercado",    "mercado")
    nav("📋  Novo Contrato",        "novo_contrato")
    nav("💼  Meu Portfólio",        "portfolio")
    nav("💰  PnL & Resultado",      "pnl")
    nav("📚  Glossário",            "glossario")

    missoes = st.session_state.get('missoes_concluidas', set())
    total_missoes = 5
    if missoes:
        prog = len(missoes) / total_missoes
        st.markdown(f"""
        <div style='margin-top:0.5rem; padding: 0.6rem 0.75rem; background:#111827;
                    border:1px solid #1e293b; border-radius:6px;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem;
                        color:#475569; text-transform:uppercase; margin-bottom:4px;'>
                Tutorial — {len(missoes)}/{total_missoes} missoes
            </div>
            <div style='background:#1e293b; border-radius:3px; height:4px;'>
                <div style='background:#00d4aa; width:{int(prog*100)}%; height:4px; border-radius:3px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🔄  Atualizar PLD", use_container_width=True):
        novo_pld = max(30, min(500, st.session_state['pld_atual'] + random.gauss(0, 12)))
        st.session_state['pld_atual'] = round(novo_pld, 2)
        nova_linha = pd.DataFrame({'Data': [date.today()], 'PLD (R$/MWh)': [round(novo_pld, 2)]})
        st.session_state['pld_historico'] = pd.concat(
            [st.session_state['pld_historico'], nova_linha], ignore_index=True
        )
        # Recalcula PnL de todos os contratos
        for c in st.session_state['contratos']:
            _recalc_pnl(c)
        st.rerun()

pagina = st.session_state['pagina']

# ── Helpers ───────────────────────────────────────────────────────────────────
def _recalc_pnl(contrato):
    pld = st.session_state['pld_atual']
    preco = contrato['preco']
    volume_mwh = contrato['volume_mw'] * contrato['horas']
    if contrato['tipo'] == 'Compra':
        contrato['pnl_atual'] = (pld - preco) * volume_mwh
    else:
        contrato['pnl_atual'] = (preco - pld) * volume_mwh

def _cor_pnl(v):
    return "#00d4aa" if v >= 0 else "#fb7185"

def _fmt_brl(v):
    sinal = "+" if v >= 0 else ""
    return f"{sinal}R$ {v:,.2f}"

SUBM = {"SE/CO": 1.0, "S": 0.95, "NE": 1.05, "N": 1.10}
TIPOS_ENERGIA = ["Convencional", "Incentivada 50%", "Incentivada 100%"]
INDICES = ["Preço Fixo", "PLD Spot", "PLD Médio Mensal", "IPCA + Spread", "IGP-M + Spread"]

# ════════════════════════════════════════════════════════════════════════════════
# TUTORIAL
# ════════════════════════════════════════════════════════════════════════════════
if pagina == 'tutorial':

    missoes = st.session_state['missoes_concluidas']
    etapa   = st.session_state['tutorial_etapa']

    ETAPAS = [
        {
            "titulo": "Bem-vindo ao Mercado Livre de Energia",
            "icone": "⚡",
            "cor": "#00d4aa",
            "conteudo": """
O **Mercado Livre de Energia** (ACL — Ambiente de Contratação Livre) é onde grandes consumidores,
geradores e comercializadores negociam energia elétrica livremente, sem as restrições do mercado regulado.

**Por que existe o Mercado Livre?**
No Brasil, o setor elétrico é dividido em dois ambientes:
- **ACR (Regulado)**: distribuidoras compram energia em leilões para abastecer residências e pequenas empresas.
- **ACL (Livre)**: consumidores acima de 500 kW negociam diretamente com geradores e comercializadores.

**Quem são os agentes?**
| Agente | Papel |
|--------|-------|
| 🏭 Gerador | Produz energia (hidro, eólica, solar, termo...) |
| 🔄 Comercializador | Compra e revende energia, fazendo a intermediação |
| 🏢 Consumidor Livre | Compra energia diretamente, sem a distribuidora |
| ⚖️ CCEE | Câmara que administra o mercado e liquida as diferenças |

**O papel do PLD:**
O **PLD (Preço de Liquidação das Diferenças)** é o preço do mercado spot, calculado semanalmente pela CCEE.
Ele reflete o custo de gerar mais energia naquele momento — se os reservatórios estão cheios, o PLD é baixo;
se estão vazios e é preciso ligar termoelétricas caras, o PLD sobe.
            """,
            "missao": None,
            "quiz": {
                "pergunta": "O que significa ACL?",
                "opcoes": [
                    "Ambiente de Contratação Livre",
                    "Agência de Controle de Licitações",
                    "Associação de Comercialização de Luz",
                    "Acordo de Custo e Liquidez"
                ],
                "correta": 0,
                "explicacao": "ACL = Ambiente de Contratação Livre, onde consumidores acima de 500 kW negociam energia diretamente."
            }
        },
        {
            "titulo": "Entendendo o PLD",
            "icone": "📈",
            "cor": "#60a5fa",
            "conteudo": """
O **PLD** é o coração do mercado spot de energia. Entender seu comportamento é essencial para qualquer trader.

**Como o PLD é calculado?**
O PLD é derivado do **CMO (Custo Marginal de Operação)** — o custo de atender mais uma unidade de demanda.
O modelo computacional (NEWAVE/DECOMP) simula o sistema elétrico e encontra esse custo ótimo.

**O que influencia o PLD?**

🌧️ **Hidrologia**: Chuvas enchendo reservatórios → PLD cai. Seca → PLD sobe.

⚡ **Demanda**: Alta demanda (verão quente, economia aquecida) → PLD sobe.

🔥 **Termelétricas**: Quando acionadas, adicionam custo e elevam o PLD.

🌬️ **Renováveis**: Muita geração eólica/solar reduz a necessidade de outras fontes → PLD cai.

**Os 4 Submercados:**
O Brasil tem 4 submercados com PLDs diferentes por causa das restrições de transmissão entre regiões:

| Submercado | Sigla | Característica |
|-----------|-------|---------------|
| Sudeste/Centro-Oeste | SE/CO | Principal referência |
| Sul | S | Influenciado pelo vento e hidrologia sulina |
| Nordeste | NE | Alto potencial eólico |
| Norte | N | Grandes hidrelétricas (Tucuruí, Belo Monte) |

**Faixas históricas do PLD:**
- Mínimo regulatório: **R$ 30/MWh** (pode variar por regulação)
- Máximo regulatório: **R$ 500+/MWh** (em crises hídricas)
- Valor "normal": entre **R$ 70–200/MWh**
            """,
            "missao": {
                "id": "missao_pld",
                "titulo": "Missão 1: Observe o PLD",
                "descricao": "Vá até o **Painel de Mercado**, clique em **Atualizar PLD** na sidebar 3 vezes e observe como o valor muda.",
                "verificacao": "pld_atualizado",
                "dica": "O botão 'Atualizar PLD' fica no rodapé da barra lateral esquerda."
            },
            "quiz": {
                "pergunta": "Quando ocorre uma seca severa nos reservatórios, o que tende a acontecer com o PLD?",
                "opcoes": [
                    "O PLD cai, pois há menos energia disponível",
                    "O PLD sobe, pois é necessário acionar termelétricas mais caras",
                    "O PLD não muda, pois é calculado só pela demanda",
                    "O PLD vai a zero para incentivar o consumo"
                ],
                "correta": 1,
                "explicacao": "Com reservatórios baixos, o sistema precisa acionar termelétricas, que têm custo de combustível elevado. Isso eleva o CMO e consequentemente o PLD."
            }
        },
        {
            "titulo": "Contratos Bilaterais e Estratégias",
            "icone": "📋",
            "cor": "#a78bfa",
            "conteudo": """
No ACL, a principal ferramenta do trader é o **contrato bilateral** — um acordo direto entre duas partes.

**Anatomia de um Contrato:**

```
Comprador: Empresa X
Vendedor:  Geradora Solar ABC
Preço:     R$ 120/MWh (FIXO)
Volume:    5 MW médios
Período:   Jan/2025 a Dez/2025
Submercado: SE/CO
Energia:   Incentivada 50%
```

**Estratégias básicas:**

**🟢 COMPRA (Long)**
Você trava um preço de compra esperando que o PLD suba acima dele.
- Lucro: PLD > Preço contratado
- Prejuízo: PLD < Preço contratado

Exemplo: Comprei a R$ 100/MWh. PLD foi a R$ 150/MWh.
Ganho = (150 − 100) × volume = R$ 50/MWh × volume

**🔴 VENDA (Short)**
Você trava um preço de venda esperando que o PLD caia abaixo dele.
- Lucro: PLD < Preço contratado
- Prejuízo: PLD > Preço contratado

Exemplo: Vendi a R$ 120/MWh. PLD caiu para R$ 80/MWh.
Ganho = (120 − 80) × volume = R$ 40/MWh × volume

**⚖️ Posição Líquida (Hedge)**
Um comercializador pode **comprar de geradores** e **vender para consumidores**,
ficando com uma posição equilibrada. O lucro vem do **spread** entre os dois preços.

**Índices de reajuste:**
- **Preço Fixo**: preço não muda durante o contrato
- **PLD Spot**: preço varia com o mercado (máxima exposição)
- **IPCA/IGP-M + Spread**: indexado à inflação (mais comum em contratos longos)
            """,
            "missao": {
                "id": "missao_contrato",
                "titulo": "Missão 2: Registre seu primeiro contrato",
                "descricao": "Vá até **Novo Contrato** e registre um contrato de **Compra** de qualquer volume e preço.",
                "verificacao": "tem_contrato",
                "dica": "Preencha pelo menos o nome do contrato e clique em 'Registrar Contrato'."
            },
            "quiz": {
                "pergunta": "Você comprou energia a R$ 90/MWh. O PLD atual é R$ 130/MWh. Qual é o seu PnL por MWh?",
                "opcoes": [
                    "−R$ 40/MWh (prejuízo)",
                    "+R$ 40/MWh (lucro)",
                    "+R$ 130/MWh",
                    "Zero, pois o preço foi fixado"
                ],
                "correta": 1,
                "explicacao": "Na posição comprada: PnL = PLD − Preço = 130 − 90 = +R$ 40/MWh. Você comprou barato e pode liquidar mais caro no spot."
            }
        },
        {
            "titulo": "Mark to Market e PnL",
            "icone": "💰",
            "cor": "#f59e0b",
            "conteudo": """
**Mark to Market (MtM)** é a reavaliação dos contratos a preços correntes de mercado.
Em vez de esperar o vencimento, você sabe *hoje* quanto valeria liquidar tudo.

**Fórmula do PnL MtM:**

Para posição **comprada**:
```
PnL = (PLD atual − Preço contratado) × Volume (MWh)
```

Para posição **vendida**:
```
PnL = (Preço contratado − PLD atual) × Volume (MWh)
```

**Exemplo prático:**

| Contrato | Tipo | Preço | PLD atual | Volume | PnL |
|---------|------|-------|-----------|--------|-----|
| CTR-001 | Compra | R$ 100 | R$ 140 | 1.000 MWh | +R$ 40.000 |
| CTR-002 | Venda | R$ 160 | R$ 140 | 500 MWh | +R$ 10.000 |
| **Total** | | | | | **+R$ 50.000** |

**Gross-up de PIS/COFINS:**
Quando um contrato inclui impostos embutidos, aplica-se o gross-up:

```
Preço gross-upado = Preço líquido / (1 − 9,25%)
Preço gross-upado = Preço líquido × 1,1025...
```

Exemplo: Preço líquido R$ 100 → Gross-upado ≈ R$ 110,25/MWh

**Por que o gross-up importa?**
No Book de trading, os preços são comparados com a curva de mercado que já embute impostos.
Sem o gross-up, você estaria comparando preços em bases diferentes — como comparar preços com e sem IVA.

**Delta e sensibilidade:**
O **delta** indica quanto seu PnL muda para cada R$ 1 de variação no PLD.
- Posição comprada de 1.000 MWh → Delta = +1.000 (PLD sobe R$1 = ganho de R$1.000)
- Posição vendida de 500 MWh → Delta = −500 (PLD sobe R$1 = perda de R$500)
            """,
            "missao": {
                "id": "missao_pnl",
                "titulo": "Missao 3: Analise o PnL",
                "descricao": "Com pelo menos 1 contrato registrado, acesse **PnL & Resultado** e use o slider para simular o PLD em R$ 200/MWh.",
                "verificacao": "tem_contrato",
                "dica": "Na pagina PnL & Resultado, ha um slider de cenario hipotetico."
            },
            "quiz": {
                "pergunta": "Você tem posição vendida de 2.000 MWh a R$ 150/MWh. O PLD subiu para R$ 180/MWh. Qual o impacto?",
                "opcoes": [
                    "+R$ 60.000 (lucro, pois vendeu caro)",
                    "−R$ 60.000 (prejuízo, pois o mercado foi contra)",
                    "+R$ 30.000",
                    "Zero, pois o preço de venda já estava fixado"
                ],
                "correta": 1,
                "explicacao": "Posição vendida: PnL = (Preço − PLD) × Volume = (150 − 180) × 2000 = −R$ 60.000. Você vendeu a R$150 mas o mercado foi a R$180 — se precisar recomprar, pagará mais caro."
            }
        },
        {
            "titulo": "Energia Incentivada e Estratégias Avancadas",
            "icone": "🌿",
            "cor": "#34d399",
            "conteudo": """
**Energia Incentivada** é gerada por fontes renováveis (solar, eólica, PCH, biomassa) e possui
desconto na TUSD/TUST — a tarifa de uso do sistema de transmissão e distribuição.

**Tipos e descontos:**
| Tipo | Desconto TUSD/TUST | Migração a partir de |
|------|-------------------|---------------------|
| Incentivada 100% | 100% | 30 kW de demanda |
| Incentivada 50% | 50% | 500 kW de demanda |
| Convencional | 0% | 500 kW de demanda |

**Por que o consumidor prefere energia incentivada?**
O desconto na tarifa de transporte pode representar 30–50% da conta de energia total.
Isso permite que o consumidor pague mais pelo MWh no contrato e ainda assim economize.

**Estratégias de portfólio:**

**📦 Book Balanceado (Flat Book)**
Objetivo: posição líquida = 0 MW. Lucro vem apenas do spread compra/venda.
- Risco: baixo (não depende da direção do PLD)
- Ideal para: comercializadores que buscam margem previsível

**📈 Book Direcional**
Objetivo: manter posição comprada ou vendida esperando movimento do PLD.
- Risco: alto (depende de acertar a direção)
- Ideal para: traders com visão de mercado

**🔀 Arbitragem Submercado**
Comprar energia barata em um submercado e vender em outro mais caro.
- Risco: médio (depende de restrições de transmissão)

**⏱️ Arbitragem Temporal**
Comprar energia para entrega futura esperando que o preço spot suba.
- Comum em períodos pré-seca (comprar no úmido, vender no seco)

**Gestão de Risco — Regras de ouro:**
1. Nunca fique com posição muito direcional sem stop-loss definido
2. Monitore o PLD diariamente — uma crise hídrica pode mover centenas de R$/MWh em dias
3. Diversifique entre submercados e tipos de energia
4. Contratos de longo prazo = menor risco de PLD, maior risco de crédito da contraparte
            """,
            "missao": {
                "id": "missao_avancado",
                "titulo": "Missao 4: Monte um portfolio equilibrado",
                "descricao": "Registre pelo menos **2 contratos** — um de Compra e um de Venda — para montar uma posicao parcialmente hedgeada.",
                "verificacao": "tem_compra_e_venda",
                "dica": "Va em Novo Contrato duas vezes, escolhendo tipos diferentes (Compra e Venda)."
            },
            "quiz": {
                "pergunta": "Qual a vantagem da energia incentivada 100% para o consumidor?",
                "opcoes": [
                    "O MWh é sempre mais barato no contrato",
                    "100% de desconto na tarifa de uso da rede (TUSD/TUST)",
                    "Isenção total de impostos federais",
                    "Garantia de fornecimento em qualquer situação"
                ],
                "correta": 1,
                "explicacao": "A energia incentivada 100% garante desconto total na TUSD/TUST, que pode representar grande parte da conta. Isso reduz o custo total mesmo que o MWh no contrato seja um pouco mais caro."
            }
        },
        {
            "titulo": "Desafio Final: Simule uma Crise Hidrica",
            "icone": "🏆",
            "cor": "#f472b6",
            "conteudo": """
Você chegou ao módulo final! Vamos simular um cenário real do mercado brasileiro.

**Cenário: Crise Hídrica 2021**

Em 2021, o Brasil enfrentou a pior seca em 91 anos. Os reservatórios caíram para menos de 20% da capacidade.
O PLD disparou para o valor máximo regulatório (então R$ 583/MWh).

**O que aconteceu com os traders?**

✅ **Vencedores**: Comercializadores que tinham **posição vendida** (venderam caro antes) ou que compraram
energia barata no passado e revenderam no spot com enorme margem.

❌ **Perdedores**: Consumidores com contratos indexados ao PLD spot pagaram contas absurdas.
Comercializadores com posição comprada a preços altos esperando queda do PLD sofreram enormes prejuízos.

**Lições aprendidas:**

1. **Nunca ficar 100% exposto ao spot** sem hedge. Uma seca pode triplicar sua conta.
2. **Contratos de longo prazo** protegem contra volatilidade extrema.
3. **Diversificação de fontes** (eólica no NE não sofre com seca na SE/CO) reduz risco sistêmico.
4. **Reserva de margem** para cobrir variações de MtM é essencial.

**Como usar este simulador para aprender:**

| Ação | Aprendizado |
|------|------------|
| Registre contratos de compra com PLD baixo | Veja o lucro quando o PLD sobe |
| Registre contratos de venda com PLD alto | Veja o lucro quando o PLD cai |
| Use o slider de cenário no PnL | Entenda a sensibilidade do portfólio |
| Clique em Atualizar PLD repetidamente | Simule a volatilidade do mercado |
| Monte posição comprada + vendida | Veja como o hedge reduz o risco |

**Próximos passos reais:**
- Estude o relatório semanal do ONS (Operador Nacional do Sistema)
- Acompanhe as previsões de afluência da CCEE
- Leia os boletins do EPE (Empresa de Pesquisa Energética)
- Pratique no simulador montando diferentes estratégias de portfólio
            """,
            "missao": {
                "id": "missao_final",
                "titulo": "Missao Final: Simule a crise",
                "descricao": "Em **PnL & Resultado**, use o slider e coloque o PLD em **R$ 500/MWh**. Analise o impacto no seu portfolio e veja se sua posicao sobreviveria a uma crise hidrica.",
                "verificacao": "tem_contrato",
                "dica": "Va para PnL & Resultado e arraste o slider de cenario ate R$ 500."
            },
            "quiz": None
        },
    ]

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='display:flex; align-items:center; gap:1rem; margin-bottom:0.5rem;'>
        <div style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800;
                    background: linear-gradient(90deg, #00d4aa, #60a5fa);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🎓 Tutorial Completo
        </div>
    </div>
    <p style='color:#475569; font-size:0.9rem; margin-top:-0.25rem; margin-bottom:1.5rem;'>
        Aprenda o mercado livre de energia do zero, com teoria, exemplos e missoes praticas.
    </p>
    """, unsafe_allow_html=True)

    # ── Progresso geral ──────────────────────────────────────────────────────
    prog_pct = int(len(missoes) / 5 * 100)
    badges = {
        "missao_pld":      ("🌊", "Observador do PLD"),
        "missao_contrato": ("📋", "Primeiro Contrato"),
        "missao_pnl":      ("💰", "Analista de PnL"),
        "missao_avancado": ("⚖️", "Trader Equilibrado"),
        "missao_final":    ("🏆", "Sobrevivente da Crise"),
    }

    st.markdown(f"""
    <div style='background:#111827; border:1px solid #1e293b; border-radius:8px;
                padding:1.25rem 1.5rem; margin-bottom:1.5rem;'>
        <div style='display:flex; justify-content:space-between; align-items:center;
                    margin-bottom:0.6rem;'>
            <span style='font-family:JetBrains Mono,monospace; font-size:0.75rem;
                         color:#94a3b8; text-transform:uppercase; letter-spacing:0.08em;'>
                Progresso Geral
            </span>
            <span style='font-family:JetBrains Mono,monospace; font-size:0.85rem;
                         font-weight:700; color:#00d4aa;'>{prog_pct}%</span>
        </div>
        <div style='background:#1e293b; border-radius:4px; height:6px; margin-bottom:1rem;'>
            <div style='background:linear-gradient(90deg,#00d4aa,#60a5fa);
                        width:{prog_pct}%; height:6px; border-radius:4px;
                        transition: width 0.5s;'></div>
        </div>
        <div style='display:flex; gap:0.75rem; flex-wrap:wrap;'>
    """, unsafe_allow_html=True)

    for mid, (icon, nome) in badges.items():
        conquistado = mid in missoes
        st.markdown(f"""
        <div style='padding:0.4rem 0.75rem; border-radius:20px; font-size:0.75rem;
                    font-family:JetBrains Mono,monospace;
                    background:{"rgba(0,212,170,0.1)" if conquistado else "#1e293b"};
                    border:1px solid {"rgba(0,212,170,0.4)" if conquistado else "#334155"};
                    color:{"#00d4aa" if conquistado else "#475569"};'>
            {icon} {nome}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Navegação entre módulos ──────────────────────────────────────────────
    tabs_labels = [f"{e['icone']} Módulo {i+1}" for i, e in enumerate(ETAPAS)]
    tabs = st.tabs(tabs_labels)

    for i, (tab, etapa_info) in enumerate(zip(tabs, ETAPAS)):
        with tab:
            cor = etapa_info['cor']

            # Header do módulo
            st.markdown(f"""
            <div style='border-left:4px solid {cor}; padding:0.5rem 0 0.5rem 1rem;
                        margin-bottom:1rem;'>
                <div style='font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800;
                            color:{cor};'>{etapa_info["icone"]} {etapa_info["titulo"]}</div>
                <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                            color:#475569; text-transform:uppercase; letter-spacing:0.1em;
                            margin-top:2px;'>Módulo {i+1} de {len(ETAPAS)}</div>
            </div>
            """, unsafe_allow_html=True)

            # Conteúdo teórico
            st.markdown(etapa_info["conteudo"])

            # Missão prática
            if etapa_info["missao"]:
                missao = etapa_info["missao"]
                mid    = missao["id"]
                concluida = mid in missoes

                # Verifica automaticamente se missão foi cumprida
                auto_verificar = False
                if mid == "missao_pld":
                    auto_verificar = len(st.session_state['pld_historico']) > 26
                elif mid in ("missao_contrato", "missao_pnl", "missao_final"):
                    auto_verificar = len(st.session_state['contratos']) > 0
                elif mid == "missao_avancado":
                    tipos = [c['tipo'] for c in st.session_state['contratos']]
                    auto_verificar = 'Compra' in tipos and 'Venda' in tipos

                if auto_verificar and not concluida:
                    st.session_state['missoes_concluidas'].add(mid)
                    concluida = True

                status_cor  = "#00d4aa" if concluida else cor
                status_icon = "✅" if concluida else "🎯"
                status_txt  = "CONCLUÍDA" if concluida else "PENDENTE"

                st.markdown(f"""
                <div style='background:{"rgba(0,212,170,0.05)" if concluida else "rgba(0,0,0,0)"};
                            border:1px solid {"rgba(0,212,170,0.3)" if concluida else "#1e293b"};
                            border-radius:8px; padding:1.25rem 1.5rem; margin:1.5rem 0;'>
                    <div style='display:flex; justify-content:space-between; align-items:center;
                                margin-bottom:0.75rem;'>
                        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:0.95rem;
                                    color:{status_cor};'>{status_icon} {missao["titulo"]}</div>
                        <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                                    color:{status_cor}; background:{"rgba(0,212,170,0.1)" if concluida else "#1e293b"};
                                    padding:2px 8px; border-radius:3px; letter-spacing:0.1em;'>
                            {status_txt}
                        </div>
                    </div>
                    <div style='font-size:0.875rem; color:#94a3b8; line-height:1.6;
                                margin-bottom:0.75rem;'>{missao["descricao"]}</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.75rem;
                                color:#475569;'>💡 Dica: {missao["dica"]}</div>
                </div>
                """, unsafe_allow_html=True)

                if not concluida:
                    col_m1, col_m2 = st.columns([1, 3])
                    with col_m1:
                        if st.button(f"✓ Marcar como concluída", key=f"marca_{mid}"):
                            st.session_state['missoes_concluidas'].add(mid)
                            st.rerun()

            # Quiz
            if etapa_info["quiz"]:
                quiz = etapa_info["quiz"]
                qkey = f"quiz_{i}"
                respondida = qkey in st.session_state['quiz_respostas']

                st.markdown(f"""
                <div style='background:#0d1117; border:1px solid #1e293b; border-radius:8px;
                            padding:1.25rem 1.5rem; margin-top:1.5rem;'>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                                color:#475569; text-transform:uppercase; letter-spacing:0.1em;
                                margin-bottom:0.75rem;'>📝 Quiz de Fixação</div>
                    <div style='font-family:Syne,sans-serif; font-size:0.95rem; color:#e2e8f0;
                                margin-bottom:0.75rem;'>{quiz["pergunta"]}</div>
                """, unsafe_allow_html=True)

                if not respondida:
                    resposta = st.radio(
                        "Escolha sua resposta:",
                        quiz["opcoes"],
                        key=f"radio_{i}",
                        label_visibility="collapsed"
                    )
                    if st.button("Confirmar resposta", key=f"confirma_{i}"):
                        idx = quiz["opcoes"].index(resposta)
                        st.session_state['quiz_respostas'][qkey] = idx
                        st.rerun()
                else:
                    resp_idx = st.session_state['quiz_respostas'][qkey]
                    correta  = quiz["correta"]
                    acertou  = resp_idx == correta

                    for j, opcao in enumerate(quiz["opcoes"]):
                        if j == correta:
                            icon_o = "✅"
                            cor_o  = "#00d4aa"
                        elif j == resp_idx and not acertou:
                            icon_o = "❌"
                            cor_o  = "#fb7185"
                        else:
                            icon_o = "○"
                            cor_o  = "#334155"
                        st.markdown(f"""
                        <div style='font-family:JetBrains Mono,monospace; font-size:0.82rem;
                                    color:{cor_o}; padding:4px 0;'>{icon_o} {opcao}</div>
                        """, unsafe_allow_html=True)

                    resultado_txt = "✅ Correto!" if acertou else "❌ Não foi dessa vez."
                    resultado_cor = "#00d4aa" if acertou else "#fb7185"
                    st.markdown(f"""
                    <div style='margin-top:0.75rem; padding:0.75rem 1rem;
                                background:{"rgba(0,212,170,0.05)" if acertou else "rgba(251,113,133,0.05)"};
                                border-left:3px solid {resultado_cor}; border-radius:0 6px 6px 0;
                                font-size:0.85rem; color:#94a3b8;'>
                        <b style='color:{resultado_cor};'>{resultado_txt}</b><br>
                        {quiz["explicacao"]}
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button("Tentar novamente", key=f"retry_{i}"):
                        del st.session_state['quiz_respostas'][qkey]
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    # ── Certificado ──────────────────────────────────────────────────────────
    if len(missoes) >= 5:
        st.markdown("---")
        quizzes_corretos = sum(
            1 for k, v in st.session_state['quiz_respostas'].items()
            if v == ETAPAS[int(k.split('_')[1])]['quiz']['correta']
            if ETAPAS[int(k.split('_')[1])]['quiz'] is not None
        )
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,rgba(0,212,170,0.08),rgba(96,165,250,0.08));
                    border:1px solid rgba(0,212,170,0.3); border-radius:12px;
                    padding:2rem; text-align:center; margin-top:1rem;'>
            <div style='font-size:3rem; margin-bottom:0.5rem;'>🏆</div>
            <div style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:800;
                        background:linear-gradient(90deg,#00d4aa,#60a5fa);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
                Tutorial Concluído!
            </div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.85rem;
                        color:#64748b; margin-top:0.5rem;'>
                Você completou todas as 5 missões e demonstrou conhecimento no mercado livre de energia.
            </div>
            <div style='display:flex; justify-content:center; gap:2rem; margin-top:1.25rem;'>
                <div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.8rem;
                                font-weight:700; color:#00d4aa;'>5/5</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                                color:#475569; text-transform:uppercase;'>Missões</div>
                </div>
                <div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.8rem;
                                font-weight:700; color:#60a5fa;'>{quizzes_corretos}/4</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                                color:#475569; text-transform:uppercase;'>Quizzes certos</div>
                </div>
            </div>
            <div style='margin-top:1.25rem; font-family:JetBrains Mono,monospace;
                        font-size:0.8rem; color:#475569;'>
                Agora explore o simulador livremente — registre contratos, atualize o PLD e treine suas estratégias!
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAINEL DE MERCADO
# ════════════════════════════════════════════════════════════════════════════════
if pagina == 'mercado':

    st.markdown("# 📊 Painel de Mercado")
    st.markdown("<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Visão geral do mercado livre de energia elétrica</p>", unsafe_allow_html=True)
    st.markdown("---")

    pld = st.session_state['pld_atual']
    df_hist = st.session_state['pld_historico']
    var_pld  = pld - df_hist['PLD (R$/MWh)'].iloc[-2] if len(df_hist) > 1 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PLD SE/CO", f"R$ {pld:.2f}", f"{var_pld:+.2f} R$/MWh")
    c2.metric("PLD Sul",   f"R$ {pld * SUBM['S']:.2f}",  "−5% SE/CO")
    c3.metric("PLD NE",    f"R$ {pld * SUBM['NE']:.2f}", "+5% SE/CO")
    c4.metric("PLD Norte", f"R$ {pld * SUBM['N']:.2f}",  "+10% SE/CO")

    st.markdown("")
    col_graf, col_info = st.columns([3, 1])

    with col_graf:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_hist['Data'].astype(str),
            y=df_hist['PLD (R$/MWh)'],
            mode='lines',
            line=dict(color='#00d4aa', width=2),
            fill='tozeroy',
            fillcolor='rgba(0,212,170,0.07)',
            name='PLD SE/CO',
            hovertemplate='%{x}<br>PLD: R$ %{y:.2f}<extra></extra>'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569'),
            yaxis=dict(gridcolor='#1e293b', color='#475569', title='R$/MWh'),
            margin=dict(l=10, r=10, t=30, b=10), height=300,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
            title=dict(text='Histórico PLD SE/CO (Simulado)', font=dict(size=13, color='#94a3b8'))
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("""
        <div class='card'>
            <div style='font-family: JetBrains Mono, monospace; font-size: 0.65rem;
                        color: #475569; text-transform: uppercase; letter-spacing: 0.1em;
                        margin-bottom: 0.75rem;'>Estatísticas (24m)</div>
        """, unsafe_allow_html=True)
        stats = {
            "Mínimo":  df_hist['PLD (R$/MWh)'].min(),
            "Máximo":  df_hist['PLD (R$/MWh)'].max(),
            "Média":   df_hist['PLD (R$/MWh)'].mean(),
            "Desvio":  df_hist['PLD (R$/MWh)'].std(),
        }
        for k, v in stats.items():
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; padding: 4px 0;
                        border-bottom: 1px solid #1e293b; font-family: JetBrains Mono, monospace;
                        font-size: 0.8rem;'>
                <span style='color:#64748b;'>{k}</span>
                <span style='color:#e2e8f0;'>R$ {v:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💡 Como funciona o Mercado Livre de Energia?")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div class='card'>
            <div style='font-size:1.5rem; margin-bottom:0.5rem;'>🏭</div>
            <div style='font-weight:700; color:#e2e8f0; margin-bottom:0.4rem;'>Agentes</div>
            <div style='font-size:0.82rem; color:#64748b; line-height:1.6;'>
                <b style='color:#94a3b8;'>Geradores</b> produzem energia e a vendem.
                <b style='color:#94a3b8;'>Comercializadores</b> compram e revendem.
                <b style='color:#94a3b8;'>Consumidores Livres</b> negociam diretamente
                (acima de 500 kW).
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class='card'>
            <div style='font-size:1.5rem; margin-bottom:0.5rem;'>📈</div>
            <div style='font-weight:700; color:#e2e8f0; margin-bottom:0.4rem;'>PLD</div>
            <div style='font-size:0.82rem; color:#64748b; line-height:1.6;'>
                O <b style='color:#94a3b8;'>Preço de Liquidação das Diferenças</b> é calculado
                semanalmente pela CCEE. Serve como referência para liquidar contratos e
                reflete o custo marginal de operação do sistema.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div class='card'>
            <div style='font-size:1.5rem; margin-bottom:0.5rem;'>⚖️</div>
            <div style='font-weight:700; color:#e2e8f0; margin-bottom:0.4rem;'>Contrato vs Spot</div>
            <div style='font-size:0.82rem; color:#64748b; line-height:1.6;'>
                Você pode travar um <b style='color:#94a3b8;'>preço fixo</b> por contrato bilateral,
                ou ficar exposto ao <b style='color:#94a3b8;'>PLD (spot)</b>.
                A diferença entre os dois gera o PnL do trader.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔢 Calculadora Rápida de Exposição")

    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        vol_calc = st.number_input("Volume (MW médio)", min_value=0.1, value=5.0, step=0.5)
    with cc2:
        preco_calc = st.number_input("Preço Contratado (R$/MWh)", min_value=0.0, value=float(round(pld, 0)), step=1.0)
    with cc3:
        horas_calc = st.number_input("Horas do período", min_value=1, value=720, step=24)

    vol_total   = vol_calc * horas_calc
    exposicao   = (pld - preco_calc) * vol_total
    st.markdown(f"""
    <div style='display:flex; gap:1rem; margin-top:0.5rem;'>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                        color:#475569; text-transform:uppercase;'>Volume Total</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.3rem;
                        font-weight:700; color:#e2e8f0;'>{vol_total:,.0f} MWh</div>
        </div>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                        color:#475569; text-transform:uppercase;'>PnL se comprado</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.3rem;
                        font-weight:700; color:{_cor_pnl(exposicao)};'>{_fmt_brl(exposicao)}</div>
        </div>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                        color:#475569; text-transform:uppercase;'>PnL se vendido</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.3rem;
                        font-weight:700; color:{_cor_pnl(-exposicao)};'>{_fmt_brl(-exposicao)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# NOVO CONTRATO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'novo_contrato':

    st.markdown("# 📋 Novo Contrato")
    st.markdown("<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Monte e registre um contrato bilateral de energia</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div class='info-box'>
        💡 <b>Como funciona:</b> Um contrato bilateral é um acordo entre comprador e vendedor com
        preço, volume e período definidos. Ao registrar aqui, o simulador calculará seu PnL
        comparando o preço acordado com o PLD atual.
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_contrato"):
        st.markdown("#### Identificação")
        col1, col2 = st.columns(2)
        with col1:
            nome_contrato = st.text_input("Nome / Referência do Contrato", placeholder="ex: CONTRATO-001")
        with col2:
            contraparte   = st.text_input("Contraparte", placeholder="ex: Geradora Solar ABC")

        st.markdown("#### Operação")
        col3, col4, col5 = st.columns(3)
        with col3:
            tipo_op = st.selectbox("Tipo de Operação", ["Compra", "Venda"],
                                   help="Compra: você está comprando energia. Venda: você está vendendo.")
        with col4:
            submercado = st.selectbox("Submercado", list(SUBM.keys()))
        with col5:
            tipo_energia = st.selectbox("Tipo de Energia", TIPOS_ENERGIA)

        st.markdown("#### Preço e Volume")
        col6, col7, col8 = st.columns(3)
        with col6:
            preco = st.number_input("Preço (R$/MWh)", min_value=0.01, value=float(round(st.session_state['pld_atual'], 0)), step=1.0)
        with col7:
            volume_mw = st.number_input("Volume (MW médio)", min_value=0.1, value=1.0, step=0.5)
        with col8:
            indice = st.selectbox("Índice de Reajuste", INDICES)

        st.markdown("#### Vigência")
        col9, col10 = st.columns(2)
        with col9:
            data_inicio = st.date_input("Data de Início", value=date.today().replace(day=1))
        with col10:
            data_fim = st.date_input("Data de Fim", value=(date.today().replace(day=1) + relativedelta(months=11)))

        st.markdown("#### Gross-up")
        col11, col12 = st.columns(2)
        with col11:
            gross_up = st.checkbox("Aplicar Gross-up de PIS/COFINS (9,25%)", value=False)
        with col12:
            flag_pc = st.checkbox("Marcar flag P/C na boleta", value=False)

        obs = st.text_area("Observações", placeholder="Notas adicionais sobre o contrato...", height=80)

        submitted = st.form_submit_button("✅  REGISTRAR CONTRATO", type="primary", use_container_width=True)

    if submitted:
        if not nome_contrato:
            st.error("⚠️ Informe o nome do contrato.")
        elif data_fim <= data_inicio:
            st.error("⚠️ A data de fim deve ser posterior à data de início.")
        else:
            delta     = data_fim - data_inicio
            horas     = int(delta.days * 24)
            preco_adj = preco * 1.0925 if gross_up else preco

            novo = {
                'id':           len(st.session_state['contratos']) + 1,
                'nome':         nome_contrato,
                'contraparte':  contraparte,
                'tipo':         tipo_op,
                'submercado':   submercado,
                'tipo_energia': tipo_energia,
                'preco':        preco_adj,
                'preco_orig':   preco,
                'volume_mw':    volume_mw,
                'indice':       indice,
                'data_inicio':  data_inicio,
                'data_fim':     data_fim,
                'horas':        horas,
                'gross_up':     gross_up,
                'flag_pc':      flag_pc,
                'obs':          obs,
                'pnl_atual':    0.0,
                'criado_em':    datetime.now(),
            }
            _recalc_pnl(novo)
            st.session_state['contratos'].append(novo)

            vol_total_mwh = volume_mw * horas
            receita_bruta = preco_adj * vol_total_mwh

            st.success(f"✅ Contrato **{nome_contrato}** registrado com sucesso!")
            st.markdown(f"""
            <div style='display:flex; gap:1rem; margin-top:0.5rem;'>
                <div class='card' style='flex:1;'>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem;
                                color:#475569; text-transform:uppercase;'>Volume Total</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.2rem;
                                font-weight:700; color:#e2e8f0;'>{vol_total_mwh:,.0f} MWh</div>
                </div>
                <div class='card' style='flex:1;'>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem;
                                color:#475569; text-transform:uppercase;'>Receita Bruta</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.2rem;
                                font-weight:700; color:#e2e8f0;'>R$ {receita_bruta:,.2f}</div>
                </div>
                <div class='card' style='flex:1;'>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem;
                                color:#475569; text-transform:uppercase;'>PnL vs PLD atual</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.2rem;
                                font-weight:700; color:{_cor_pnl(novo["pnl_atual"])};'>
                        {_fmt_brl(novo["pnl_atual"])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# PORTFÓLIO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'portfolio':

    st.markdown("# 💼 Meu Portfólio")
    st.markdown("<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Todos os contratos registrados</p>", unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state['contratos']:
        st.markdown("""
        <div class='warn-box'>
            ⚠️ Nenhum contrato registrado ainda. Acesse <b>Novo Contrato</b> para começar a operar.
        </div>
        """, unsafe_allow_html=True)
    else:
        contratos = st.session_state['contratos']

        pos_compra = sum(c['volume_mw'] for c in contratos if c['tipo'] == 'Compra')
        pos_venda  = sum(c['volume_mw'] for c in contratos if c['tipo'] == 'Venda')
        pos_liq    = pos_compra - pos_venda

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Posição Comprada", f"{pos_compra:.1f} MW")
        m2.metric("Posição Vendida",  f"{pos_venda:.1f} MW")
        m3.metric("Posição Líquida",  f"{pos_liq:+.1f} MW",
                  delta="Comprado" if pos_liq > 0 else "Vendido" if pos_liq < 0 else "Zerado")
        m4.metric("Contratos Ativos", len(contratos))

        st.markdown("")

        for c in contratos:
            tag_html = f"<span class='tag-{'compra' if c['tipo']=='Compra' else 'venda'}'>{c['tipo'].upper()}</span>"
            pnl_cor  = _cor_pnl(c['pnl_atual'])

            with st.expander(f"#{c['id']} — {c['nome']}  |  {c['volume_mw']} MW  |  R$ {c['preco']:.2f}/MWh", expanded=False):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.markdown(f"""
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; line-height:2;'>
                        <b style='color:#64748b;'>Tipo:</b> {tag_html}<br>
                        <b style='color:#64748b;'>Contraparte:</b> <span style='color:#e2e8f0;'>{c['contraparte'] or '—'}</span><br>
                        <b style='color:#64748b;'>Submercado:</b> <span style='color:#e2e8f0;'>{c['submercado']}</span><br>
                        <b style='color:#64748b;'>Energia:</b> <span style='color:#e2e8f0;'>{c['tipo_energia']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; line-height:2;'>
                        <b style='color:#64748b;'>Preço:</b> <span style='color:#e2e8f0;'>R$ {c['preco']:.2f}/MWh</span><br>
                        <b style='color:#64748b;'>Volume:</b> <span style='color:#e2e8f0;'>{c['volume_mw']} MW</span><br>
                        <b style='color:#64748b;'>Horas:</b> <span style='color:#e2e8f0;'>{c['horas']:,} h</span><br>
                        <b style='color:#64748b;'>Índice:</b> <span style='color:#e2e8f0;'>{c['indice']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_c:
                    st.markdown(f"""
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; line-height:2;'>
                        <b style='color:#64748b;'>Início:</b> <span style='color:#e2e8f0;'>{c['data_inicio']}</span><br>
                        <b style='color:#64748b;'>Fim:</b> <span style='color:#e2e8f0;'>{c['data_fim']}</span><br>
                        <b style='color:#64748b;'>Gross-up:</b> <span style='color:#e2e8f0;'>{'✓ 9,25%' if c['gross_up'] else '—'}</span><br>
                        <b style='color:#64748b;'>Flag P/C:</b> <span style='color:#e2e8f0;'>{'✓' if c['flag_pc'] else '—'}</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style='margin-top:0.75rem; padding:0.75rem 1rem; background:#0d1117;
                            border-radius:6px; display:flex; justify-content:space-between;
                            align-items:center;'>
                    <span style='font-family:JetBrains Mono,monospace; font-size:0.7rem;
                                 color:#475569; text-transform:uppercase;'>PnL vs PLD Atual</span>
                    <span style='font-family:JetBrains Mono,monospace; font-size:1.1rem;
                                 font-weight:700; color:{pnl_cor};'>{_fmt_brl(c['pnl_atual'])}</span>
                </div>
                """, unsafe_allow_html=True)

                if c['obs']:
                    st.markdown(f"<div class='info-box'>📝 {c['obs']}</div>", unsafe_allow_html=True)

                if st.button(f"🗑️ Remover contrato #{c['id']}", key=f"del_{c['id']}"):
                    st.session_state['contratos'] = [x for x in st.session_state['contratos'] if x['id'] != c['id']]
                    st.rerun()


# ════════════════════════════════════════════════════════════════════════════════
# PnL & RESULTADO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'pnl':

    st.markdown("# 💰 PnL & Resultado")
    st.markdown("<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Análise de resultado do portfólio</p>", unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state['contratos']:
        st.markdown("<div class='warn-box'>⚠️ Nenhum contrato registrado ainda.</div>", unsafe_allow_html=True)
    else:
        contratos = st.session_state['contratos']
        pld       = st.session_state['pld_atual']

        pnl_total    = sum(c['pnl_atual'] for c in contratos)
        pnl_compras  = sum(c['pnl_atual'] for c in contratos if c['tipo'] == 'Compra')
        pnl_vendas   = sum(c['pnl_atual'] for c in contratos if c['tipo'] == 'Venda')
        vol_total    = sum(c['volume_mw'] * c['horas'] for c in contratos)
        receita_tot  = sum(c['preco'] * c['volume_mw'] * c['horas'] for c in contratos)

        m1, m2, m3 = st.columns(3)
        m1.metric("PnL Total",        _fmt_brl(pnl_total),   delta=f"{'▲' if pnl_total>=0 else '▼'} vs PLD R${pld:.2f}")
        m2.metric("PnL Compras",      _fmt_brl(pnl_compras))
        m3.metric("PnL Vendas",       _fmt_brl(pnl_vendas))

        st.markdown("")

        # Gráfico de barras por contrato
        nomes  = [c['nome'] for c in contratos]
        pnls   = [c['pnl_atual'] for c in contratos]
        cores  = ['#00d4aa' if v >= 0 else '#fb7185' for v in pnls]

        fig_bar = go.Figure(go.Bar(
            x=nomes, y=pnls,
            marker_color=cores,
            text=[_fmt_brl(v) for v in pnls],
            textposition='outside',
            textfont=dict(family='JetBrains Mono', size=11),
            hovertemplate='%{x}<br>PnL: R$ %{y:,.2f}<extra></extra>'
        ))
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569'),
            yaxis=dict(gridcolor='#1e293b', color='#475569', title='PnL (R$)'),
            margin=dict(l=10, r=10, t=40, b=10), height=320,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
            title=dict(text='PnL por Contrato vs PLD Atual', font=dict(size=13, color='#94a3b8'))
        )
        fig_bar.add_shape(type='line', x0=-0.5, x1=len(nomes)-0.5, y0=0, y1=0,
                          line=dict(color='#475569', width=1, dash='dash'))
        st.plotly_chart(fig_bar, use_container_width=True)

        # Simulador de cenário
        st.markdown("---")
        st.markdown("#### 🔮 Simulador de Cenário")
        st.markdown("""
        <div class='info-box'>
            Arraste o PLD hipotético para ver como seu portfólio se comportaria em diferentes cenários.
        </div>
        """, unsafe_allow_html=True)

        pld_sim = st.slider(
            "PLD Hipotético (R$/MWh)",
            min_value=30.0, max_value=500.0,
            value=float(round(pld, 0)), step=5.0
        )

        pnl_sim_list = []
        for c in contratos:
            vol = c['volume_mw'] * c['horas']
            if c['tipo'] == 'Compra':
                pnl_sim_list.append((pld_sim - c['preco']) * vol)
            else:
                pnl_sim_list.append((c['preco'] - pld_sim) * vol)

        pnl_sim_total = sum(pnl_sim_list)
        delta_cenario = pnl_sim_total - pnl_total

        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("PLD Hipotético",   f"R$ {pld_sim:.2f}/MWh", f"{pld_sim - pld:+.2f} vs atual")
        sc2.metric("PnL no Cenário",   _fmt_brl(pnl_sim_total))
        sc3.metric("Variação vs Atual", _fmt_brl(delta_cenario),  delta=f"{delta_cenario:+.2f}")

        # Curva de sensibilidade
        pld_range  = np.linspace(30, 500, 200)
        pnl_range  = []
        for p in pld_range:
            total_s = 0
            for c in contratos:
                v = c['volume_mw'] * c['horas']
                total_s += (p - c['preco']) * v if c['tipo'] == 'Compra' else (c['preco'] - p) * v
            pnl_range.append(total_s)

        fig_sens = go.Figure()
        fig_sens.add_trace(go.Scatter(
            x=pld_range, y=pnl_range,
            mode='lines', line=dict(color='#00d4aa', width=2),
            fill='tozeroy', fillcolor='rgba(0,212,170,0.05)',
            name='PnL Portfólio',
            hovertemplate='PLD: R$ %{x:.0f}<br>PnL: R$ %{y:,.0f}<extra></extra>'
        ))
        fig_sens.add_vline(x=pld, line_color='#94a3b8', line_dash='dash',
                           annotation_text=f"PLD atual: R${pld:.0f}",
                           annotation_font_color='#94a3b8')
        fig_sens.add_vline(x=pld_sim, line_color='#fbbf24', line_dash='dot',
                           annotation_text=f"Cenário: R${pld_sim:.0f}",
                           annotation_font_color='#fbbf24')
        fig_sens.add_hline(y=0, line_color='#475569', line_dash='dash')
        fig_sens.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569', title='PLD (R$/MWh)'),
            yaxis=dict(gridcolor='#1e293b', color='#475569', title='PnL (R$)'),
            margin=dict(l=10, r=10, t=40, b=10), height=320,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
            title=dict(text='Sensibilidade do Portfólio ao PLD', font=dict(size=13, color='#94a3b8'))
        )
        st.plotly_chart(fig_sens, use_container_width=True)

        # Tabela resumo
        st.markdown("---")
        st.markdown("#### 📊 Tabela Resumo")
        rows = []
        for c, pnl_s in zip(contratos, pnl_sim_list):
            rows.append({
                'Contrato':      c['nome'],
                'Tipo':          c['tipo'],
                'Submercado':    c['submercado'],
                'Preço (R$/MWh)': f"{c['preco']:.2f}",
                'Volume (MW)':   c['volume_mw'],
                'PnL Atual (R$)': c['pnl_atual'],
                'PnL Cenário (R$)': pnl_s,
            })
        df_res = pd.DataFrame(rows)
        st.dataframe(
            df_res.style
                .format({'PnL Atual (R$)': '{:,.2f}', 'PnL Cenário (R$)': '{:,.2f}'})
                .applymap(lambda v: f'color: {"#00d4aa" if v >= 0 else "#fb7185"}',
                          subset=['PnL Atual (R$)', 'PnL Cenário (R$)'])
                .set_properties(**{'text-align': 'center', 'font-family': 'JetBrains Mono, monospace'})
                .set_table_styles([{'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'center')]}]),
            use_container_width=True, hide_index=True
        )


# ════════════════════════════════════════════════════════════════════════════════
# GLOSSÁRIO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'glossario':

    st.markdown("# 📚 Glossário")
    st.markdown("<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Conceitos essenciais do mercado livre de energia</p>", unsafe_allow_html=True)
    st.markdown("---")

    termos = [
        ("PLD — Preço de Liquidação das Diferenças",
         "Preço calculado semanalmente pela CCEE com base no Custo Marginal de Operação (CMO) do sistema elétrico. "
         "Reflete o custo de se produzir mais uma unidade de energia naquele momento. "
         "É o principal referencial de preço no mercado de curto prazo."),

        ("CMO — Custo Marginal de Operação",
         "Custo de se atender a mais uma unidade de demanda no sistema. Em períodos secos, com reservatórios baixos, "
         "o CMO sobe porque é necessário acionar termoelétricas mais caras. Em períodos úmidos, o CMO cai."),

        ("ACL — Ambiente de Contratação Livre",
         "Segmento do mercado onde consumidores com demanda acima de 500 kW podem comprar energia livremente "
         "de qualquer gerador ou comercializador, negociando preço, prazo e condições."),

        ("ACR — Ambiente de Contratação Regulada",
         "Segmento onde distribuidoras compram energia em leilões regulados pela ANEEL para atender "
         "consumidores cativos (residências, pequenas empresas etc.)."),

        ("Submercado",
         "O Brasil é dividido em 4 submercados: SE/CO (Sudeste/Centro-Oeste), S (Sul), NE (Nordeste) e N (Norte). "
         "Cada um tem seu próprio PLD, que pode diferir dos demais por conta de restrições de transmissão."),

        ("Posição Comprada (Long)",
         "Quando você comprou mais energia do que vendeu. Você se beneficia quando o PLD sobe acima do seu preço de compra, "
         "pois pode revender no spot com lucro."),

        ("Posição Vendida (Short)",
         "Quando você vendeu mais energia do que comprou. Você se beneficia quando o PLD cai abaixo do seu preço de venda."),

        ("Gross-up de PIS/COFINS",
         "Ajuste no preço da energia para embutir os impostos PIS/COFINS (alíquota de 9,25%). "
         "Usado para que o preço líquido após impostos corresponda ao valor acordado. "
         "Fórmula: Preço Gross-up = Preço / (1 − 9,25%)."),

        ("Mark to Market (MtM)",
         "Reavaliação dos contratos a preços de mercado correntes (PLD atual). "
         "O PnL MtM mostra quanto você ganharia ou perderia se liquidasse tudo hoje."),

        ("Contrato Bilateral",
         "Acordo direto entre duas partes (comprador e vendedor) fora do ambiente de leilão. "
         "Permite flexibilidade total na negociação de preço, prazo, volume e índice de reajuste."),

        ("Energia Incentivada",
         "Energia proveniente de fontes renováveis (solar, eólica, PCH, biomassa) que possui desconto "
         "de 50% ou 100% na TUSD/TUST. Consumidores que compram esse tipo de energia podem migrar ao ACL "
         "com demanda a partir de 500 kW (50%) ou 30 kW (100%)."),

        ("CCEE — Câmara de Comercialização de Energia Elétrica",
         "Entidade que administra o mercado de curto prazo (spot) no Brasil. "
         "Calcula e publica o PLD, realiza a liquidação financeira das diferenças entre "
         "o contratado e o consumido/gerado."),

        ("Delta",
         "Variação do PnL para uma variação unitária no PLD. Indica a sensibilidade do portfólio. "
         "Um delta positivo (posição comprada) significa que o portfólio ganha quando o PLD sobe."),

        ("Spread",
         "Diferença entre o preço de compra e o preço de venda. "
         "O lucro de um comercializador vem em parte desse spread entre o que paga ao gerador "
         "e o que cobra do consumidor."),
    ]

    for termo, definicao in termos:
        with st.expander(f"📌 {termo}"):
            st.markdown(f"""
            <div style='font-family: Syne, sans-serif; font-size: 0.88rem;
                        color: #94a3b8; line-height: 1.7; padding: 0.25rem 0;'>
                {definicao}
            </div>
            """, unsafe_allow_html=True)