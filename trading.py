import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import random
import json
import os
import math

st.set_page_config(
    page_title="EnergyTrader v4",
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
h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; letter-spacing: -0.02em; }

.stButton > button {
    font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 600;
    letter-spacing: 0.08em; border-radius: 4px; border: 1px solid #334155;
    background: #1e293b; color: #94a3b8; transition: all 0.2s; text-transform: uppercase;
}
.stButton > button:hover { border-color: #00d4aa; color: #00d4aa; background: rgba(0,212,170,0.05); }
.stButton > button[kind="primary"] { background: #00d4aa; color: #0a0e1a; border-color: #00d4aa; font-weight: 700; }
.stButton > button[kind="primary"]:hover { background: #00f0c0; border-color: #00f0c0; color: #0a0e1a; }

[data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #1e293b; }
[data-testid="stSidebar"] * { color: #94a3b8; }

.stSelectbox > div > div, .stNumberInput > div > div > input,
.stTextInput > div > div > input, .stDateInput > div > div > input {
    background-color: #1e293b !important; color: #e2e8f0 !important;
    border-color: #334155 !important; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
}
.stSlider > div > div > div { background-color: #334155; }
.stSlider > div > div > div > div { background-color: #00d4aa; }
[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; font-size: 1.6rem !important; font-weight: 700; color: #e2e8f0; }
[data-testid="stMetricLabel"] { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: #64748b; }
[data-testid="stMetricDelta"] { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; }

.card { background: #111827; border: 1px solid #1e293b; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; }
.tag-compra { background: rgba(0,212,170,0.15); color: #00d4aa; border: 1px solid rgba(0,212,170,0.3); padding: 2px 10px; border-radius: 3px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 600; }
.tag-venda { background: rgba(251,113,133,0.15); color: #fb7185; border: 1px solid rgba(251,113,133,0.3); padding: 2px 10px; border-radius: 3px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 600; }
.info-box { background: rgba(0,212,170,0.05); border-left: 3px solid #00d4aa; padding: 0.75rem 1rem; border-radius: 0 6px 6px 0; margin: 0.5rem 0; font-size: 0.85rem; color: #94a3b8; }
.warn-box { background: rgba(251,191,36,0.05); border-left: 3px solid #fbbf24; padding: 0.75rem 1rem; border-radius: 0 6px 6px 0; margin: 0.5rem 0; font-size: 0.85rem; color: #94a3b8; }
.danger-box { background: rgba(251,113,133,0.05); border-left: 3px solid #fb7185; padding: 0.75rem 1rem; border-radius: 0 6px 6px 0; margin: 0.5rem 0; font-size: 0.85rem; color: #94a3b8; }
.market-closed-box { background: rgba(100,116,139,0.08); border: 1px solid #334155; border-radius: 8px; padding: 1rem 1.5rem; margin: 0.5rem 0; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #475569; }

.turn-clock { background: linear-gradient(135deg, #111827 0%, #0d1117 100%); border: 1px solid #1e293b; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1rem; text-align: center; }
.turn-clock .clock-time { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 700; color: #00d4aa; letter-spacing: 0.05em; line-height: 1; }
.turn-clock .clock-date { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }
.turn-clock .clock-turn { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #334155; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 6px; border-top: 1px solid #1e293b; padding-top: 6px; }
.market-status-open { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #00d4aa; font-weight: 700; margin-top: 4px; }
.market-status-closed { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #475569; margin-top: 4px; }

.turn-log-item { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #64748b; padding: 3px 0; border-bottom: 1px solid #0d1117; }
.turn-log-item span.ts { color: #334155; }
.turn-log-item span.ev { color: #94a3b8; }
.turn-log-item span.pos { color: #00d4aa; }
.turn-log-item span.neg { color: #fb7185; }
.turn-log-item span.rfq { color: #a78bfa; }
.turn-log-item span.deal { color: #fbbf24; }
.rfq-card { background: rgba(167,139,250,0.05); border: 1px solid rgba(167,139,250,0.3); border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #a78bfa; }
hr { border-color: #1e293b; }

.perfil-badge { display:inline-block; padding:1px 8px; border-radius:3px; font-family:'JetBrains Mono',monospace; font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; }
.perfil-agressiva    { background:rgba(251,191,36,0.15);  color:#fbbf24; border:1px solid rgba(251,191,36,0.35); }
.perfil-conservadora { background:rgba(96,165,250,0.15);  color:#60a5fa; border:1px solid rgba(96,165,250,0.35); }
.perfil-inadimplente { background:rgba(251,113,133,0.15); color:#fb7185; border:1px solid rgba(251,113,133,0.35); }
.perfil-padrao       { background:rgba(100,116,139,0.10); color:#64748b; border:1px solid rgba(100,116,139,0.25); }
.evento-card  { border-radius:8px; padding:0.75rem 1rem; margin-bottom:0.5rem; font-family:'JetBrains Mono',monospace; }
.evento-danger{ background:rgba(251,113,133,0.07); border:1px solid rgba(251,113,133,0.4); }
.evento-warn  { background:rgba(251,191,36,0.07);  border:1px solid rgba(251,191,36,0.4);  }
.evento-info  { background:rgba(96,165,250,0.07);  border:1px solid rgba(96,165,250,0.4);  }
.margem-bar   { background:#1e293b; border-radius:4px; height:7px; overflow:hidden; margin-top:5px; }
.margem-fill  { height:7px; border-radius:4px; transition:width 0.3s; }
.liquidado-row{ background:rgba(0,212,170,0.04); border:1px solid rgba(0,212,170,0.15); border-radius:5px; padding:5px 10px; margin-bottom:3px; font-family:'JetBrains Mono',monospace; font-size:0.77rem; }
.default-row  { background:rgba(251,113,133,0.04); border:1px solid rgba(251,113,133,0.2); border-radius:5px; padding:5px 10px; margin-bottom:3px; font-family:'JetBrains Mono',monospace; font-size:0.77rem; }
.ponta-badge  { display:inline-block; background:rgba(251,191,36,0.15); color:#fbbf24; border:1px solid rgba(251,191,36,0.4); border-radius:3px; padding:1px 8px; font-family:'JetBrains Mono',monospace; font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ════════════════════════════════════════════════════════════════════════════════
SAVE_FILE          = "energy_trader_save.json"
HOURS_PER_TURN     = 1
METEO_UPDATE_HOURS = 24
PLD_UPDATE_HOURS   = 6        # PLD atualiza a cada 6h de jogo
MARKET_OPEN_HOUR   = 9
MARKET_CLOSE_HOUR  = 18

MESES_ABREV = ["JAN","FEV","MAR","ABR","MAI","JUN","JUL","AGO","SET","OUT","NOV","DEZ"]
MESES_FULL  = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
               "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

SUBM  = {"SE/CO": 1.0, "S": 0.95, "NE": 1.05, "N": 1.10}
TIPOS_ENERGIA = ["Convencional", "Incentivada 50%", "Incentivada 100%"]
INDICES       = ["Preço Fixo", "PLD Spot", "PLD Médio Mensal", "IPCA + Spread", "IGP-M + Spread"]
ORDER_TYPES   = ["Limite", "Mercado (Market)", "IOC (Immediate or Cancel)"]

FATOR_PONTA     = 1.20        # PLD +20% nas horas de ponta (17–18h)
LIMITE_CREDITO  = 10_000_000  # R$ 10M — notional máximo em aberto

EVENTOS_MERCADO = [
    {"id":"seca_ne",    "titulo":"🌵 Seca Severa no Nordeste",
     "desc":"ANA declara alerta hídrico no NE. Reservatórios abaixo de 25%. PLD pressiona alta.",
     "delta_pld":+18, "dur":14, "cor":"danger"},
    {"id":"chuvas_se",  "titulo":"🌧️ Chuvas Acima da Média no SE/CO",
     "desc":"Afluências superam 130% da MLT. Despacho hídrico pleno. PLD cede.",
     "delta_pld":-14, "dur":10, "cor":"info"},
    {"id":"lt_falha",   "titulo":"⚡ Falha em LT 500 kV Norte–Sul",
     "desc":"Linha de transmissão tripou em manutenção não programada. Restrição de intercâmbio.",
     "delta_pld":+22, "dur":7,  "cor":"danger"},
    {"id":"ons_alerta", "titulo":"🚨 ONS Declara Alerta de Escassez",
     "desc":"ONS ativa alerta de escassez energética. Bandeira Vermelha 2 em vigor.",
     "delta_pld":+35, "dur":20, "cor":"danger"},
    {"id":"vento_ne",   "titulo":"💨 Ventos Fortes no Nordeste",
     "desc":"Frente fria eleva geração eólica a 90% da capacidade instalada. PLD alivia.",
     "delta_pld":-10, "dur":6,  "cor":"info"},
    {"id":"ute_pane",   "titulo":"🔥 Pane em Usina Termelétrica",
     "desc":"UTE de 600 MW sai de operação por falha mecânica. Reserva de capacidade reduzida.",
     "delta_pld":+20, "dur":12, "cor":"danger"},
    {"id":"onda_calor", "titulo":"🌡️ Onda de Calor — Demanda Recorde",
     "desc":"Temperatura acima de 38 °C nas capitais. ONS registra novo pico de carga horário.",
     "delta_pld":+25, "dur":9,  "cor":"warn"},
    {"id":"gas_crise",  "titulo":"⛽ Crise de Suprimento de Gás",
     "desc":"Petrobras restringe gás para termelétricas. Despacho termal reduzido.",
     "delta_pld":+30, "dur":16, "cor":"danger"},
    {"id":"cheias_sul", "titulo":"🌊 Cheias no Rio Grande do Sul",
     "desc":"Afluências excepcionais no Sul. Usinas operam plena carga.",
     "delta_pld":-16, "dur":12, "cor":"info"},
    {"id":"importacao", "titulo":"🌐 Importação Emergencial do Uruguai",
     "desc":"Brasil fecha contrato emergencial de importação. Curto prazo aliviado.",
     "delta_pld":-8,  "dur":5,  "cor":"info"},
]

# ── 100+ Contrapartes ──────────────────────────────────────────────────────────
def _build_counterparties():
    """Gera lista de 108 contrapartes simuladas com perfis realistas."""
    cps = []

    # --- Geradores Hidrelétricos (20) ---
    hidro_nomes = [
        "Eletrobras Chesf", "Eletrobras Furnas", "Eletrobras Eletronorte", "Cemig GT",
        "CPFL Geração", "Engie Brasil Hidro", "AES Tietê", "Duke Energy Geração",
        "EDP Geração Hidro", "Neoenergia Hidro", "Enel Geração Hidro", "Copel GeT",
        "Cesp Hidro", "Tractebel Hidro", "Brookfield Energia", "PCH Paraíba",
        "PCH Rio Verde", "PCH Serra Alta", "Hydro BrazGen", "Itaipu Binacional"
    ]
    for n in hidro_nomes:
        cps.append({"nome": n, "tipo": "Vendedora", "produtos_tipo": "longo",
                    "agressividade": round(random.uniform(0.5, 0.85), 2),
                    "descricao": "Gerador hidrelétrico — vende agressivamente em períodos úmidos",
                    "submercados_pref": ["SE/CO","S"], "spread_ref": random.uniform(-0.03, 0.02)})

    # --- Geradores Eólicos (18) ---
    eolico_nomes = [
        "Casa dos Ventos", "Voltalia Brasil", "Neoenergia Eólica", "EDP Eólica NE",
        "Engie Eólica", "CPFL Renováveis Eólica", "Orteng Eólica", "Ômega Energia",
        "Rio Energy", "Elera Renováveis", "Equatorial Geração Eólica", "Cubico Brasil",
        "Brasol Eólica", "Venacast Wind", "Enel Green Power NE", "EDPR Brasil",
        "Vestas Operations", "Siemens Gamesa Energy"
    ]
    for n in eolico_nomes:
        cps.append({"nome": n, "tipo": "Vendedora", "produtos_tipo": "anual",
                    "agressividade": round(random.uniform(0.45, 0.70), 2),
                    "descricao": "Gerador eólico — preço baseado em custo de projeto",
                    "submercados_pref": ["NE","S"], "spread_ref": random.uniform(0.0, 0.04)})

    # --- Geradores Solares (14) ---
    solar_nomes = [
        "Atlas Renewable Solar", "Canadian Solar Brazil", "BYD Energy Brasil",
        "Enel Green Power Solar", "Lightsource bp Brasil", "Elera Solar",
        "Solaria Brasil", "Grenergy Solar", "Statkraft Solar",
        "Eneva Solar", "Omega Solar NE", "Serra Solar Geração",
        "Brasol Solar", "Sungrow Energy Brasil"
    ]
    for n in solar_nomes:
        cps.append({"nome": n, "tipo": "Vendedora", "produtos_tipo": "anual",
                    "agressividade": round(random.uniform(0.40, 0.65), 2),
                    "descricao": "Gerador solar — incentivada 100%, PPA de longo prazo",
                    "submercados_pref": ["NE","SE/CO"], "spread_ref": random.uniform(0.0, 0.05)})

    # --- Geradores Termelétricos (8) ---
    termo_nomes = [
        "Eneva Termelétrica", "Celse GNL Sergipe", "Petrobras Termeletrica",
        "Termomanaus", "TermoNordeste", "UTE Porto do Pecém", "Suape Energética", "GNL Rio"
    ]
    for n in termo_nomes:
        cps.append({"nome": n, "tipo": "Vendedora", "produtos_tipo": "mensal",
                    "agressividade": round(random.uniform(0.55, 0.80), 2),
                    "descricao": "Gerador termelétrico — despacho por ordem de mérito",
                    "submercados_pref": ["SE/CO","NE","N"], "spread_ref": random.uniform(-0.02, 0.03)})

    # --- Comercializadoras (20) ---
    comer_nomes = [
        "Comerc Energia", "Atem Energia", "Tradener", "LiquidPower",
        "Matrix Energia", "Eneva Trading", "Voltalia Trading", "BRL Energy",
        "BIG Trading", "Plural Energia", "Greener Energia", "GreenYellow Trading",
        "Axpo Brasil", "Alpiq Brasil", "EDF Trading Brasil", "Shell Energy Brasil",
        "Trafigura Energy", "Vitol Energy Brasil", "Mercados Energia", "Enertrade"
    ]
    for n in comer_nomes:
        cps.append({"nome": n, "tipo": "Ambos", "produtos_tipo": "todos",
                    "agressividade": round(random.uniform(0.50, 0.75), 2),
                    "descricao": "Comercializadora — compra e vende conforme cenário",
                    "submercados_pref": ["SE/CO","NE","S","N"], "spread_ref": random.uniform(-0.02, 0.02)})

    # --- Consumidores Livres Industriais (20) ---
    indus_nomes = [
        "Vale Energia", "Gerdau Aços", "CSN Mineração", "Usiminas Inox",
        "Votorantim Cimentos", "Suzano Papel", "Fibria Energia", "Klabin Energia",
        "Braskem Petroquímica", "Petrobras Downstream", "Embraer Facilities",
        "Natura Cosméticos", "Ambev Cervejaria", "BRF Foods", "JBS Frigorífico",
        "Marfrig Energia", "Seara Foods", "Perdigão Energia", "Cargill Brasil", "ADM Grains"
    ]
    for n in indus_nomes:
        cps.append({"nome": n, "tipo": "Compradora", "produtos_tipo": "mensal",
                    "agressividade": round(random.uniform(0.35, 0.65), 2),
                    "descricao": "Consumidor industrial livre — compra mensalmente",
                    "submercados_pref": ["SE/CO","S"], "spread_ref": random.uniform(-0.04, 0.0)})

    # --- Distribuidoras (8) ---
    distrib_nomes = [
        "Cemig D", "Copel DIS", "CPFL Paulista", "Elektro",
        "Light Distribuição", "Equatorial Maranhão", "Coelba", "Celpe"
    ]
    for n in distrib_nomes:
        cps.append({"nome": n, "tipo": "Compradora", "produtos_tipo": "mensal",
                    "agressividade": round(random.uniform(0.60, 0.90), 2),
                    "descricao": "Distribuidora — alta urgência no fim do mês",
                    "submercados_pref": ["SE/CO","NE","S"], "spread_ref": random.uniform(-0.02, 0.02)})

    # ── Atribuição de perfis comportamentais ──────────────────────────────────
    _pesos = ["padrao"] * 5 + ["agressiva"] * 2 + ["conservadora"] * 2 + ["inadimplente"] * 1
    _distrib_urgente = ["agressiva", "agressiva", "padrao"]
    _distrib_pequeno = ["inadimplente", "inadimplente", "padrao"]
    for cp in cps:
        if any(k in cp["nome"] for k in ["Cemig D","Copel DIS","CPFL Paulista","Elektro","Light","Equatorial","Coelba","Celpe"]):
            cp["perfil"] = random.choice(_distrib_urgente)
        elif cp["nome"].startswith("PCH"):
            cp["perfil"] = random.choice(_distrib_pequeno)
        else:
            cp["perfil"] = random.choice(_pesos)
    return cps

COUNTERPARTIES = _build_counterparties()

def _cp_produtos(cp: dict, gdt: datetime) -> list:
    """Retorna produtos válidos para uma contraparte com base no tipo."""
    produtos_todos = _gerar_produtos(gdt)
    t = cp.get("produtos_tipo","todos")
    if t == "mensal":
        return [p for p in produtos_todos if p["tipo"] == "M"][:4]
    elif t == "anual":
        return [p for p in produtos_todos if p["tipo"] == "A"][:3]
    elif t == "longo":
        return [p for p in produtos_todos if p["tipo"] in ["Q","A"]][:4]
    else:  # todos
        return produtos_todos[:6]

# ════════════════════════════════════════════════════════════════════════════════
# PRODUTOS DINÂMICOS (nomes dos meses reais)
# ════════════════════════════════════════════════════════════════════════════════
def _gerar_produtos(gdt: datetime) -> list:
    """
    Gera produtos com nome real dos meses a partir da data do jogo.
    Inclui mês atual + 11 meses à frente (mensais), 4 trimestres e 2 anos.
    """
    produtos = []
    base = gdt.date().replace(day=1)

    # Meses: atual + próximos 11
    for i in range(12):
        dt = base + relativedelta(months=i)
        codigo = f"{MESES_ABREV[dt.month-1]}/{str(dt.year)[2:]}"
        label  = f"{MESES_FULL[dt.month-1]} {dt.year}"
        produtos.append({
            "codigo": codigo, "label": label, "tipo": "M",
            "inicio": dt, "fim": (dt + relativedelta(months=1)),
            "meses": 1, "horas_mes": _horas_mes(dt),
            "fator_prazo": 1 + (i * 0.004)
        })

    # Trimestres: Q corrente + Q+1, Q+2, Q+3
    q_base = _inicio_trimestre(base)
    for i in range(4):
        dt_q = q_base + relativedelta(months=3*i)
        dt_q_fim = dt_q + relativedelta(months=3)
        mes_q = dt_q.month
        tri_num = (mes_q - 1) // 3 + 1
        codigo = f"T{tri_num}/{str(dt_q.year)[2:]}"
        label  = f"{tri_num}º Trim. {dt_q.year}"
        horas  = sum(_horas_mes(dt_q + relativedelta(months=k)) for k in range(3))
        produtos.append({
            "codigo": codigo, "label": label, "tipo": "Q",
            "inicio": dt_q, "fim": dt_q_fim,
            "meses": 3, "horas_mes": horas // 3,
            "fator_prazo": 1 + (3*i * 0.004)
        })

    # Anos: ano corrente + próximo
    for i in range(2):
        ano = base.year + i
        dt_a = date(ano, 1, 1)
        horas = sum(_horas_mes(date(ano, m, 1)) for m in range(1, 13))
        produtos.append({
            "codigo": f"ANO/{ano}", "label": f"Ano {ano}", "tipo": "A",
            "inicio": dt_a, "fim": date(ano+1, 1, 1),
            "meses": 12, "horas_mes": horas // 12,
            "fator_prazo": 1 + (12*i * 0.003)
        })

    return produtos

def _horas_mes(dt: date) -> int:
    fim = dt + relativedelta(months=1)
    return int((fim - dt).days * 24)

def _inicio_trimestre(dt: date) -> date:
    q_month = ((dt.month - 1) // 3) * 3 + 1
    return dt.replace(month=q_month, day=1)

def _get_produto_by_codigo(codigo: str, gdt: datetime):
    for p in _gerar_produtos(gdt):
        if p["codigo"] == codigo:
            return p
    return None

# ════════════════════════════════════════════════════════════════════════════════
# HELPERS DE MERCADO
# ════════════════════════════════════════════════════════════════════════════════
def _is_market_open(gdt: datetime) -> bool:
    if gdt.weekday() >= 5:
        return False
    return MARKET_OPEN_HOUR <= gdt.hour < MARKET_CLOSE_HOUR

def _market_status_str(gdt: datetime) -> str:
    if _is_market_open(gdt):
        return f"🟢 ABERTO · Fecha em {MARKET_CLOSE_HOUR - gdt.hour}h"
    elif gdt.weekday() >= 5:
        return "🔴 FECHADO · Fim de semana"
    elif gdt.hour < MARKET_OPEN_HOUR:
        return f"🔴 FECHADO · Abre em {MARKET_OPEN_HOUR - gdt.hour}h"
    else:
        return "🔴 FECHADO · Abre amanhã às 09:00"

def _reference_price(produto: dict, subm: str) -> float:
    """Preço de referência = PLD mensal × fator submercado × fator prazo."""
    pld  = st.session_state['pld_atual']
    fsub = SUBM.get(subm, 1.0)
    fprd = produto.get("fator_prazo", 1.0)
    return round(pld * fsub * fprd, 2)

# ════════════════════════════════════════════════════════════════════════════════
# PERSISTÊNCIA
# ════════════════════════════════════════════════════════════════════════════════
def _serializar_contrato(c):
    d = dict(c)
    for k in ('data_inicio', 'data_fim'):
        if isinstance(d.get(k), date):
            d[k] = d[k].isoformat()
    if isinstance(d.get('criado_em'), datetime):
        d['criado_em'] = d['criado_em'].isoformat()
    return d

def _desserializar_contrato(d):
    d = dict(d)
    for k in ('data_inicio', 'data_fim'):
        if isinstance(d.get(k), str):
            d[k] = date.fromisoformat(d[k])
    if isinstance(d.get('criado_em'), str):
        d['criado_em'] = datetime.fromisoformat(d['criado_em'])
    return d

def salvar_estado():
    df_hist = st.session_state['pld_historico']
    payload = {
        'pld_atual':     st.session_state['pld_atual'],
        'saldo_caixa':   st.session_state['saldo_caixa'],
        'pagina':        st.session_state['pagina'],
        'contratos':     [_serializar_contrato(c) for c in st.session_state['contratos']],
        'pld_historico': {
            'datas': [str(d) for d in df_hist['Data'].tolist()],
            'plds':  df_hist['PLD (R$/MWh)'].tolist(),
        },
        'meteo':          st.session_state.get('meteo', {}),
        'turno':          st.session_state.get('turno', 0),
        'game_datetime':  st.session_state['game_datetime'].isoformat(),
        'turn_log':       st.session_state.get('turn_log', []),
        'order_book':     st.session_state.get('order_book', {}),
        'pending_rfqs':   st.session_state.get('pending_rfqs', []),
        'eventos_ativos': st.session_state.get('eventos_ativos', []),
        'liquidacoes':    st.session_state.get('liquidacoes', []),
        'limite_credito': st.session_state.get('limite_credito', LIMITE_CREDITO),
    }
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def carregar_estado():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def resetar_estado():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# ════════════════════════════════════════════════════════════════════════════════
# METEOROLOGIA
# ════════════════════════════════════════════════════════════════════════════════
def _gerar_meteo_inicial():
    base_date = date.today().replace(day=1)
    datas = [base_date - relativedelta(months=i) for i in range(23, -1, -1)]
    res_seco, nivel = [], 65.0
    for d in datas:
        mes = d.month
        tend = 3.0 if mes in [12,1,2,3] else -2.5 if mes in [6,7,8,9] else 0.5
        nivel = max(5, min(100, nivel + tend + random.gauss(0, 4)))
        res_seco.append(round(nivel, 1))
    afluen, precip, temp, eolica, solar = [], [], [], [], []
    for d in datas:
        mes = d.month
        afluen.append(round(max(10, (130 if mes in [12,1,2,3] else 60 if mes in [6,7,8,9] else 95) + random.gauss(0, 20)), 1))
        precip.append(round(max(0,  (220 if mes in [12,1,2,3] else 30 if mes in [6,7,8] else 100) + random.gauss(0, 30)), 1))
        temp.append(round((28 if mes in [12,1,2] else 22 if mes in [6,7,8] else 25) + random.gauss(0, 1.5), 1))
        eolica.append(round(max(5,  min(100, (70 if mes in [7,8,9,10] else 35 if mes in [1,2,3] else 50) + random.gauss(0, 8))), 1))
        solar.append(round(max(10, min(100,  (75 if mes in [11,12,1,2] else 55 if mes in [6,7] else 65) + random.gauss(0, 6))), 1))
    return {
        'datas': [str(d) for d in datas],
        'reserv': res_seco, 'afluen': afluen,
        'precip': precip,   'temp': temp,
        'eolica': eolica,   'solar': solar,
    }

def _atualizar_meteo(game_dt: datetime):
    m = st.session_state['meteo']
    mes = game_dt.month
    res  = m['reserv'][-1]; aflu = m['afluen'][-1]
    prec = m['precip'][-1]; temp = m['temp'][-1]
    eol  = m['eolica'][-1]; sol  = m['solar'][-1]
    tend_r = 3.0 if mes in [12,1,2,3] else -2.5 if mes in [6,7,8,9] else 0.5
    m['datas'].append(str(game_dt.date()))
    m['reserv'].append(round(max(5,  min(100, res  + tend_r + random.gauss(0, 1.5))), 1))
    m['afluen'].append(round(max(10, min(200, aflu + random.gauss(0, 5))), 1))
    m['precip'].append(round(max(0,          prec + random.gauss(0, 8)), 1))
    m['temp'].append(round(               temp + random.gauss(0, 0.3),  1))
    m['eolica'].append(round(max(5,  min(100, eol  + random.gauss(0, 2.5))), 1))
    m['solar'].append(round(max(10, min(100, sol  + random.gauss(0, 2))), 1))
    st.session_state['meteo'] = m

def _impacto_meteo_no_pld(meteo):
    fator, alertas = 1.0, []
    res = meteo['reserv'][-1]; aflu = meteo['afluen'][-1]
    eol = meteo['eolica'][-1]; temp = meteo['temp'][-1]
    if res < 20:
        fator += 0.35; alertas.append(("🚨","danger",f"Reservatório crítico ({res:.0f}%) — pressão muito alta sobre o PLD"))
    elif res < 40:
        fator += 0.15; alertas.append(("⚠️","warn",f"Reservatório baixo ({res:.0f}%) — risco de elevação do PLD"))
    elif res > 75:
        fator -= 0.10; alertas.append(("✅","info",f"Reservatório cheio ({res:.0f}%) — pressão de baixa no PLD"))
    if aflu < 50:
        fator += 0.20; alertas.append(("⚠️","warn",f"Afluência muito abaixo da MLT ({aflu:.0f}%) — risco hídrico elevado"))
    elif aflu > 120:
        fator -= 0.08; alertas.append(("✅","info",f"Afluência acima da MLT ({aflu:.0f}%) — boas condições hídricas"))
    if eol > 65:
        fator -= 0.06; alertas.append(("✅","info",f"Geração eólica forte ({eol:.0f}%) — contribui para redução do PLD"))
    elif eol < 25:
        fator += 0.05; alertas.append(("⚠️","warn",f"Geração eólica fraca ({eol:.0f}%) — menor alívio sobre o sistema"))
    if temp > 30:
        fator += 0.08; alertas.append(("⚠️","warn",f"Temperatura elevada ({temp:.1f}°C) — maior demanda de resfriamento"))
    elif temp < 18:
        fator -= 0.03; alertas.append(("✅","info",f"Temperatura amena ({temp:.1f}°C) — menor pressão sobre a demanda"))
    return round(fator, 3), alertas

# ────────────────────────────────────────────────────────────────────────────────
# Sazonalidade e hora de ponta
# ────────────────────────────────────────────────────────────────────────────────
def _fator_sazonalidade(gdt: datetime) -> float:
    mes = gdt.month
    if mes in [12, 1, 2, 3]:  return 0.90   # período úmido → PLD tende baixo
    if mes in [6, 7, 8, 9]:   return 1.12   # período seco  → PLD tende alto
    return 1.0

def _is_hora_ponta(gdt: datetime) -> bool:
    return gdt.weekday() < 5 and gdt.hour in [17, 18]

def _label_sazonalidade(gdt: datetime) -> str:
    mes = gdt.month
    if mes in [12, 1, 2, 3]: return "Período Úmido", "#60a5fa"
    if mes in [6, 7, 8, 9]:  return "Período Seco",  "#fb7185"
    return "Transição", "#fbbf24"

# ────────────────────────────────────────────────────────────────────────────────
# Eventos de mercado
# ────────────────────────────────────────────────────────────────────────────────
def _gerar_evento_mercado(gdt: datetime, turno: int):
    ativos = st.session_state.get('eventos_ativos', [])
    if ativos:
        return None
    if random.random() > 0.05:
        return None
    evt = dict(random.choice(EVENTOS_MERCADO))
    evt['expira_turno'] = turno + evt['dur']
    evt['aplicado_em']  = gdt.strftime('%d/%m %H:%M')
    return evt

# ────────────────────────────────────────────────────────────────────────────────
# Liquidação de contratos vencidos
# ────────────────────────────────────────────────────────────────────────────────
def _verificar_vencimentos(new_dt: datetime) -> list:
    eventos  = []
    saldo    = st.session_state.get('saldo_caixa', 0.0)
    liq_hist = st.session_state.get('liquidacoes', [])
    for c in st.session_state['contratos']:
        if c.get('status') in ('liquidado', 'inadimplido'):
            continue
        data_fim = c.get('data_fim')
        if not isinstance(data_fim, date):
            continue
        if new_dt.date() < data_fim:
            continue
        _recalc_pnl(c)
        pnl = c.get('pnl_atual', 0.0)
        cp_nome = c.get('contraparte', '')
        cp_obj  = next((x for x in COUNTERPARTIES if x['nome'] == cp_nome), None)
        if cp_obj and cp_obj.get('perfil') == 'inadimplente' and random.random() < 0.25:
            recuperado = round(pnl * 0.40, 2)
            saldo += recuperado
            c['status']        = 'inadimplido'
            c['pnl_realizado'] = recuperado
            liq_hist.append({'nome': c['nome'], 'contraparte': cp_nome,
                             'pnl_realizado': recuperado, 'status': 'inadimplido',
                             'data': new_dt.strftime('%d/%m/%Y')})
            eventos.append(f'<span class="neg">💀 INADIMPLÊNCIA — {c["nome"]} c/ {cp_nome}: recuperação 40% = {_fmt_brl(recuperado)}</span>')
        else:
            saldo += pnl
            c['status']        = 'liquidado'
            c['pnl_realizado'] = pnl
            liq_hist.append({'nome': c['nome'], 'contraparte': cp_nome,
                             'pnl_realizado': pnl, 'status': 'liquidado',
                             'data': new_dt.strftime('%d/%m/%Y')})
            sinal = "pos" if pnl >= 0 else "neg"
            eventos.append(f'<span class="ev">📦 Liquidação </span><span class="deal">{c["nome"]}</span>'
                           f' <span class="{sinal}">{_fmt_brl(pnl)}</span>')
    st.session_state['saldo_caixa'] = round(saldo, 2)
    st.session_state['liquidacoes'] = liq_hist[-50:]
    return eventos

# ────────────────────────────────────────────────────────────────────────────────
# Margem / limite de crédito
# ────────────────────────────────────────────────────────────────────────────────
def _notional_aberto() -> float:
    return sum(
        c.get('volume_mwm', 1) * c.get('horas', 720) * c.get('preco', 0)
        for c in st.session_state['contratos']
        if c.get('status') not in ('liquidado', 'inadimplido')
    )

def _margem_pct() -> float:
    lim = st.session_state.get('limite_credito', LIMITE_CREDITO)
    return min(1.0, _notional_aberto() / lim) if lim > 0 else 0.0

def _pode_negociar(volume_mwm: float, horas: int, preco: float):
    novo_notional   = volume_mwm * horas * preco
    total_notional  = _notional_aberto() + novo_notional
    lim = st.session_state.get('limite_credito', LIMITE_CREDITO)
    if total_notional > lim:
        return False, f"Limite de crédito atingido (R$ {lim/1e6:.1f}M). Liquidez insuficiente."
    return True, ""

# ════════════════════════════════════════════════════════════════════════════════
# LIVRO DE ORDENS
# ════════════════════════════════════════════════════════════════════════════════
def _init_order_book():
    """Inicializa o livro com os produtos dos próximos 3 meses + trimestres + anos."""
    book = {}
    gdt  = st.session_state['game_datetime']
    for prod in _gerar_produtos(gdt)[:10]:  # primeiros 10 produtos
        codigo = prod["codigo"]
        book[codigo] = {"bids": [], "asks": []}
        ref = _reference_price(prod, "SE/CO")
        for i in range(1, 5):
            spread_pct = 0.005 + i * 0.004
            bid_price  = round(ref * (1 - spread_pct * i), 2)
            ask_price  = round(ref * (1 + spread_pct * i), 2)
            vol = round(random.uniform(3, 25), 1)
            cp  = random.choice(COUNTERPARTIES)
            book[codigo]["bids"].append({"preco": bid_price, "volume_mwm": vol, "contraparte": cp["nome"]})
            book[codigo]["asks"].append({"preco": ask_price, "volume_mwm": vol, "contraparte": cp["nome"]})
        book[codigo]["bids"].sort(key=lambda x: -x["preco"])
        book[codigo]["asks"].sort(key=lambda x:  x["preco"])
    return book

def _atualizar_order_book():
    book = st.session_state.get('order_book', {})
    gdt  = st.session_state['game_datetime']
    fator_meteo, _ = _impacto_meteo_no_pld(st.session_state['meteo'])
    for prod in _gerar_produtos(gdt)[:10]:
        codigo = prod["codigo"]
        if codigo not in book:
            book[codigo] = {"bids": [], "asks": []}
        ref = _reference_price(prod, "SE/CO")
        for lado in ["bids", "asks"]:
            niveis = book[codigo][lado]
            if not niveis:
                continue
            for ordem in niveis:
                ruido   = random.gauss(0, ref * 0.005)
                pressao = (ref * fator_meteo - ordem["preco"]) * 0.03
                ordem["preco"]     = round(max(30, min(600, ordem["preco"] + ruido + pressao)), 2)
                ordem["volume_mwm"] = round(max(1, ordem["volume_mwm"] + random.gauss(0, 1)), 1)
        book[codigo]["bids"].sort(key=lambda x: -x["preco"])
        book[codigo]["asks"].sort(key=lambda x:  x["preco"])
    st.session_state['order_book'] = book

def _gerar_rfq_aleatorio(gdt: datetime):
    if not _is_market_open(gdt):
        return None
    if random.random() > 0.30:
        return None
    cp       = random.choice(COUNTERPARTIES)
    produtos = _cp_produtos(cp, gdt)
    if not produtos:
        return None
    prod = random.choice(produtos)
    tipo = "Venda" if cp["tipo"] == "Vendedora" else \
           "Compra" if cp["tipo"] == "Compradora" else \
           random.choice(["Compra","Venda"])
    ref    = _reference_price(prod, "SE/CO")
    desvio = random.uniform(-0.04, 0.04) + cp.get("spread_ref", 0)
    preco  = round(ref * (1 + desvio), 2)
    vol    = round(random.uniform(2, 30), 1)  # MW médio
    return {
        "id":          random.randint(10000, 99999),
        "contraparte": cp["nome"],
        "tipo":        tipo,
        "produto_cod": prod["codigo"],
        "produto_lab": prod["label"],
        "submercado":  random.choice(cp.get("submercados_pref", ["SE/CO"])),
        "preco":       preco,
        "volume_mwm":  vol,          # MW médio mensal
        "referencia":  ref,
        "desvio_pct":  round(desvio * 100, 1),
        "timestamp":   gdt.strftime("%d/%m %H:%M"),
        "status":      "pendente",
        "expira_turno": st.session_state.get('turno', 0) + random.randint(3, 10),
    }

def _prob_aceitar(preco_oferta, preco_ref, fator_meteo, tipo_ordem, cp):
    if tipo_ordem == "Compra":
        delta_p = (preco_oferta - preco_ref) / max(preco_ref, 1)
    else:
        delta_p = (preco_ref - preco_oferta) / max(preco_ref, 1)
    urgencia = 1 if random.random() < cp.get("agressividade", 0.5) else 0
    z = 15.0 * delta_p + 0.3 * (fator_meteo - 1.0) + 0.2 * urgencia
    perfil = cp.get('perfil', 'padrao')
    if perfil == 'agressiva':    z += 0.6
    if perfil == 'conservadora': z -= 1.0
    if perfil == 'inadimplente': z += 0.4   # aceita mais fácil, não se importa em honrar depois
    return round(1 / (1 + math.exp(-z)), 3)

def _executar_ordem_mercado(tipo, produto_cod, volume_mwm, subm, gdt):
    book = st.session_state.get('order_book', {})
    if produto_cod not in book:
        return None, "Produto não encontrado no livro."
    lado   = "asks" if tipo == "Compra" else "bids"
    niveis = book[produto_cod][lado]
    if not niveis:
        return None, "Sem liquidez no lado solicitado."
    melhor    = niveis[0]
    # Ajusta preço pelo submercado
    fator_sub = SUBM.get(subm, 1.0)
    preco_exec = round(melhor["preco"] * fator_sub, 2)
    vol_exec   = min(volume_mwm, melhor["volume_mwm"])
    melhor["volume_mwm"] = round(melhor["volume_mwm"] - vol_exec, 1)
    if melhor["volume_mwm"] <= 0:
        niveis.pop(0)
    st.session_state['order_book'] = book
    return {
        "preco":       preco_exec,
        "volume_mwm":  vol_exec,
        "contraparte": melhor["contraparte"],
        "parcial":     vol_exec < volume_mwm,
    }, None

# ════════════════════════════════════════════════════════════════════════════════
# MOTOR DE TURNOS
# ════════════════════════════════════════════════════════════════════════════════
def _avancar_turno():
    old_dt: datetime = st.session_state['game_datetime']
    new_dt = old_dt + timedelta(hours=HOURS_PER_TURN)
    st.session_state['game_datetime'] = new_dt
    st.session_state['turno'] += 1
    turno = st.session_state['turno']
    eventos = []

    # ── PLD mensal update ──────────────────────────────────────────────────────
    if turno % PLD_UPDATE_HOURS == 0:
        fator_meteo, _ = _impacto_meteo_no_pld(st.session_state['meteo'])
        ruido    = random.gauss(0, 8)
        pld_med  = st.session_state['pld_historico']['PLD (R$/MWh)'].mean()
        f_saz    = _fator_sazonalidade(new_dt)
        pressao  = (pld_med * fator_meteo * f_saz - st.session_state['pld_atual']) * 0.06
        novo_pld = max(30, min(500, st.session_state['pld_atual'] + ruido + pressao))
        delta    = novo_pld - st.session_state['pld_atual']
        st.session_state['pld_atual'] = round(novo_pld, 2)
        nova_linha = pd.DataFrame({'Data': [new_dt.date()], 'PLD (R$/MWh)': [round(novo_pld, 2)]})
        st.session_state['pld_historico'] = pd.concat(
            [st.session_state['pld_historico'], nova_linha], ignore_index=True
        )
        sinal = "pos" if delta >= 0 else "neg"
        eventos.append(f'<span class="ev">PLD atualizado →</span> <span class="{sinal}">R$ {novo_pld:.2f} ({delta:+.2f})</span>')
        _atualizar_order_book()
        rfq = _gerar_rfq_aleatorio(new_dt)
        if rfq:
            pending = st.session_state.get('pending_rfqs', [])
            pending.append(rfq)
            st.session_state['pending_rfqs'] = pending
            eventos.append(f'<span class="rfq">📨 RFQ de {rfq["contraparte"]} — {rfq["tipo"]} {rfq["produto_cod"]} R${rfq["preco"]:.2f} · {rfq["volume_mwm"]:.1f} MWm</span>')

    # ── Pressão de hora de ponta ───────────────────────────────────────────────
    if _is_hora_ponta(new_dt):
        spike = round(random.uniform(2.5, 7.0), 2)
        st.session_state['pld_atual'] = round(min(500, st.session_state['pld_atual'] + spike), 2)
        eventos.append(f'<span class="ev">⚡ Hora de ponta</span> <span class="pos">+R$ {spike:.2f} pressão PLD</span>')

    # ── Eventos de mercado ─────────────────────────────────────────────────────
    ativos = [e for e in st.session_state.get('eventos_ativos', []) if e['expira_turno'] > turno]
    if _is_market_open(new_dt):
        novo_evt = _gerar_evento_mercado(new_dt, turno)
        if novo_evt:
            st.session_state['pld_atual'] = round(
                max(30, min(500, st.session_state['pld_atual'] + novo_evt['delta_pld'])), 2)
            ativos.append(novo_evt)
            sinal_evt = "pos" if novo_evt['delta_pld'] < 0 else "neg"
            eventos.append(f'<span class="rfq">📰 EVENTO: {novo_evt["titulo"]}</span>'
                           f' <span class="{sinal_evt}">PLD {novo_evt["delta_pld"]:+}R$</span>')
    st.session_state['eventos_ativos'] = ativos

    # ── Meteo update ──────────────────────────────────────────────────────────
    if turno % METEO_UPDATE_HOURS == 0:
        _atualizar_meteo(new_dt)
        res = st.session_state['meteo']['reserv'][-1]
        eventos.append(f'<span class="ev">Meteo atualizado · Reserv.</span> <span class="{"neg" if res < 40 else "pos"}">{res:.0f}%</span>')

    # ── Liquidação de contratos vencidos ──────────────────────────────────────
    ev_liq = _verificar_vencimentos(new_dt)
    eventos.extend(ev_liq)

    # ── Expirar RFQs ──────────────────────────────────────────────────────────
    pending = st.session_state.get('pending_rfqs', [])
    n_antes = len(pending)
    pending = [r for r in pending if r['expira_turno'] > turno and r['status'] == 'pendente']
    if len(pending) < n_antes:
        eventos.append('<span class="ev">RFQs expirados removidos</span>')
    st.session_state['pending_rfqs'] = pending

    # ── Avisos de abertura/fechamento ─────────────────────────────────────────
    if new_dt.hour == MARKET_CLOSE_HOUR:
        eventos.append('<span class="ev">🔔 Mercado fechou às 18:00</span>')
    if new_dt.hour == MARKET_OPEN_HOUR and new_dt.weekday() < 5:
        eventos.append('<span class="ev">🔔 Mercado abriu às 09:00</span>')

    # ── PnL ───────────────────────────────────────────────────────────────────
    for c in st.session_state['contratos']:
        _recalc_pnl(c)

    # ── Log ───────────────────────────────────────────────────────────────────
    log    = st.session_state.get('turn_log', [])
    ts_str = new_dt.strftime('%d/%m %H:%M')
    mkt    = "🟢" if _is_market_open(new_dt) else "🔴"
    if eventos:
        for ev in eventos:
            log.append(f'<span class="ts">[{ts_str}] {mkt}</span> {ev}')
    else:
        log.append(f'<span class="ts">[{ts_str}] {mkt}</span> <span class="ev">Turno {turno} — mercado estável</span>')
    st.session_state['turn_log'] = log[-50:]
    salvar_estado()

def _proxima_abertura(gdt: datetime) -> datetime:
    """Retorna o datetime de 09:00 do próximo dia útil (ou hoje se ainda não abriu)."""
    # Se ainda não chegou às 09h de um dia útil, abre hoje mesmo
    if gdt.weekday() < 5 and gdt.hour < MARKET_OPEN_HOUR:
        return gdt.replace(hour=MARKET_OPEN_HOUR, minute=0, second=0, microsecond=0)
    # Caso contrário avança para o próximo dia útil
    candidato = gdt.replace(hour=MARKET_OPEN_HOUR, minute=0, second=0, microsecond=0) + timedelta(days=1)
    while candidato.weekday() >= 5:
        candidato += timedelta(days=1)
    return candidato

def _avancar_ate_abertura():
    """Avança o jogo em bloco até 09:00 do próximo dia útil, processando cada turno."""
    alvo = _proxima_abertura(st.session_state['game_datetime'])
    while st.session_state['game_datetime'] < alvo:
        _avancar_turno()

# ════════════════════════════════════════════════════════════════════════════════
# ESTADO INICIAL
# ════════════════════════════════════════════════════════════════════════════════
if 'estado_carregado' not in st.session_state:
    salvo = carregar_estado()
    if salvo:
        datas = [date.fromisoformat(d) for d in salvo['pld_historico']['datas']]
        st.session_state['pld_historico'] = pd.DataFrame({'Data': datas, 'PLD (R$/MWh)': salvo['pld_historico']['plds']})
        st.session_state['pld_atual']    = salvo['pld_atual']
        st.session_state['saldo_caixa']  = salvo['saldo_caixa']
        st.session_state['pagina']       = salvo.get('pagina', 'mercado')
        st.session_state['contratos']    = [_desserializar_contrato(c) for c in salvo['contratos']]
        st.session_state['meteo']        = salvo.get('meteo') or _gerar_meteo_inicial()
        st.session_state['turno']        = salvo.get('turno', 0)
        st.session_state['turn_log']     = salvo.get('turn_log', [])
        st.session_state['pending_rfqs']  = salvo.get('pending_rfqs', [])
        st.session_state['eventos_ativos']= salvo.get('eventos_ativos', [])
        st.session_state['liquidacoes']   = salvo.get('liquidacoes', [])
        st.session_state['limite_credito']= salvo.get('limite_credito', LIMITE_CREDITO)
        gdt = salvo.get('game_datetime')
        st.session_state['game_datetime'] = datetime.fromisoformat(gdt) if gdt else datetime.now().replace(minute=0, second=0, microsecond=0)
        ob = salvo.get('order_book')
        st.session_state['order_book'] = ob if ob else {}
    else:
        st.session_state['contratos']     = []
        st.session_state['saldo_caixa']   = 0.0
        st.session_state['pagina']        = 'mercado'
        st.session_state['turno']         = 0
        st.session_state['turn_log']      = []
        st.session_state['pending_rfqs']  = []
        st.session_state['eventos_ativos']= []
        st.session_state['liquidacoes']   = []
        st.session_state['limite_credito']= LIMITE_CREDITO
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        days_to_monday = (7 - now.weekday()) % 7
        start = (now + timedelta(days=days_to_monday)).replace(hour=9)
        st.session_state['game_datetime'] = start
        base_date = date.today().replace(day=1)
        datas = [base_date - relativedelta(months=i) for i in range(23, -1, -1)]
        plds, pld_v = [], 80.0
        for _ in datas:
            pld_v = max(30, min(500, pld_v + random.gauss(0, 15)))
            plds.append(round(pld_v, 2))
        st.session_state['pld_historico'] = pd.DataFrame({'Data': datas, 'PLD (R$/MWh)': plds})
        st.session_state['pld_atual']     = st.session_state['pld_historico']['PLD (R$/MWh)'].iloc[-1]
        st.session_state['meteo']         = _gerar_meteo_inicial()
        st.session_state['order_book']    = {}
    st.session_state['estado_carregado'] = True
    # Garante livro inicializado
    if not st.session_state.get('order_book'):
        st.session_state['order_book'] = _init_order_book()

# ════════════════════════════════════════════════════════════════════════════════
# HELPERS GERAIS
# ════════════════════════════════════════════════════════════════════════════════
def _recalc_pnl(c):
    """PnL em R$ = (PLD - Preço) × volume_mwm × horas_mes."""
    pld  = st.session_state['pld_atual']
    horas = c.get('horas', 720)
    vol   = c.get('volume_mwm', c.get('volume_mw', 1))  # backward compat
    if c['tipo'] == 'Compra':
        c['pnl_atual'] = (pld - c['preco']) * vol * horas
    else:
        c['pnl_atual'] = (c['preco'] - pld) * vol * horas

def _cor_pnl(v):   return "#00d4aa" if v >= 0 else "#fb7185"
def _fmt_brl(v):   return f"{'+'if v>=0 else ''}R$ {v:,.2f}"
def _fmt_mwm(v):   return f"{v:.1f} MWm"

def _registrar_contrato_negociado(tipo, preco, volume_mwm, produto, subm, contraparte, gdt):
    horas = produto.get("horas_mes", 720)
    novo = {
        'id':          len(st.session_state['contratos']) + 1,
        'nome':        f"{tipo[:1]}{produto['codigo']}-{contraparte[:10]}",
        'contraparte': contraparte,
        'tipo':        tipo,
        'submercado':  subm,
        'tipo_energia':'Convencional',
        'preco':       preco,
        'volume_mwm':  volume_mwm,   # MW médio mensal
        'indice':      'Preço Fixo',
        'data_inicio': produto['inicio'],
        'data_fim':    produto['fim'],
        'horas':       horas,
        'gross_up':    False,
        'flag_pc':     False,
        'obs':         f'Via livro · {produto["label"]} · {subm}',
        'pnl_atual':   0.0,
        'criado_em':   datetime.now(),
        'produto_cod': produto['codigo'],
        'produto_lab': produto['label'],
    }
    _recalc_pnl(novo)
    st.session_state['contratos'].append(novo)
    salvar_estado()
    return novo

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 0.75rem;'>
        <div style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:#00d4aa;letter-spacing:-0.02em;'>⚡ EnergyTrader</div>
        <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-top:2px;'>Simulador · Mercado Livre v4</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    gdt    = st.session_state['game_datetime']
    turno  = st.session_state['turno']
    DIAS_PT  = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]
    MESES_PT = ["","Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    mkt_open  = _is_market_open(gdt)
    mkt_class = "market-status-open" if mkt_open else "market-status-closed"

    st.markdown(f"""
    <div class='turn-clock'>
        <div class='clock-time'>{gdt.strftime('%H:%M')}</div>
        <div class='clock-date'>{DIAS_PT[gdt.weekday()]}, {gdt.day} {MESES_PT[gdt.month]} {gdt.year}</div>
        <div class='{mkt_class}'>{_market_status_str(gdt)}</div>
        <div class='clock-turn'>Turno #{turno} · +1h/avanço · PLD mensal</div>
    </div>""", unsafe_allow_html=True)

    if st.button("⏩  AVANÇAR TURNO  (+1h)", use_container_width=True, type="primary"):
        _avancar_turno(); st.rerun()

    if not _is_market_open(gdt):
        prox = _proxima_abertura(gdt)
        horas_ate = int((prox - gdt).total_seconds() // 3600)
        lbl = f"⏭  ATÉ ABERTURA  (+{horas_ate}h)" if horas_ate > 0 else "⏭  ATÉ ABERTURA"
        if st.button(lbl, use_container_width=True):
            _avancar_ate_abertura(); st.rerun()

    rfqs_pend = [r for r in st.session_state.get('pending_rfqs',[]) if r['status']=='pendente']
    if rfqs_pend:
        st.markdown(f"""<div style='background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.3);
                    border-radius:6px;padding:0.5rem 0.75rem;margin-bottom:0.5rem;
                    font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#a78bfa;'>
            📨 {len(rfqs_pend)} RFQ(s) aguardando</div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Evento ativo ──────────────────────────────────────────────────────────
    evts = st.session_state.get('eventos_ativos', [])
    if evts:
        e = evts[0]
        cor_cls = e.get('cor', 'info')
        st.markdown(f"<div class='evento-card evento-{cor_cls}' style='font-size:0.72rem;'>"
                    f"<b style='font-size:0.68rem;text-transform:uppercase;letter-spacing:0.05em;'>{e['titulo']}</b><br>"
                    f"<span style='color:#64748b;font-size:0.65rem;'>{e['desc']}</span></div>",
                    unsafe_allow_html=True)

    pld = st.session_state['pld_atual']
    ponta_str = " · <span class='ponta-badge'>PONTA</span>" if _is_hora_ponta(gdt) else ""
    saz_lbl, saz_cor = _label_sazonalidade(gdt)
    st.markdown(f"""<div style='background:#111827;border:1px solid #1e293b;border-radius:6px;padding:0.75rem 1rem;margin-bottom:0.75rem;'>
        <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>PLD Mensal (SE/CO){ponta_str}</div>
        <div style='font-family:JetBrains Mono,monospace;font-size:1.4rem;font-weight:700;color:#00d4aa;margin-top:4px;'>R$ {pld:.2f}</div>
        <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;'>R$/MWh · <span style='color:{saz_cor};'>{saz_lbl}</span> · atualiza cada {PLD_UPDATE_HOURS}h</div>
    </div>""", unsafe_allow_html=True)

    # ── Barra de margem/crédito ───────────────────────────────────────────────
    marg  = _margem_pct()
    lim   = st.session_state.get('limite_credito', LIMITE_CREDITO)
    cor_m = "#00d4aa" if marg < 0.60 else "#fbbf24" if marg < 0.85 else "#fb7185"
    st.markdown(f"""<div style='background:#111827;border:1px solid #1e293b;border-radius:6px;padding:0.6rem 0.85rem;margin-bottom:0.75rem;'>
        <div style='display:flex;justify-content:space-between;font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>
            <span>Crédito Utilizado</span><span style='color:{cor_m};'>{marg:.0%}</span></div>
        <div class='margem-bar'><div class='margem-fill' style='width:{marg*100:.1f}%;background:{cor_m};'></div></div>
        <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#334155;margin-top:4px;'>
            Notional: R$ {_notional_aberto()/1e6:.2f}M / Limite R$ {lim/1e6:.1f}M</div>
    </div>""", unsafe_allow_html=True)

    n_c      = len(st.session_state['contratos'])
    pnl_tot  = sum(c.get('pnl_atual',0) for c in st.session_state['contratos'])
    st.markdown(f"""<div style='display:flex;gap:8px;margin-bottom:0.75rem;'>
        <div style='flex:1;background:#111827;border:1px solid #1e293b;border-radius:6px;padding:0.6rem 0.75rem;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.55rem;color:#475569;text-transform:uppercase;'>Contratos</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.1rem;font-weight:700;color:#e2e8f0;'>{n_c}</div>
        </div>
        <div style='flex:1;background:#111827;border:1px solid #1e293b;border-radius:6px;padding:0.6rem 0.75rem;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.55rem;color:#475569;text-transform:uppercase;'>PnL Total</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.1rem;font-weight:700;color:{"#00d4aa" if pnl_tot>=0 else "#fb7185"}'>
                {"+" if pnl_tot>=0 else ""}R${pnl_tot/1000:.1f}k</div>
        </div></div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    def nav(label, key):
        ativo = st.session_state['pagina'] == key
        style = "color:#00d4aa;font-weight:700;" if ativo else ""
        st.markdown(f"<div style='{style}'>", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state['pagina'] = key; salvar_estado(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    nav("📊  Painel de Mercado",  "mercado")
    nav("📒  Livro de Negócios",  "livro")
    nav("📨  RFQs",               "rfqs")
    nav("🌦️  Meteorologia",       "meteo")
    nav("📋  Novo Contrato",      "novo_contrato")
    nav("💼  Meu Portfólio",      "portfolio")
    nav("💰  PnL & Resultado",    "pnl")
    nav("📜  Log de Turnos",      "log")
    nav("🏢  Contrapartes",       "contrapartes")
    nav("📚  Glossário",          "glossario")

    st.markdown("<hr>", unsafe_allow_html=True)
    col_s, col_r = st.columns(2)
    with col_s:
        if st.button("💾 Salvar", use_container_width=True):
            salvar_estado(); st.toast("✅ Salvo!", icon="💾")
    with col_r:
        if st.button("🗑️ Resetar", use_container_width=True):
            st.session_state['confirmar_reset'] = True
    if st.session_state.get('confirmar_reset'):
        st.markdown("<div class='danger-box'>Apaga todos os dados?</div>", unsafe_allow_html=True)
        cs, cn = st.columns(2)
        with cs:
            if st.button("Sim", key="rs_sim", use_container_width=True):
                resetar_estado(); st.rerun()
        with cn:
            if st.button("Não", key="rs_nao", use_container_width=True):
                st.session_state['confirmar_reset'] = False; st.rerun()

pagina = st.session_state['pagina']

# ════════════════════════════════════════════════════════════════════════════════
# PAINEL DE MERCADO
# ════════════════════════════════════════════════════════════════════════════════
if pagina == 'mercado':
    gdt = st.session_state['game_datetime']
    st.markdown("# 📊 Painel de Mercado")
    st.markdown(f"<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>Data do jogo: <b style='color:#00d4aa'>{gdt.strftime('%d/%m/%Y %H:%M')}</b> · Turno #{turno} · {_market_status_str(gdt)}</p>", unsafe_allow_html=True)
    st.markdown("---")

    pld      = st.session_state['pld_atual']
    df_hist  = st.session_state['pld_historico']
    var_pld  = pld - df_hist['PLD (R$/MWh)'].iloc[-2] if len(df_hist) > 1 else 0
    fator_meteo, alertas = _impacto_meteo_no_pld(st.session_state['meteo'])

    # Eventos ativos de mercado
    for evt in st.session_state.get('eventos_ativos', []):
        cor_cls = evt.get('cor', 'info')
        turnos_rest = evt['expira_turno'] - turno
        st.markdown(f"<div class='evento-card evento-{cor_cls}'>"
                    f"<b>{evt['titulo']}</b> &nbsp;<span style='color:#475569;font-size:0.72rem;'>expira em {turnos_rest} turno(s)</span><br>"
                    f"<span style='font-size:0.8rem;color:#94a3b8;'>{evt['desc']}</span></div>",
                    unsafe_allow_html=True)
    # Indicadores de sazonalidade e hora de ponta
    saz_lbl, saz_cor = _label_sazonalidade(gdt)
    ponta_info = " · <span class='ponta-badge'>⚡ HORA DE PONTA</span>" if _is_hora_ponta(gdt) else ""
    st.markdown(f"<div class='info-box' style='margin-bottom:0.5rem;'>📅 <b style='color:{saz_cor};'>{saz_lbl}</b> — fator {_fator_sazonalidade(gdt):.2f}× sobre a média de longo prazo{ponta_info}</div>",
                unsafe_allow_html=True)
    for icone, tipo, msg in alertas[:3]:
        box_class = "danger-box" if tipo=="danger" else "warn-box" if tipo=="warn" else "info-box"
        st.markdown(f"<div class='{box_class}'>{icone} {msg}</div>", unsafe_allow_html=True)
    if not _is_market_open(gdt):
        st.markdown(f"<div class='market-closed-box'>🔴 {_market_status_str(gdt)} — Ordens executadas entre 09:00 e 18:00</div>", unsafe_allow_html=True)

        # ── Painel noturno ────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🌙 Central de Análise — Mercado Fechado")
        st.markdown("<p style='color:#475569;font-size:0.83rem;margin-top:-0.5rem;'>Aproveite o tempo fora do pregão para revisar o cenário e preparar suas ordens.</p>", unsafe_allow_html=True)

        pan1, pan2, pan3 = st.columns(3)

        # Resumo do dia
        with pan1:
            contratos_hoje = [c for c in st.session_state['contratos']
                              if isinstance(c.get('criado_em'), datetime) and c['criado_em'].date() == gdt.date()]
            pnl_dia = sum(c.get('pnl_atual', 0) for c in contratos_hoje)
            log_hoje = [l for l in st.session_state.get('turn_log', [])
                        if gdt.strftime('%d/%m') in l]
            st.markdown(f"""<div class='card'>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;margin-bottom:0.75rem;'>📋 Resumo do Dia</div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.8rem;color:#94a3b8;margin-bottom:4px;'>
                    Contratos fechados hoje: <b style='color:#e2e8f0;'>{len(contratos_hoje)}</b></div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.8rem;color:#94a3b8;margin-bottom:4px;'>
                    PnL desses contratos: <b style='color:{"#00d4aa" if pnl_dia>=0 else "#fb7185"};'>{_fmt_brl(pnl_dia)}</b></div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.8rem;color:#94a3b8;'>
                    Eventos no log hoje: <b style='color:#e2e8f0;'>{len(log_hoje)}</b></div>
                <div style='margin-top:0.75rem;font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#334155;'>
                    PLD encerramento: <b style='color:#00d4aa;'>R$ {st.session_state['pld_atual']:.2f}</b></div>
            </div>""", unsafe_allow_html=True)

        # Previsão meteorológica
        with pan2:
            meteo = st.session_state['meteo']
            res   = meteo['reserv'][-1] if meteo['reserv'] else 50
            chuva = meteo['precip'][-1] if meteo['precip'] else 80
            fator_meteo, alertas_meteo = _impacto_meteo_no_pld(meteo)
            cor_res   = "#00d4aa" if res >= 60 else "#fbbf24" if res >= 40 else "#fb7185"
            cor_fat   = "#00d4aa" if fator_meteo <= 1.0 else "#fbbf24" if fator_meteo <= 1.2 else "#fb7185"
            alerta_txt = alertas_meteo[0][2] if alertas_meteo else "Cenário estável"
            st.markdown(f"""<div class='card'>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;margin-bottom:0.75rem;'>🌦️ Cenário Meteorológico</div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.8rem;color:#94a3b8;margin-bottom:4px;'>
                    Reservatórios: <b style='color:{cor_res};'>{res:.0f}%</b></div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.8rem;color:#94a3b8;margin-bottom:4px;'>
                    Chuvas: <b style='color:#e2e8f0;'>{chuva:.0f}%</b> da média</div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.8rem;color:#94a3b8;margin-bottom:0.75rem;'>
                    Pressão no PLD: <b style='color:{cor_fat};'>{fator_meteo:.2f}×</b></div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#64748b;border-top:1px solid #1e293b;padding-top:0.5rem;'>
                    ⚠ {alerta_txt}</div>
            </div>""", unsafe_allow_html=True)

        # Preparação de ordens
        with pan3:
            pld_now  = st.session_state['pld_atual']
            prox_abt = _proxima_abertura(gdt)
            horas_ft = int((prox_abt - gdt).total_seconds() // 3600)
            produtos_prox = _gerar_produtos(gdt)[:3]
            linhas_prod = "".join([
                f"<div style='display:flex;justify-content:space-between;padding:3px 0;"
                f"border-bottom:1px solid #1e293b;font-family:JetBrains Mono,monospace;font-size:0.75rem;'>"
                f"<span style='color:#64748b;'>{p['codigo']}</span>"
                f"<span style='color:#e2e8f0;'>R$ {_reference_price(p,'SE/CO'):.2f}</span></div>"
                for p in produtos_prox
            ])
            st.markdown(f"""<div class='card'>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;margin-bottom:0.75rem;'>🎯 Preparação de Ordens</div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#94a3b8;margin-bottom:0.5rem;'>
                    Abertura em <b style='color:#fbbf24;'>{horas_ft}h</b> ({prox_abt.strftime('%d/%m %H:%M')})</div>
                <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;margin-bottom:4px;text-transform:uppercase;'>Refs. de preço amanhã</div>
                {linhas_prod}
                <div style='margin-top:0.75rem;font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#334155;'>
                    Use <b style='color:#94a3b8;'>📒 Livro</b> para inserir ordens-limite agora — elas entram na fila às 09:00.</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

    st.markdown("")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PLD SE/CO",  f"R$ {pld:.2f}",               f"{var_pld:+.2f} R$/MWh")
    c2.metric("PLD Sul",    f"R$ {pld*SUBM['S']:.2f}",     "−5% SE/CO")
    c3.metric("PLD NE",     f"R$ {pld*SUBM['NE']:.2f}",    "+5% SE/CO")
    c4.metric("PLD Norte",  f"R$ {pld*SUBM['N']:.2f}",     "+10% SE/CO")

    st.markdown("")
    col_g, col_i = st.columns([3,1])
    with col_g:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_hist['Data'].astype(str), y=df_hist['PLD (R$/MWh)'],
            mode='lines', line=dict(color='#00d4aa', width=2),
            fill='tozeroy', fillcolor='rgba(0,212,170,0.07)',
            hovertemplate='%{x}<br>PLD: R$ %{y:.2f}<extra></extra>'))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569'),
            yaxis=dict(gridcolor='#1e293b', color='#475569', title='R$/MWh'),
            margin=dict(l=10,r=10,t=30,b=10), height=300,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
            title=dict(text='Histórico PLD SE/CO — Mensal Simulado', font=dict(size=13, color='#94a3b8')))
        st.plotly_chart(fig, use_container_width=True)
    with col_i:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;margin-bottom:0.75rem;'>Estatísticas (24m)</div>", unsafe_allow_html=True)
        for k, v in {"Mínimo": df_hist['PLD (R$/MWh)'].min(), "Máximo": df_hist['PLD (R$/MWh)'].max(),
                     "Média":  df_hist['PLD (R$/MWh)'].mean(), "Desvio": df_hist['PLD (R$/MWh)'].std()}.items():
            st.markdown(f"""<div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #1e293b;font-family:JetBrains Mono,monospace;font-size:0.8rem;'>
                <span style='color:#64748b;'>{k}</span><span style='color:#e2e8f0;'>R$ {v:.2f}</span></div>""", unsafe_allow_html=True)
        cor_f = "#00d4aa" if fator_meteo <= 1.0 else "#fbbf24" if fator_meteo <= 1.2 else "#fb7185"
        st.markdown(f"""<div style='display:flex;justify-content:space-between;padding:6px 0 0;font-family:JetBrains Mono,monospace;font-size:0.8rem;'>
            <span style='color:#64748b;'>Pressão Meteo</span>
            <span style='color:{cor_f};font-weight:700;'>{fator_meteo:.2f}×</span></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Curva Forward compacta no painel
    st.markdown("---")
    st.markdown("#### 📈 Curva Forward — Próximos 6 meses")
    produtos_graf = _gerar_produtos(gdt)[:6]
    fig_fw = go.Figure()
    fig_fw.add_trace(go.Bar(
        x=[p["codigo"] for p in produtos_graf],
        y=[_reference_price(p, "SE/CO") for p in produtos_graf],
        marker_color=['#00d4aa' if i == 0 else '#334155' for i in range(len(produtos_graf))],
        text=[f"R${_reference_price(p,'SE/CO'):.2f}" for p in produtos_graf],
        textposition='outside', textfont=dict(family='JetBrains Mono', size=10, color='#94a3b8'),
        hovertemplate='%{x}<br>R$ %{y:.2f}<extra></extra>'))
    fig_fw.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#1e293b', color='#475569'),
        yaxis=dict(gridcolor='#1e293b', color='#475569', title='R$/MWh'),
        margin=dict(l=10,r=10,t=10,b=10), height=200,
        font=dict(family='JetBrains Mono', size=11, color='#94a3b8'))
    st.plotly_chart(fig_fw, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔢 Calculadora Rápida de Exposição")
    cc1, cc2, cc3 = st.columns(3)
    with cc1: vol_c  = st.number_input("Volume (MW médio)", min_value=0.1, value=5.0, step=0.5)
    with cc2: preco_c = st.number_input("Preço (R$/MWh)", min_value=0.0, value=float(round(pld,0)), step=1.0)
    with cc3: horas_c = st.number_input("Horas do período", min_value=1, value=720, step=24)
    exp = (pld - preco_c) * vol_c * horas_c
    st.markdown(f"""<div style='display:flex;gap:1rem;margin-top:0.5rem;'>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;'>Energia Total</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.3rem;font-weight:700;color:#e2e8f0;'>{vol_c*horas_c:,.0f} MWh</div>
        </div>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;'>PnL se comprado</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.3rem;font-weight:700;color:{_cor_pnl(exp)};'>{_fmt_brl(exp)}</div>
        </div>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;'>PnL se vendido</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.3rem;font-weight:700;color:{_cor_pnl(-exp)};'>{_fmt_brl(-exp)}</div>
        </div></div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# LIVRO DE NEGÓCIOS
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'livro':
    gdt      = st.session_state['game_datetime']
    mkt_open = _is_market_open(gdt)
    st.markdown("# 📒 Livro de Negócios")
    st.markdown(f"<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>Order book por produto · Volumes em <b>MW médio mensal</b> · {_market_status_str(gdt)}</p>", unsafe_allow_html=True)
    st.markdown("---")

    if not mkt_open:
        st.markdown(f"<div class='market-closed-box'>🔴 <b>Mercado Fechado</b><br>Livro ativo apenas entre 09:00 e 18:00 de dias úteis.</div>", unsafe_allow_html=True)

    # Seletor de produto com nome do mês
    produtos_disp = _gerar_produtos(gdt)
    prod_opcoes   = {p["codigo"]: f"{p['codigo']} — {p['label']}" for p in produtos_disp}
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        prod_cod_sel = st.selectbox("Produto", list(prod_opcoes.keys()),
                                    format_func=lambda x: prod_opcoes[x], key="livro_produto")
    with col_sel2:
        subm_sel = st.selectbox("Submercado", list(SUBM.keys()), key="livro_subm")

    prod_sel   = _get_produto_by_codigo(prod_cod_sel, gdt)
    book       = st.session_state.get('order_book', {})
    bids       = book.get(prod_cod_sel, {}).get("bids", [])
    asks       = book.get(prod_cod_sel, {}).get("asks", [])
    fator_subm = SUBM[subm_sel]
    ref        = _reference_price(prod_sel, subm_sel) if prod_sel else 0

    bids_adj = [{"preco": round(b["preco"]*fator_subm,2), "volume_mwm": b["volume_mwm"], "contraparte": b["contraparte"]} for b in bids]
    asks_adj = [{"preco": round(a["preco"]*fator_subm,2), "volume_mwm": a["volume_mwm"], "contraparte": a["contraparte"]} for a in asks]

    melhor_bid = bids_adj[0]["preco"] if bids_adj else None
    melhor_ask = asks_adj[0]["preco"] if asks_adj else None
    spread     = round(melhor_ask - melhor_bid, 2) if (melhor_bid and melhor_ask) else None

    st.markdown(f"""<div style='display:flex;gap:1rem;margin-bottom:1rem;'>
        <div style='flex:1;background:#111827;border:1px solid #1e293b;border-radius:6px;padding:0.75rem 1rem;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>Referência {prod_cod_sel} {subm_sel}</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.4rem;font-weight:700;color:#e2e8f0;'>R$ {ref:.2f}</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#334155;'>{prod_sel["label"] if prod_sel else ""}</div>
        </div>
        <div style='flex:1;background:#111827;border:1px solid rgba(0,212,170,0.2);border-radius:6px;padding:0.75rem 1rem;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>Melhor Bid</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.4rem;font-weight:700;color:#00d4aa;'>{"R$ "+str(melhor_bid) if melhor_bid else "—"}</div>
        </div>
        <div style='flex:1;background:#111827;border:1px solid rgba(251,113,133,0.2);border-radius:6px;padding:0.75rem 1rem;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>Melhor Ask</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.4rem;font-weight:700;color:#fb7185;'>{"R$ "+str(melhor_ask) if melhor_ask else "—"}</div>
        </div>
        <div style='flex:1;background:#111827;border:1px solid #1e293b;border-radius:6px;padding:0.75rem 1rem;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>Spread</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.4rem;font-weight:700;color:#fbbf24;'>{"R$ "+str(spread) if spread else "—"}</div>
        </div></div>""", unsafe_allow_html=True)

    col_bid, col_ask = st.columns(2)
    with col_bid:
        st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#00d4aa;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;'>🟢 COMPRA (BID) — MW médio</div>", unsafe_allow_html=True)
        for i, b in enumerate(bids_adj[:6]):
            opac = max(0.3, 1 - i*0.15)
            st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;
                background:rgba(0,212,170,{opac*0.08:.2f});border:1px solid rgba(0,212,170,{opac*0.2:.2f});
                border-radius:4px;padding:6px 12px;margin-bottom:3px;font-family:JetBrains Mono,monospace;font-size:0.8rem;'>
                <span style='color:#00d4aa;font-weight:700;'>R$ {b["preco"]:.2f}</span>
                <span style='color:#64748b;'>{b["volume_mwm"]:.1f} MWm</span>
                <span style='color:#334155;font-size:0.65rem;'>{b["contraparte"][:18]}</span>
            </div>""", unsafe_allow_html=True)
    with col_ask:
        st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#fb7185;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;'>🔴 VENDA (ASK) — MW médio</div>", unsafe_allow_html=True)
        for i, a in enumerate(asks_adj[:6]):
            opac = max(0.3, 1 - i*0.15)
            st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;
                background:rgba(251,113,133,{opac*0.08:.2f});border:1px solid rgba(251,113,133,{opac*0.2:.2f});
                border-radius:4px;padding:6px 12px;margin-bottom:3px;font-family:JetBrains Mono,monospace;font-size:0.8rem;'>
                <span style='color:#fb7185;font-weight:700;'>R$ {a["preco"]:.2f}</span>
                <span style='color:#64748b;'>{a["volume_mwm"]:.1f} MWm</span>
                <span style='color:#334155;font-size:0.65rem;'>{a["contraparte"][:18]}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚡ Enviar Ordem")
    if not mkt_open:
        st.markdown("<div class='warn-box'>⚠️ Mercado fechado. Avance turnos até às 09:00.</div>", unsafe_allow_html=True)
    else:
        with st.form("form_ordem"):
            col1, col2, col3, col4 = st.columns(4)
            with col1: tipo_ord   = st.selectbox("Operação", ["Compra","Venda"])
            with col2: tipo_order = st.selectbox("Tipo de Ordem", ORDER_TYPES)
            with col3: vol_ord    = st.number_input("Volume (MW médio)", min_value=0.5, value=5.0, step=0.5,
                                                     help="MW médio mensal — o simulador calcula a energia total automaticamente")
            with col4: preco_ord  = st.number_input("Preço (R$/MWh)", min_value=30.0, value=float(round(ref,0)), step=0.5)
            sub_ord = st.form_submit_button("📤  ENVIAR ORDEM", type="primary", use_container_width=True)

        if sub_ord and prod_sel:
            fm, _ = _impacto_meteo_no_pld(st.session_state['meteo'])
            horas_prod = prod_sel.get('horas_mes', 720)
            ok_margem, msg_margem = _pode_negociar(vol_ord, horas_prod, ref)
            if not ok_margem:
                st.error(f"🚫 {msg_margem}")
            elif tipo_order == "Mercado (Market)":
                resultado, erro = _executar_ordem_mercado(tipo_ord, prod_cod_sel, vol_ord, subm_sel, gdt)
                if erro:
                    st.error(f"⚠️ {erro}")
                elif resultado:
                    _registrar_contrato_negociado(tipo_ord, resultado["preco"], resultado["volume_mwm"], prod_sel, subm_sel, resultado["contraparte"], gdt)
                    log = st.session_state.get('turn_log',[])
                    log.append(f'<span class="ts">[{gdt.strftime("%d/%m %H:%M")}]</span> <span class="deal">✅ DEAL — {tipo_ord} {resultado["volume_mwm"]:.1f}MWm {prod_cod_sel} @ R${resultado["preco"]:.2f} c/ {resultado["contraparte"]}</span>')
                    st.session_state['turn_log'] = log[-50:]
                    salvar_estado()
                    st.success(f"✅ Executado! {tipo_ord} de **{resultado['volume_mwm']:.1f} MWm** a **R$ {resultado['preco']:.2f}/MWh** com **{resultado['contraparte']}**")
                    if resultado.get("parcial"):
                        st.warning("⚠️ Execução parcial — volume disponível era menor.")
            else:
                cp_sel = random.choice(COUNTERPARTIES)
                prob   = _prob_aceitar(preco_ord, ref, fm, tipo_ord, cp_sel)
                if random.random() < prob:
                    _registrar_contrato_negociado(tipo_ord, preco_ord, vol_ord, prod_sel, subm_sel, cp_sel["nome"], gdt)
                    log = st.session_state.get('turn_log',[])
                    log.append(f'<span class="ts">[{gdt.strftime("%d/%m %H:%M")}]</span> <span class="deal">✅ DEAL — {tipo_ord} {vol_ord:.1f}MWm {prod_cod_sel} @ R${preco_ord:.2f} c/ {cp_sel["nome"]}</span>')
                    st.session_state['turn_log'] = log[-50:]
                    salvar_estado()
                    st.success(f"✅ Aceito por **{cp_sel['nome']}** (prob. {prob:.0%})")
                else:
                    desvio = round((preco_ord - ref) / ref * 100, 1)
                    if abs(desvio) > 5:
                        st.error(f"❌ Recusado — preço {desvio:+.1f}% fora da referência R$ {ref:.2f}")
                    else:
                        cp2 = round(ref * (0.99 if tipo_ord=="Compra" else 1.01), 2)
                        st.warning(f"🔄 **{cp_sel['nome']}** contrapropos R$ {cp2:.2f}/MWh (prob. aceite {prob:.0%}). Ajuste e reenvie.")

    # Curva completa
    st.markdown("---")
    st.markdown("#### 📋 Curva Forward Completa")
    todos_prods = _gerar_produtos(gdt)
    mensal   = [p for p in todos_prods if p["tipo"]=="M"]
    trimest  = [p for p in todos_prods if p["tipo"]=="Q"]
    anual    = [p for p in todos_prods if p["tipo"]=="A"]
    fig_fw2 = go.Figure()
    fig_fw2.add_trace(go.Scatter(x=[p["codigo"] for p in mensal], y=[_reference_price(p, subm_sel) for p in mensal],
        mode='lines+markers', name='Mensal', line=dict(color='#00d4aa',width=2), marker=dict(size=7)))
    fig_fw2.add_trace(go.Scatter(x=[p["codigo"] for p in trimest], y=[_reference_price(p, subm_sel) for p in trimest],
        mode='markers', name='Trimestral', marker=dict(size=12, color='#a78bfa', symbol='diamond')))
    fig_fw2.add_trace(go.Scatter(x=[p["codigo"] for p in anual], y=[_reference_price(p, subm_sel) for p in anual],
        mode='markers', name='Anual', marker=dict(size=14, color='#fbbf24', symbol='star')))
    fig_fw2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#1e293b', color='#475569'),
        yaxis=dict(gridcolor='#1e293b', color='#475569', title='R$/MWh'),
        margin=dict(l=10,r=10,t=30,b=10), height=280,
        font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8')),
        title=dict(text=f'Curva Forward {subm_sel} — nomes dos meses reais', font=dict(size=13, color='#94a3b8')))
    st.plotly_chart(fig_fw2, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# RFQs
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'rfqs':
    gdt      = st.session_state['game_datetime']
    mkt_open = _is_market_open(gdt)
    st.markdown("# 📨 RFQs — Pedidos de Cotação")
    st.markdown(f"<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>Ofertas de contrapartes · Volumes em MW médio · {_market_status_str(gdt)}</p>", unsafe_allow_html=True)
    st.markdown("---")

    pending  = st.session_state.get('pending_rfqs', [])
    ativos   = [r for r in pending if r['status']=='pendente']
    historico= [r for r in pending if r['status']!='pendente']

    if not ativos:
        st.markdown("<div class='info-box'>📭 Nenhum RFQ pendente. Avance turnos — contrapartes enviam durante 09h–18h.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"#### {len(ativos)} RFQ(s) Pendente(s)")
        for rfq in ativos:
            cor_dev = "#00d4aa" if (rfq['tipo']=="Venda" and rfq['desvio_pct']<0) or (rfq['tipo']=="Compra" and rfq['desvio_pct']>0) else "#fbbf24"
            exp_em  = rfq['expira_turno'] - st.session_state['turno']
            cp_rfq  = next((x for x in COUNTERPARTIES if x['nome']==rfq['contraparte']), {})
            perf_rfq= cp_rfq.get('perfil', 'padrao')
            p_labels_rfq = {"agressiva":"AGRESS","conservadora":"CONSERV","inadimplente":"INADIMP","padrao":"PADRÃO"}
            p_lbl_rfq = p_labels_rfq.get(perf_rfq, perf_rfq.upper())
            st.markdown(f"""<div class='rfq-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
                    <span style='color:#e2e8f0;font-weight:700;'>#{rfq['id']} · {rfq['contraparte']}&nbsp;<span class='perfil-badge perfil-{perf_rfq}'>{p_lbl_rfq}</span></span>
                    <span style='color:#334155;font-size:0.65rem;'>Recebido {rfq['timestamp']} · Expira em {exp_em} turno(s)</span>
                </div>
                <div style='display:flex;gap:1.5rem;flex-wrap:wrap;'>
                    <div><span style='color:#475569;'>Tipo: </span><span style='color:#e2e8f0;'>{rfq["tipo"]}</span></div>
                    <div><span style='color:#475569;'>Produto: </span><span style='color:#e2e8f0;'>{rfq["produto_lab"]}</span></div>
                    <div><span style='color:#475569;'>Volume: </span><span style='color:#e2e8f0;font-weight:700;'>{rfq["volume_mwm"]:.1f} MWm</span></div>
                    <div><span style='color:#475569;'>Preço: </span><span style='color:#fbbf24;font-weight:700;'>R$ {rfq["preco"]:.2f}</span></div>
                    <div><span style='color:#475569;'>Ref: </span><span style='color:#64748b;'>R$ {rfq["referencia"]:.2f}</span></div>
                    <div><span style='color:#475569;'>Desvio: </span><span style='color:{cor_dev};'>{rfq["desvio_pct"]:+.1f}%</span></div>
                    <div><span style='color:#475569;'>Submercado: </span><span style='color:#e2e8f0;'>{rfq["submercado"]}</span></div>
                </div></div>""", unsafe_allow_html=True)

            col_ac, col_rc, col_neg = st.columns(3)
            with col_ac:
                if st.button(f"✅ Aceitar #{rfq['id']}", key=f"ac_{rfq['id']}", use_container_width=True):
                    if not mkt_open:
                        st.error("Mercado fechado.")
                    else:
                        prod_rfq = _get_produto_by_codigo(rfq['produto_cod'], gdt)
                        ok_m, msg_m = _pode_negociar(rfq['volume_mwm'], prod_rfq.get('horas_mes', 720) if prod_rfq else 720, rfq['preco'])
                        if not ok_m:
                            st.error(f"🚫 {msg_m}")
                        else:
                            rfq['status'] = 'aceito'
                            tipo_c = "Compra" if rfq['tipo']=="Venda" else "Venda"
                            if prod_rfq:
                                _registrar_contrato_negociado(tipo_c, rfq['preco'], rfq['volume_mwm'], prod_rfq, rfq['submercado'], rfq['contraparte'], gdt)
                                log = st.session_state.get('turn_log',[])
                                log.append(f'<span class="ts">[{gdt.strftime("%d/%m %H:%M")}]</span> <span class="deal">✅ RFQ #{rfq["id"]} aceito — {tipo_c} {rfq["volume_mwm"]:.1f}MWm {rfq["produto_cod"]} @ R${rfq["preco"]:.2f}</span>')
                                st.session_state['turn_log'] = log[-50:]
                                salvar_estado()
                            st.rerun()
            with col_rc:
                if st.button(f"❌ Recusar #{rfq['id']}", key=f"rc_{rfq['id']}", use_container_width=True):
                    rfq['status'] = 'recusado'; salvar_estado(); st.rerun()
            with col_neg:
                st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#334155;padding:0.4rem;'>Contraproposta: ajuste no Livro de Negócios</div>", unsafe_allow_html=True)

    if historico:
        st.markdown("---")
        st.markdown("#### 📋 Histórico")
        for rfq in reversed(historico[-15:]):
            cor  = "#00d4aa" if rfq['status']=='aceito' else "#fb7185" if rfq['status']=='recusado' else "#475569"
            icon = "✅" if rfq['status']=='aceito' else "❌" if rfq['status']=='recusado' else "⏳"
            st.markdown(f"""<div style='display:flex;gap:1rem;padding:6px 0;border-bottom:1px solid #1e293b;font-family:JetBrains Mono,monospace;font-size:0.75rem;'>
                <span style='color:{cor};'>{icon}</span>
                <span style='color:#64748b;'>{rfq["timestamp"]}</span>
                <span style='color:#e2e8f0;'>{rfq["contraparte"]}</span>
                <span style='color:#94a3b8;'>{rfq["tipo"]} {rfq.get("produto_lab",rfq.get("produto_cod",""))} {rfq["volume_mwm"]:.1f}MWm</span>
                <span style='color:#fbbf24;'>R$ {rfq["preco"]:.2f}</span>
                <span style='color:{cor};'>{rfq["status"].upper()}</span>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# METEOROLOGIA
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'meteo':
    gdt = st.session_state['game_datetime']
    st.markdown("# 🌦️ Meteorologia & Hidrologia")
    st.markdown(f"<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>Condições climáticas · {gdt.strftime('%d/%m/%Y %H:%M')}</p>", unsafe_allow_html=True)
    st.markdown("---")
    meteo = st.session_state['meteo']
    datas_str = meteo['datas']
    fator_meteo, alertas = _impacto_meteo_no_pld(meteo)
    if alertas:
        for icone, tipo, msg in alertas:
            box_class = "danger-box" if tipo=="danger" else "warn-box" if tipo=="warn" else "info-box"
            st.markdown(f"<div class='{box_class}'>{icone} {msg}</div>", unsafe_allow_html=True)
        st.markdown("")

    m1,m2,m3,m4,m5,m6 = st.columns(6)
    ra = meteo['reserv'][-1]; aa = meteo['afluen'][-1]
    pa = meteo['precip'][-1]; ta = meteo['temp'][-1]
    ea = meteo['eolica'][-1]; sa = meteo['solar'][-1]
    rp = meteo['reserv'][-2] if len(meteo['reserv'])>1 else ra
    ap = meteo['afluen'][-2] if len(meteo['afluen'])>1 else aa
    ep = meteo['eolica'][-2] if len(meteo['eolica'])>1 else ea
    m1.metric("Reservatório", f"{ra:.0f}%",  f"{ra-rp:+.1f}%")
    m2.metric("Afluência MLT",f"{aa:.0f}%",  f"{aa-ap:+.1f}%")
    m3.metric("Precipitação", f"{pa:.0f} mm")
    m4.metric("Temperatura",  f"{ta:.1f}°C")
    m5.metric("Eólica NE",    f"{ea:.0f}%",  f"{ea-ep:+.1f}%")
    m6.metric("Solar",        f"{sa:.0f}%")
    cor_f = "#00d4aa" if fator_meteo<=1.0 else "#fbbf24" if fator_meteo<=1.2 else "#fb7185"
    prox  = METEO_UPDATE_HOURS - (turno % METEO_UPDATE_HOURS)
    st.markdown(f"""<div style='background:#111827;border:1px solid #1e293b;border-radius:8px;padding:1rem 1.5rem;margin-top:1rem;display:flex;justify-content:space-between;align-items:center;'>
        <div>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;'>Fator de Pressão Meteorológica sobre o PLD</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#334155;margin-top:4px;'>Próxima atualização: <b style='color:#475569'>{prox}h</b></div>
        </div>
        <div style='text-align:right;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:2rem;font-weight:700;color:{cor_f};'>{fator_meteo:.2f}×</div>
        </div></div>""", unsafe_allow_html=True)

    def _lf():
        return dict(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569'),
            yaxis=dict(gridcolor='#1e293b', color='#475569'),
            margin=dict(l=10,r=10,t=30,b=10), height=260,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8')))

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["💧 Hidrologia", "🌡️ Clima", "⚡ Renováveis"])
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            f = go.Figure(); f.add_trace(go.Scatter(x=datas_str,y=meteo['reserv'],mode='lines',line=dict(color='#60a5fa',width=2),fill='tozeroy',fillcolor='rgba(96,165,250,0.08)'))
            f.add_hline(y=40,line_color='#fbbf24',line_dash='dash'); f.add_hline(y=20,line_color='#fb7185',line_dash='dash')
            l=_lf(); l['yaxis']['range']=[0,105]; l['yaxis']['title']='%'; f.update_layout(**l)
            st.plotly_chart(f, use_container_width=True)
        with c2:
            f2=go.Figure(); f2.add_trace(go.Bar(x=datas_str,y=meteo['afluen'],marker_color=['#fb7185' if v<50 else '#fbbf24' if v<80 else '#00d4aa' for v in meteo['afluen']]))
            f2.add_hline(y=100,line_color='#475569',line_dash='dash'); l2=_lf(); l2['yaxis']['title']='% MLT'; f2.update_layout(**l2)
            st.plotly_chart(f2, use_container_width=True)
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            f=go.Figure(); f.add_trace(go.Bar(x=datas_str,y=meteo['precip'],marker_color='rgba(96,165,250,0.7)'))
            l=_lf(); l['yaxis']['title']='mm/mês'; f.update_layout(**l)
            st.plotly_chart(f, use_container_width=True)
        with c2:
            f=go.Figure(); f.add_trace(go.Scatter(x=datas_str,y=meteo['temp'],mode='lines+markers',line=dict(color='#f59e0b',width=2)))
            f.add_hline(y=30,line_color='#fb7185',line_dash='dash'); l=_lf(); l['yaxis']['title']='°C'; f.update_layout(**l)
            st.plotly_chart(f, use_container_width=True)
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            f=go.Figure(); f.add_trace(go.Scatter(x=datas_str,y=meteo['eolica'],mode='lines',line=dict(color='#a78bfa',width=2),fill='tozeroy',fillcolor='rgba(167,139,250,0.08)'))
            l=_lf(); l['yaxis']['range']=[0,105]; l['yaxis']['title']='% cap.'; f.update_layout(**l)
            st.plotly_chart(f, use_container_width=True)
        with c2:
            f=go.Figure(); f.add_trace(go.Scatter(x=datas_str,y=meteo['solar'],mode='lines',line=dict(color='#f59e0b',width=2),fill='tozeroy',fillcolor='rgba(245,158,11,0.08)'))
            l=_lf(); l['yaxis']['range']=[0,105]; l['yaxis']['title']='% cap.'; f.update_layout(**l)
            st.plotly_chart(f, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# NOVO CONTRATO (OTC manual)
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'novo_contrato':
    gdt = st.session_state['game_datetime']
    st.markdown("# 📋 Novo Contrato OTC")
    st.markdown(f"<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>Contrato bilateral manual · {gdt.strftime('%d/%m/%Y %H:%M')}</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div class='info-box'>💡 Para negociar via livro ou RFQ use as páginas correspondentes. Esta página é para contratos OTC bilaterais manuais.</div>", unsafe_allow_html=True)
    fm, _ = _impacto_meteo_no_pld(st.session_state['meteo'])
    if fm > 1.15:
        st.markdown(f"<div class='warn-box'>⚠️ Fator meteo {fm:.2f}× — pressão de alta no PLD.</div>", unsafe_allow_html=True)

    # Produtos com nome dos meses
    produtos_disp = _gerar_produtos(gdt)
    prod_opcoes   = {p["codigo"]: f"{p['codigo']} — {p['label']}" for p in produtos_disp}

    with st.form("form_contrato_otc"):
        col1, col2 = st.columns(2)
        with col1: nome_c  = st.text_input("Nome / Referência", placeholder="ex: CONTRATO-001")
        with col2: cp_nome = st.text_input("Contraparte", placeholder="ex: Cemig GT")

        col3, col4, col5 = st.columns(3)
        with col3: tipo_op  = st.selectbox("Tipo", ["Compra","Venda"])
        with col4: subm_otc = st.selectbox("Submercado", list(SUBM.keys()))
        with col5: tp_energ = st.selectbox("Energia", TIPOS_ENERGIA)

        col6, col7, col8 = st.columns(3)
        with col6: preco_otc = st.number_input("Preço (R$/MWh)", min_value=0.01, value=float(round(st.session_state['pld_atual'],0)), step=1.0)
        with col7:
            vol_otc = st.number_input("Volume (MW médio)", min_value=0.1, value=1.0, step=0.5,
                                       help="MW médio mensal — a energia total depende do prazo do produto")
        with col8: indice = st.selectbox("Índice", INDICES)

        prod_sel_cod = st.selectbox("Produto", list(prod_opcoes.keys()), format_func=lambda x: prod_opcoes[x])

        col9, col10 = st.columns(2)
        with col9:  gross_up = st.checkbox("Gross-up PIS/COFINS (9,25%)", value=False)
        with col10: flag_pc  = st.checkbox("Flag P/C na boleta", value=False)
        obs = st.text_area("Observações", height=60)
        submitted = st.form_submit_button("✅  REGISTRAR CONTRATO", type="primary", use_container_width=True)

    if submitted:
        if not nome_c:
            st.error("⚠️ Informe o nome.")
        else:
            prod_otc = _get_produto_by_codigo(prod_sel_cod, gdt)
            if prod_otc:
                preco_adj = preco_otc * 1.0925 if gross_up else preco_otc
                horas     = prod_otc["horas_mes"]
                novo = {
                    'id': len(st.session_state['contratos'])+1,
                    'nome': nome_c, 'contraparte': cp_nome,
                    'tipo': tipo_op, 'submercado': subm_otc, 'tipo_energia': tp_energ,
                    'preco': preco_adj, 'volume_mwm': vol_otc, 'indice': indice,
                    'data_inicio': prod_otc['inicio'], 'data_fim': prod_otc['fim'],
                    'horas': horas, 'gross_up': gross_up, 'flag_pc': flag_pc,
                    'obs': obs, 'pnl_atual': 0.0, 'criado_em': datetime.now(),
                    'produto_cod': prod_sel_cod, 'produto_lab': prod_otc['label'],
                }
                _recalc_pnl(novo)
                st.session_state['contratos'].append(novo)
                salvar_estado()
                energia_total = vol_otc * horas
                st.success(f"✅ **{nome_c}** registrado! {vol_otc:.1f} MWm · {energia_total:,.0f} MWh total · R$ {preco_adj:.2f}/MWh")

# ════════════════════════════════════════════════════════════════════════════════
# PORTFÓLIO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'portfolio':
    st.markdown("# 💼 Meu Portfólio")
    st.markdown("<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>Volumes em MW médio mensal (MWm)</p>", unsafe_allow_html=True)
    st.markdown("---")
    if not st.session_state['contratos']:
        st.markdown("<div class='warn-box'>⚠️ Nenhum contrato. Use Livro, RFQs ou Novo Contrato OTC.</div>", unsafe_allow_html=True)
    else:
        contratos = st.session_state['contratos']
        pos_c = sum(c.get('volume_mwm',c.get('volume_mw',0)) for c in contratos if c['tipo']=='Compra')
        pos_v = sum(c.get('volume_mwm',c.get('volume_mw',0)) for c in contratos if c['tipo']=='Venda')
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Posição Comprada", f"{pos_c:.1f} MWm")
        m2.metric("Posição Vendida",  f"{pos_v:.1f} MWm")
        m3.metric("Posição Líquida",  f"{pos_c-pos_v:+.1f} MWm")
        m4.metric("Contratos Ativos", len(contratos))
        st.markdown("")
        for c in contratos:
            pnl_cor  = _cor_pnl(c['pnl_atual'])
            vol_exib = c.get('volume_mwm', c.get('volume_mw',0))
            prod_lab = c.get('produto_lab', c.get('produto_cod', 'OTC'))
            with st.expander(f"#{c['id']} [{prod_lab}] — {c['nome']} | {vol_exib:.1f} MWm | R$ {c['preco']:.2f}/MWh"):
                col_a, col_b, col_c = st.columns(3)
                with col_a: st.markdown(f"**Tipo:** {c['tipo']} | **Contraparte:** {c.get('contraparte','—')}<br>**Submercado:** {c['submercado']}", unsafe_allow_html=True)
                with col_b: st.markdown(f"**Preço:** R$ {c['preco']:.2f}/MWh<br>**Volume:** {vol_exib:.1f} MWm | **Horas:** {c.get('horas',720):,} h<br>**Energia:** {vol_exib*c.get('horas',720):,.0f} MWh", unsafe_allow_html=True)
                with col_c: st.markdown(f"**Início:** {c['data_inicio']} | **Fim:** {c['data_fim']}", unsafe_allow_html=True)
                st.markdown(f"""<div style='margin-top:0.75rem;padding:0.75rem 1rem;background:#0d1117;border-radius:6px;display:flex;justify-content:space-between;'>
                    <span style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#475569;text-transform:uppercase;'>PnL vs PLD Mensal Atual</span>
                    <span style='font-family:JetBrains Mono,monospace;font-size:1.1rem;font-weight:700;color:{pnl_cor};'>{_fmt_brl(c['pnl_atual'])}</span>
                </div>""", unsafe_allow_html=True)
                if c.get('status') not in ('liquidado', 'inadimplido'):
                    if st.button(f"🗑️ Remover #{c['id']}", key=f"del_{c['id']}"):
                        st.session_state['contratos'] = [x for x in st.session_state['contratos'] if x['id']!=c['id']]
                        salvar_estado(); st.rerun()
                else:
                    status_cor = "#00d4aa" if c['status']=='liquidado' else "#fb7185"
                    st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:{status_cor};margin-top:0.5rem;'>"
                                f"{'✅ LIQUIDADO' if c['status']=='liquidado' else '💀 INADIMPLIDO'} · PnL Realizado: {_fmt_brl(c.get('pnl_realizado',0))}</div>",
                                unsafe_allow_html=True)

    # ── Saldo caixa + histórico de liquidações ────────────────────────────────
    saldo    = st.session_state.get('saldo_caixa', 0.0)
    liq_hist = st.session_state.get('liquidacoes', [])
    if saldo != 0.0 or liq_hist:
        st.markdown("---")
        st.markdown("#### 💵 Caixa Realizado")
        scor = "#00d4aa" if saldo >= 0 else "#fb7185"
        st.markdown(f"""<div style='background:#111827;border:1px solid #1e293b;border-radius:8px;padding:1rem 1.5rem;margin-bottom:1rem;display:flex;justify-content:space-between;align-items:center;'>
            <div><div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>Saldo Caixa (PnL Realizado)</div>
                 <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#334155;margin-top:2px;'>{len(liq_hist)} contratos liquidados/inadimplidos</div></div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.8rem;font-weight:700;color:{scor};'>{_fmt_brl(saldo)}</div>
        </div>""", unsafe_allow_html=True)
        if liq_hist:
            st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#475569;text-transform:uppercase;margin-bottom:6px;'>Histórico de Liquidações</div>", unsafe_allow_html=True)
            for liq in reversed(liq_hist[-15:]):
                cls = "liquidado-row" if liq['status']=='liquidado' else "default-row"
                icn = "✅" if liq['status']=='liquidado' else "💀"
                cor = "#00d4aa" if liq['pnl_realizado']>=0 else "#fb7185"
                st.markdown(f"<div class='{cls}'>{icn} <b style='color:#e2e8f0;'>{liq['nome']}</b> · "
                            f"<span style='color:#64748b;'>{liq['contraparte']}</span> · "
                            f"<span style='color:{cor};font-weight:700;'>{_fmt_brl(liq['pnl_realizado'])}</span> "
                            f"<span style='color:#334155;float:right;'>{liq.get('data','')}</span></div>",
                            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PnL & RESULTADO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'pnl':
    st.markdown("# 💰 PnL & Resultado")
    st.markdown("<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>Mark to Market vs PLD mensal</p>", unsafe_allow_html=True)
    st.markdown("---")
    if not st.session_state['contratos']:
        st.markdown("<div class='warn-box'>⚠️ Nenhum contrato registrado.</div>", unsafe_allow_html=True)
    else:
        contratos   = st.session_state['contratos']
        pld         = st.session_state['pld_atual']
        pnl_total   = sum(c['pnl_atual'] for c in contratos)
        pnl_compras = sum(c['pnl_atual'] for c in contratos if c['tipo']=='Compra')
        pnl_vendas  = sum(c['pnl_atual'] for c in contratos if c['tipo']=='Venda')
        m1,m2,m3 = st.columns(3)
        m1.metric("PnL Total",   _fmt_brl(pnl_total))
        m2.metric("PnL Compras", _fmt_brl(pnl_compras))
        m3.metric("PnL Vendas",  _fmt_brl(pnl_vendas))

        nomes = [c['nome'] for c in contratos]
        pnls  = [c['pnl_atual'] for c in contratos]
        fig_b = go.Figure(go.Bar(x=nomes, y=pnls, marker_color=['#00d4aa' if v>=0 else '#fb7185' for v in pnls],
            text=[_fmt_brl(v) for v in pnls], textposition='outside',
            textfont=dict(family='JetBrains Mono', size=10)))
        fig_b.add_shape(type='line', x0=-0.5, x1=len(nomes)-0.5, y0=0, y1=0, line=dict(color='#475569',width=1,dash='dash'))
        fig_b.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569'),
            yaxis=dict(gridcolor='#1e293b', color='#475569', title='PnL (R$)'),
            margin=dict(l=10,r=10,t=40,b=10), height=320,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
            title=dict(text='PnL por Contrato vs PLD Mensal Atual', font=dict(size=13, color='#94a3b8')))
        st.plotly_chart(fig_b, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🔮 Simulador de Cenário")
        pld_sim = st.slider("PLD Hipotético (R$/MWh)", 30.0, 500.0, float(round(pld,0)), 5.0)
        pnl_sim = []
        for c in contratos:
            vol = c.get('volume_mwm', c.get('volume_mw',1))
            h   = c.get('horas', 720)
            pnl_sim.append((pld_sim - c['preco'])*vol*h if c['tipo']=='Compra' else (c['preco']-pld_sim)*vol*h)
        pnl_sim_tot = sum(pnl_sim)
        sc1,sc2,sc3 = st.columns(3)
        sc1.metric("PLD Hipotético",    f"R$ {pld_sim:.2f}", f"{pld_sim-pld:+.2f}")
        sc2.metric("PnL no Cenário",    _fmt_brl(pnl_sim_tot))
        sc3.metric("Variação vs Atual", _fmt_brl(pnl_sim_tot - pnl_total))

        pld_r = np.linspace(30, 500, 200)
        pnl_r = []
        for p in pld_r:
            s = sum((p-c['preco'])*c.get('volume_mwm',c.get('volume_mw',1))*c.get('horas',720) if c['tipo']=='Compra'
                    else (c['preco']-p)*c.get('volume_mwm',c.get('volume_mw',1))*c.get('horas',720) for c in contratos)
            pnl_r.append(s)
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(x=pld_r, y=pnl_r, mode='lines', line=dict(color='#00d4aa',width=2),
            fill='tozeroy', fillcolor='rgba(0,212,170,0.05)',
            hovertemplate='PLD: R$ %{x:.0f}<br>PnL: R$ %{y:,.0f}<extra></extra>'))
        fig_s.add_vline(x=pld,     line_color='#94a3b8', line_dash='dash', annotation_text=f"Atual R${pld:.0f}", annotation_font_color='#94a3b8')
        fig_s.add_vline(x=pld_sim, line_color='#fbbf24', line_dash='dot',  annotation_text=f"Cenário R${pld_sim:.0f}", annotation_font_color='#fbbf24')
        fig_s.add_hline(y=0, line_color='#475569', line_dash='dash')
        fig_s.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569', title='PLD (R$/MWh)'),
            yaxis=dict(gridcolor='#1e293b', color='#475569', title='PnL (R$)'),
            margin=dict(l=10,r=10,t=30,b=10), height=300,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'))
        st.plotly_chart(fig_s, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# LOG DE TURNOS
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'log':
    gdt = st.session_state['game_datetime']
    st.markdown("# 📜 Log de Turnos")
    st.markdown(f"<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>Turno <b style='color:#00d4aa'>#{turno}</b> · {gdt.strftime('%d/%m/%Y %H:%M')} · {_market_status_str(gdt)}</p>", unsafe_allow_html=True)
    st.markdown("---")
    ca,cb,cc,cd = st.columns(4)
    ca.metric("Turnos Jogados", turno)
    cb.metric("Horas Simuladas", turno)
    cc.metric("Dias Simulados", turno // 24)
    cd.metric("RFQs Pendentes", len([r for r in st.session_state.get('pending_rfqs',[]) if r['status']=='pendente']))
    st.markdown("")
    turn_log = st.session_state.get('turn_log',[])
    if not turn_log:
        st.markdown("<div class='warn-box'>⚠️ Nenhum turno avançado ainda.</div>", unsafe_allow_html=True)
    else:
        log_html = "".join(f"<div class='turn-log-item'>{item}</div>" for item in reversed(turn_log))
        st.markdown(f"""<div style='background:#0d1117;border:1px solid #1e293b;border-radius:8px;padding:0.75rem 1rem;max-height:500px;overflow-y:auto;'>{log_html}</div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='display:flex;gap:1rem;flex-wrap:wrap;'>
        <div class='card' style='flex:1;min-width:140px;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>Mercado Aberto</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1rem;font-weight:700;color:#00d4aa;'>09:00 – 18:00</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:#334155;'>Seg a Sex</div>
        </div>
        <div class='card' style='flex:1;min-width:140px;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>PLD Mensal</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1rem;font-weight:700;color:#60a5fa;'>Cada 6h de jogo</div>
        </div>
        <div class='card' style='flex:1;min-width:140px;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>Meteo</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1rem;font-weight:700;color:#a78bfa;'>Cada 24h de jogo</div>
        </div>
        <div class='card' style='flex:1;min-width:140px;'>
            <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#475569;text-transform:uppercase;'>Contrapartes</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1rem;font-weight:700;color:#fbbf24;'>108 agentes</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# CONTRAPARTES
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'contrapartes':
    st.markdown("# 🏢 Contrapartes")
    st.markdown(f"<p style='color:#475569;font-size:0.85rem;margin-top:-0.5rem;'>{len(COUNTERPARTIES)} agentes simulados no mercado</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Filtros
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos","Vendedora","Compradora","Ambos"])
    with col_f2:
        filtro_texto = st.text_input("Buscar por nome", placeholder="Digite para filtrar...")

    tipos_cores = {"Vendedora": "#fb7185", "Compradora": "#00d4aa", "Ambos": "#a78bfa"}
    tipos_labels = {"Vendedora": "VEND", "Compradora": "COMP", "Ambos": "AMBOS"}
    perfil_labels = {"agressiva": "AGRESS", "conservadora": "CONSERV", "inadimplente": "INADIMP", "padrao": "PADRÃO"}
    cps_filtrados = COUNTERPARTIES
    if filtro_tipo != "Todos":
        cps_filtrados = [cp for cp in cps_filtrados if cp['tipo'] == filtro_tipo]
    if filtro_texto:
        cps_filtrados = [cp for cp in cps_filtrados if filtro_texto.lower() in cp['nome'].lower()]

    # Estatísticas
    n_vend = sum(1 for cp in COUNTERPARTIES if cp['tipo']=='Vendedora')
    n_comp = sum(1 for cp in COUNTERPARTIES if cp['tipo']=='Compradora')
    n_amb  = sum(1 for cp in COUNTERPARTIES if cp['tipo']=='Ambos')
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total", len(COUNTERPARTIES))
    c2.metric("Vendedoras", n_vend)
    c3.metric("Compradoras", n_comp)
    c4.metric("Ambos",  n_amb)
    st.markdown("")

    st.markdown(f"**Exibindo {len(cps_filtrados)} contraparte(s)**")
    for cp in cps_filtrados:
        cor   = tipos_cores.get(cp['tipo'], '#94a3b8')
        label = tipos_labels.get(cp['tipo'], cp['tipo'])
        agg   = int(cp['agressividade'] * 10)
        barra = "█" * agg + "░" * (10-agg)
        perf  = cp.get('perfil', 'padrao')
        p_lbl = perfil_labels.get(perf, perf.upper())
        st.markdown(f"""<div style='background:#111827;border:1px solid #1e293b;border-radius:6px;padding:0.6rem 1rem;margin-bottom:4px;
                    display:flex;align-items:center;gap:1rem;font-family:JetBrains Mono,monospace;font-size:0.75rem;'>
            <span style='color:{cor};font-weight:700;min-width:50px;'>{label}</span>
            <span class='perfil-badge perfil-{perf}'>{p_lbl}</span>
            <span style='color:#e2e8f0;min-width:180px;'>{cp["nome"]}</span>
            <span style='color:#64748b;flex:1;'>{cp["descricao"]}</span>
            <span style='color:#334155;font-size:0.65rem;'>Agressiv: <span style='color:{cor};'>{barra}</span></span>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# GLOSSÁRIO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'glossario':
    st.markdown("# 📚 Glossário")
    st.markdown("---")
    termos = [
        ("PLD Mensal", "Preço de Liquidação das Diferenças calculado mensalmente pelo DESSEM/CCEE. No simulador, refletido no nível médio do mês com variações a cada 6 turnos."),
        ("MW médio (MWm)", "Potência média contratada para o período. A energia total = MWm × horas do período. Ex: 5 MWm × 720h = 3.600 MWh."),
        ("Produto (mês/trimestre/ano)", "Cada produto tem o nome real: 'JAN/26', 'T1/26', 'ANO/2026'. O preço sobe levemente com o prazo (prêmio de curva de ~0,5%/mês)."),
        ("DESSEM", "Modelo de despacho hidrotérmico de curto prazo (ONS). Base do PLD horário desde 2020. Usa MILP com unit commitment de termelétricas."),
        ("CMO", "Custo Marginal de Operação — custo-sombra do balanço de carga no DESSEM. Determina o PLD antes dos limites regulatórios."),
        ("Order Book (Livro de Ordens)", "Registro de bids (compradores) e asks (vendedores) por produto. Spread = Ask mín − Bid máx."),
        ("RFQ", "Request for Quote — pedido de cotação de uma das 108 contrapartes. Aceite, recusa ou contraproposta durante 09h–18h."),
        ("Curva Forward", "Sequência de preços por produto: preços futuros tipicamente acima do PLD spot por conta do prêmio de risco de prazo."),
        ("Calendar Spread", "Compra de um produto + venda de outro prazo. Ex: compra ANO/2027 + venda T1/26 apostando em spread crescente."),
        ("Mark to Market (MtM)", "PnL = (PLD − Preço) × MWm × Horas para compras. Para vendas, sinal invertido."),
        ("Horário de Mercado", "09:00–18:00 de dias úteis (horário do jogo). RFQs e ordens só são processados nesse período."),
        ("f_meteo", "Fator de pressão climatológica sobre o PLD. >1.2 = crítico (alta); <0.9 = favorável (baixa). Gerado pelas variáveis hidrológicas."),
        ("MLT / EAR", "MLT = Média de Longo Termo das afluências. EAR = Energia Armazenável Real (%). Indicadores-chave de risco hídrico."),
    ]
    for termo, defin in termos:
        with st.expander(f"📌 {termo}"):
            st.markdown(f"<div style='font-family:Syne,sans-serif;font-size:0.88rem;color:#94a3b8;line-height:1.7;'>{defin}</div>", unsafe_allow_html=True)