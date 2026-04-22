import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import random
import json
import os

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

.danger-box {
    background: rgba(251, 113, 133, 0.05);
    border-left: 3px solid #fb7185;
    padding: 0.75rem 1rem;
    border-radius: 0 6px 6px 0;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: #94a3b8;
}

/* ── Turn-based clock widget ── */
.turn-clock {
    background: linear-gradient(135deg, #111827 0%, #0d1117 100%);
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    text-align: center;
}
.turn-clock .clock-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #00d4aa;
    letter-spacing: 0.05em;
    line-height: 1;
}
.turn-clock .clock-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}
.turn-clock .clock-turn {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 6px;
    border-top: 1px solid #1e293b;
    padding-top: 6px;
}

/* Turn log */
.turn-log-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #64748b;
    padding: 3px 0;
    border-bottom: 1px solid #0d1117;
}
.turn-log-item span.ts { color: #334155; }
.turn-log-item span.ev { color: #94a3b8; }
.turn-log-item span.pos { color: #00d4aa; }
.turn-log-item span.neg { color: #fb7185; }

.mono { font-family: 'JetBrains Mono', monospace; }
hr { border-color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PERSISTÊNCIA
# ════════════════════════════════════════════════════════════════════════════════
SAVE_FILE = "energy_trader_save.json"

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
        'meteo':         st.session_state.get('meteo', {}),
        # ── Turno ──
        'turno':         st.session_state.get('turno', 0),
        'game_datetime': st.session_state['game_datetime'].isoformat(),
        'turn_log':      st.session_state.get('turn_log', []),
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
    res   = m['reserv'][-1];  aflu = m['afluen'][-1]
    prec  = m['precip'][-1];  temp = m['temp'][-1]
    eol   = m['eolica'][-1];  sol  = m['solar'][-1]
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
    res  = meteo['reserv'][-1]; aflu = meteo['afluen'][-1]
    eol  = meteo['eolica'][-1]; temp = meteo['temp'][-1]
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

# ════════════════════════════════════════════════════════════════════════════════
# MOTOR DE TURNOS
# ════════════════════════════════════════════════════════════════════════════════
HOURS_PER_TURN = 1          # cada turno avança 1 hora
METEO_UPDATE_HOURS = 24     # meteo atualiza a cada 24h de jogo
PLD_UPDATE_HOURS   = 6      # PLD atualiza a cada 6h de jogo (4×/dia)

def _avancar_turno():
    """Avança o clock de jogo em 1 hora e processa todos os efeitos do turno."""
    # ── Avança clock ──────────────────────────────────────────────────────────
    old_dt: datetime = st.session_state['game_datetime']
    new_dt = old_dt + timedelta(hours=HOURS_PER_TURN)
    st.session_state['game_datetime'] = new_dt
    st.session_state['turno'] += 1
    turno = st.session_state['turno']

    eventos = []

    # ── Atualiza PLD a cada PLD_UPDATE_HOURS ──────────────────────────────────
    if turno % PLD_UPDATE_HOURS == 0:
        fator_meteo, _ = _impacto_meteo_no_pld(st.session_state['meteo'])
        ruido = random.gauss(0, 8)
        pld_medio = st.session_state['pld_historico']['PLD (R$/MWh)'].mean()
        pressao = (pld_medio * fator_meteo - st.session_state['pld_atual']) * 0.06
        novo_pld = max(30, min(500, st.session_state['pld_atual'] + ruido + pressao))
        delta_pld = novo_pld - st.session_state['pld_atual']
        st.session_state['pld_atual'] = round(novo_pld, 2)
        nova_linha = pd.DataFrame({
            'Data': [new_dt.date()],
            'PLD (R$/MWh)': [round(novo_pld, 2)]
        })
        st.session_state['pld_historico'] = pd.concat(
            [st.session_state['pld_historico'], nova_linha], ignore_index=True
        )
        sinal = "pos" if delta_pld >= 0 else "neg"
        eventos.append(f'<span class="ev">PLD atualizado →</span> <span class="{sinal}">R$ {novo_pld:.2f} ({delta_pld:+.2f})</span>')

    # ── Atualiza meteo a cada METEO_UPDATE_HOURS ──────────────────────────────
    if turno % METEO_UPDATE_HOURS == 0:
        _atualizar_meteo(new_dt)
        meteo = st.session_state['meteo']
        res = meteo['reserv'][-1]
        eventos.append(f'<span class="ev">Meteo atualizado · Reserv.</span> <span class="{"neg" if res < 40 else "pos"}">{res:.0f}%</span>')

    # ── Recalcula PnL de todos os contratos ───────────────────────────────────
    for c in st.session_state['contratos']:
        _recalc_pnl(c)

    # ── Registra no log de turnos ─────────────────────────────────────────────
    log = st.session_state.get('turn_log', [])
    ts_str = new_dt.strftime('%d/%m %H:%M')
    if eventos:
        for ev in eventos:
            log.append(f'<span class="ts">[{ts_str}]</span> {ev}')
    else:
        log.append(f'<span class="ts">[{ts_str}]</span> <span class="ev">Turno {turno} — mercado estável</span>')
    # mantém só os últimos 40 eventos
    st.session_state['turn_log'] = log[-40:]

    salvar_estado()

# ════════════════════════════════════════════════════════════════════════════════
# ESTADO INICIAL
# ════════════════════════════════════════════════════════════════════════════════
if 'estado_carregado' not in st.session_state:
    salvo = carregar_estado()

    if salvo:
        datas = [date.fromisoformat(d) for d in salvo['pld_historico']['datas']]
        st.session_state['pld_historico'] = pd.DataFrame({
            'Data': datas, 'PLD (R$/MWh)': salvo['pld_historico']['plds'],
        })
        st.session_state['pld_atual']   = salvo['pld_atual']
        st.session_state['saldo_caixa'] = salvo['saldo_caixa']
        st.session_state['pagina']      = salvo.get('pagina', 'mercado')
        st.session_state['contratos']   = [_desserializar_contrato(c) for c in salvo['contratos']]
        st.session_state['meteo']       = salvo.get('meteo') or _gerar_meteo_inicial()
        st.session_state['turno']       = salvo.get('turno', 0)
        st.session_state['turn_log']    = salvo.get('turn_log', [])
        gdt = salvo.get('game_datetime')
        st.session_state['game_datetime'] = (
            datetime.fromisoformat(gdt) if gdt
            else datetime.now().replace(minute=0, second=0, microsecond=0)
        )
    else:
        st.session_state['contratos']     = []
        st.session_state['saldo_caixa']   = 0.0
        st.session_state['pagina']        = 'mercado'
        st.session_state['turno']         = 0
        st.session_state['turn_log']      = []
        st.session_state['game_datetime'] = datetime.now().replace(minute=0, second=0, microsecond=0)

        base_date = date.today().replace(day=1)
        datas = [base_date - relativedelta(months=i) for i in range(23, -1, -1)]
        plds, pld_v = [], 80.0
        for _ in datas:
            pld_v = max(30, min(500, pld_v + random.gauss(0, 15)))
            plds.append(round(pld_v, 2))
        st.session_state['pld_historico'] = pd.DataFrame({'Data': datas, 'PLD (R$/MWh)': plds})
        st.session_state['pld_atual']     = st.session_state['pld_historico']['PLD (R$/MWh)'].iloc[-1]
        st.session_state['meteo']         = _gerar_meteo_inicial()

    st.session_state['estado_carregado'] = True

# ════════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════════
def _recalc_pnl(contrato):
    pld = st.session_state['pld_atual']
    vol = contrato['volume_mw'] * contrato['horas']
    if contrato['tipo'] == 'Compra':
        contrato['pnl_atual'] = (pld - contrato['preco']) * vol
    else:
        contrato['pnl_atual'] = (contrato['preco'] - pld) * vol

def _cor_pnl(v):
    return "#00d4aa" if v >= 0 else "#fb7185"

def _fmt_brl(v):
    return f"{'+'if v>=0 else ''}R$ {v:,.2f}"

SUBM = {"SE/CO": 1.0, "S": 0.95, "NE": 1.05, "N": 1.10}
TIPOS_ENERGIA = ["Convencional", "Incentivada 50%", "Incentivada 100%"]
INDICES = ["Preço Fixo", "PLD Spot", "PLD Médio Mensal", "IPCA + Spread", "IGP-M + Spread"]

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 0.75rem;'>
        <div style='font-family: Syne, sans-serif; font-size: 1.2rem; font-weight: 800;
                    color: #00d4aa; letter-spacing: -0.02em;'>⚡ EnergyTrader</div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.65rem;
                    color: #475569; text-transform: uppercase; letter-spacing: 0.1em;
                    margin-top: 2px;'>Simulador · Mercado Livre</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Relógio do jogo ───────────────────────────────────────────────────────
    gdt: datetime = st.session_state['game_datetime']
    turno = st.session_state['turno']

    DIAS_PT = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]
    MESES_PT = ["","Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    dia_semana = DIAS_PT[gdt.weekday()]
    mes_str    = MESES_PT[gdt.month]

    st.markdown(f"""
    <div class='turn-clock'>
        <div class='clock-time'>{gdt.strftime('%H:%M')}</div>
        <div class='clock-date'>{dia_semana}, {gdt.day} {mes_str} {gdt.year}</div>
        <div class='clock-turn'>Turno #{turno} · +{HOURS_PER_TURN}h por avanço</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Botão central: AVANÇAR TURNO ─────────────────────────────────────────
    if st.button("⏩  AVANÇAR TURNO  (+1h)", use_container_width=True, type="primary"):
        _avancar_turno()
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── PLD + stats portfólio ─────────────────────────────────────────────────
    pld = st.session_state['pld_atual']
    st.markdown(f"""
    <div style='background:#111827; border:1px solid #1e293b; border-radius:6px;
                padding: 0.75rem 1rem; margin-bottom: 0.75rem;'>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.6rem;
                    color: #475569; text-transform: uppercase; letter-spacing: 0.1em;'>
            PLD Atual (SE/CO)
        </div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 1.4rem;
                    font-weight: 700; color: #00d4aa; margin-top: 4px;'>
            R$ {pld:.2f}
        </div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.65rem;
                    color: #475569;'>R$/MWh · atualiza cada {PLD_UPDATE_HOURS}h</div>
    </div>
    """, unsafe_allow_html=True)

    n_contratos = len(st.session_state['contratos'])
    pnl_total   = sum(c.get('pnl_atual', 0) for c in st.session_state['contratos'])
    st.markdown(f"""
    <div style='display: flex; gap: 8px; margin-bottom: 0.75rem;'>
        <div style='flex:1; background:#111827; border:1px solid #1e293b; border-radius:6px; padding:0.6rem 0.75rem;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.55rem; color:#475569; text-transform:uppercase;'>Contratos</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.1rem; font-weight:700; color:#e2e8f0;'>{n_contratos}</div>
        </div>
        <div style='flex:1; background:#111827; border:1px solid #1e293b; border-radius:6px; padding:0.6rem 0.75rem;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.55rem; color:#475569; text-transform:uppercase;'>PnL Total</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.1rem; font-weight:700;
                        color:{"#00d4aa" if pnl_total >= 0 else "#fb7185"}'>
                {"+" if pnl_total >= 0 else ""}R${pnl_total/1000:.1f}k
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Navegação ─────────────────────────────────────────────────────────────
    def nav(label, key):
        ativo = st.session_state['pagina'] == key
        style = "color: #00d4aa; font-weight: 700;" if ativo else ""
        st.markdown(f"<div style='{style}'>", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state['pagina'] = key
            salvar_estado()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    nav("📊  Painel de Mercado",  "mercado")
    nav("🌦️  Meteorologia",       "meteo")
    nav("📋  Novo Contrato",      "novo_contrato")
    nav("💼  Meu Portfólio",      "portfolio")
    nav("💰  PnL & Resultado",    "pnl")
    nav("📜  Log de Turnos",      "log")
    nav("📚  Glossário",          "glossario")

    st.markdown("<hr>", unsafe_allow_html=True)

    col_save, col_reset = st.columns(2)
    with col_save:
        if st.button("💾  Salvar", use_container_width=True):
            salvar_estado()
            st.toast("✅ Progresso salvo!", icon="💾")
    with col_reset:
        if st.button("🗑️  Resetar", use_container_width=True):
            st.session_state['confirmar_reset'] = True

    if st.session_state.get('confirmar_reset'):
        st.markdown("""
        <div style='background:rgba(251,113,133,0.08); border:1px solid rgba(251,113,133,0.3);
                    border-radius:6px; padding:0.6rem 0.75rem; margin-top:0.25rem;
                    font-family:JetBrains Mono,monospace; font-size:0.72rem; color:#fb7185;'>
            Tem certeza? Apaga todos os dados.
        </div>
        """, unsafe_allow_html=True)
        col_sim, col_nao = st.columns(2)
        with col_sim:
            if st.button("Sim", key="reset_sim", use_container_width=True):
                resetar_estado(); st.rerun()
        with col_nao:
            if st.button("Não", key="reset_nao", use_container_width=True):
                st.session_state['confirmar_reset'] = False; st.rerun()

    if os.path.exists(SAVE_FILE):
        mtime = datetime.fromtimestamp(os.path.getmtime(SAVE_FILE))
        st.markdown(f"""
        <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem;
                    color:#334155; text-align:center; margin-top:0.4rem;'>
            último save {mtime.strftime('%d/%m %H:%M')}
        </div>
        """, unsafe_allow_html=True)

pagina = st.session_state['pagina']

# ════════════════════════════════════════════════════════════════════════════════
# PAINEL DE MERCADO
# ════════════════════════════════════════════════════════════════════════════════
if pagina == 'mercado':
    gdt = st.session_state['game_datetime']
    st.markdown("# 📊 Painel de Mercado")
    st.markdown(f"<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Data/hora do jogo: <b style='color:#00d4aa'>{gdt.strftime('%d/%m/%Y %H:%M')}</b> · Turno #{st.session_state['turno']}</p>", unsafe_allow_html=True)
    st.markdown("---")

    pld     = st.session_state['pld_atual']
    df_hist = st.session_state['pld_historico']
    var_pld = pld - df_hist['PLD (R$/MWh)'].iloc[-2] if len(df_hist) > 1 else 0

    fator_meteo, alertas = _impacto_meteo_no_pld(st.session_state['meteo'])
    for icone, tipo, msg in alertas[:3]:
        box_class = "danger-box" if tipo == "danger" else "warn-box" if tipo == "warn" else "info-box"
        st.markdown(f"<div class='{box_class}'>{icone} {msg}</div>", unsafe_allow_html=True)

    st.markdown("")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PLD SE/CO", f"R$ {pld:.2f}", f"{var_pld:+.2f} R$/MWh")
    c2.metric("PLD Sul",   f"R$ {pld*SUBM['S']:.2f}",  "−5% SE/CO")
    c3.metric("PLD NE",    f"R$ {pld*SUBM['NE']:.2f}", "+5% SE/CO")
    c4.metric("PLD Norte", f"R$ {pld*SUBM['N']:.2f}",  "+10% SE/CO")

    st.markdown("")
    col_graf, col_info = st.columns([3, 1])

    with col_graf:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_hist['Data'].astype(str), y=df_hist['PLD (R$/MWh)'],
            mode='lines', line=dict(color='#00d4aa', width=2),
            fill='tozeroy', fillcolor='rgba(0,212,170,0.07)',
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
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#475569; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;'>Estatísticas (24m)</div>", unsafe_allow_html=True)
        stats = {
            "Mínimo": df_hist['PLD (R$/MWh)'].min(),
            "Máximo": df_hist['PLD (R$/MWh)'].max(),
            "Média":  df_hist['PLD (R$/MWh)'].mean(),
            "Desvio": df_hist['PLD (R$/MWh)'].std(),
        }
        for k, v in stats.items():
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; padding:4px 0;
                        border-bottom:1px solid #1e293b; font-family:JetBrains Mono,monospace; font-size:0.8rem;'>
                <span style='color:#64748b;'>{k}</span>
                <span style='color:#e2e8f0;'>R$ {v:.2f}</span>
            </div>""", unsafe_allow_html=True)
        cor_fator = "#00d4aa" if fator_meteo <= 1.0 else "#fbbf24" if fator_meteo <= 1.2 else "#fb7185"
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; padding:6px 0 0 0;
                    font-family:JetBrains Mono,monospace; font-size:0.8rem;'>
            <span style='color:#64748b;'>Pressão Meteo</span>
            <span style='color:{cor_fator}; font-weight:700;'>{fator_meteo:.2f}×</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔢 Calculadora Rápida de Exposição")
    cc1, cc2, cc3 = st.columns(3)
    with cc1: vol_calc  = st.number_input("Volume (MW médio)", min_value=0.1, value=5.0, step=0.5)
    with cc2: preco_calc = st.number_input("Preço Contratado (R$/MWh)", min_value=0.0, value=float(round(pld,0)), step=1.0)
    with cc3: horas_calc = st.number_input("Horas do período", min_value=1, value=720, step=24)
    vol_total = vol_calc * horas_calc
    exposicao = (pld - preco_calc) * vol_total
    st.markdown(f"""
    <div style='display:flex; gap:1rem; margin-top:0.5rem;'>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#475569; text-transform:uppercase;'>Volume Total</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.3rem; font-weight:700; color:#e2e8f0;'>{vol_total:,.0f} MWh</div>
        </div>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#475569; text-transform:uppercase;'>PnL se comprado</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.3rem; font-weight:700; color:{_cor_pnl(exposicao)};'>{_fmt_brl(exposicao)}</div>
        </div>
        <div class='card' style='flex:1;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#475569; text-transform:uppercase;'>PnL se vendido</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.3rem; font-weight:700; color:{_cor_pnl(-exposicao)};'>{_fmt_brl(-exposicao)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# METEOROLOGIA
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'meteo':
    gdt = st.session_state['game_datetime']
    st.markdown("# 🌦️ Meteorologia & Hidrologia")
    st.markdown(f"<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Condições climáticas · Data do jogo: <b style='color:#00d4aa'>{gdt.strftime('%d/%m/%Y %H:%M')}</b></p>", unsafe_allow_html=True)
    st.markdown("---")

    meteo = st.session_state['meteo']
    datas_str = meteo['datas']
    fator_meteo, alertas = _impacto_meteo_no_pld(meteo)

    if alertas:
        st.markdown("#### 🔔 Alertas do Sistema")
        for icone, tipo, msg in alertas:
            box_class = "danger-box" if tipo=="danger" else "warn-box" if tipo=="warn" else "info-box"
            st.markdown(f"<div class='{box_class}'>{icone} {msg}</div>", unsafe_allow_html=True)
        st.markdown("")

    st.markdown("#### 📡 Condições Atuais")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    res_atual  = meteo['reserv'][-1]; aflu_atual = meteo['afluen'][-1]
    prec_atual = meteo['precip'][-1]; temp_atual = meteo['temp'][-1]
    eol_atual  = meteo['eolica'][-1]; sol_atual  = meteo['solar'][-1]
    res_prev  = meteo['reserv'][-2]  if len(meteo['reserv'])  > 1 else res_atual
    aflu_prev = meteo['afluen'][-2]  if len(meteo['afluen'])  > 1 else aflu_atual
    eol_prev  = meteo['eolica'][-2]  if len(meteo['eolica'])  > 1 else eol_atual
    m1.metric("Reservatório SE/CO", f"{res_atual:.0f}%",  f"{res_atual-res_prev:+.1f}%")
    m2.metric("Afluência (% MLT)",  f"{aflu_atual:.0f}%", f"{aflu_atual-aflu_prev:+.1f}%")
    m3.metric("Precipitação",       f"{prec_atual:.0f} mm")
    m4.metric("Temperatura SE/CO",  f"{temp_atual:.1f}°C")
    m5.metric("Geração Eólica NE",  f"{eol_atual:.0f}%",  f"{eol_atual-eol_prev:+.1f}%")
    m6.metric("Geração Solar",      f"{sol_atual:.0f}%")

    cor_fator   = "#00d4aa" if fator_meteo <= 1.0 else "#fbbf24" if fator_meteo <= 1.2 else "#fb7185"
    label_fator = "Baixa pressão" if fator_meteo <= 1.0 else "Pressão moderada" if fator_meteo <= 1.2 else "Alta pressão"
    proxima_att = METEO_UPDATE_HOURS - (st.session_state['turno'] % METEO_UPDATE_HOURS)
    st.markdown(f"""
    <div style='background:#111827; border:1px solid #1e293b; border-radius:8px;
                padding:1rem 1.5rem; margin-top:1rem; display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#475569; text-transform:uppercase; letter-spacing:0.1em;'>
                Fator de Pressão Meteorológica sobre o PLD
            </div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.82rem; color:#94a3b8; margin-top:2px;'>
                Reflete o impacto combinado das condições climáticas na tendência do PLD
            </div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#334155; margin-top:4px;'>
                Próxima atualização: <b style='color:#475569'>{proxima_att}h</b> de jogo
            </div>
        </div>
        <div style='text-align:right;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:2rem; font-weight:700; color:{cor_fator};'>{fator_meteo:.2f}×</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:{cor_fator};'>{label_fator}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📈 Histórico (série completa)")

    tab1, tab2, tab3 = st.tabs(["💧 Hidrologia", "🌡️ Clima", "⚡ Renováveis"])

    def _layout_fig():
        return dict(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569'),
            yaxis=dict(gridcolor='#1e293b', color='#475569'),
            margin=dict(l=10, r=10, t=30, b=10), height=260,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8'))
        )

    with tab1:
        fig_hid = go.Figure()
        fig_hid.add_trace(go.Scatter(
            x=datas_str, y=meteo['reserv'], mode='lines', name='Reservatório SE/CO (%)',
            line=dict(color='#60a5fa', width=2), fill='tozeroy', fillcolor='rgba(96,165,250,0.08)',
            hovertemplate='%{x}<br>Reservatório: %{y:.1f}%<extra></extra>'
        ))
        fig_hid.add_hline(y=40, line_color='#fbbf24', line_dash='dash', annotation_text='Atenção (40%)', annotation_font_color='#fbbf24')
        fig_hid.add_hline(y=20, line_color='#fb7185', line_dash='dash', annotation_text='Crítico (20%)',  annotation_font_color='#fb7185')
        lay = _layout_fig(); lay['yaxis']['range'] = [0,105]; lay['yaxis']['title'] = '%'
        fig_hid.update_layout(**lay)

        fig_aflu = go.Figure()
        fig_aflu.add_trace(go.Bar(
            x=datas_str, y=meteo['afluen'], name='Afluência (% MLT)',
            marker_color=['#fb7185' if v<50 else '#fbbf24' if v<80 else '#00d4aa' for v in meteo['afluen']],
            hovertemplate='%{x}<br>Afluência: %{y:.1f}% MLT<extra></extra>'
        ))
        fig_aflu.add_hline(y=100, line_color='#475569', line_dash='dash', annotation_text='MLT (100%)', annotation_font_color='#475569')
        lay2 = _layout_fig(); lay2['yaxis']['title'] = '% MLT'
        fig_aflu.update_layout(**lay2)

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("<div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#475569; text-transform:uppercase; margin-bottom:4px;'>Nível dos Reservatórios</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_hid, use_container_width=True)
        with col_h2:
            st.markdown("<div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#475569; text-transform:uppercase; margin-bottom:4px;'>Afluência Natural (% da MLT)</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_aflu, use_container_width=True)

        st.markdown("<div class='info-box'>💡 <b>Como interpretar:</b> Reservatório abaixo de 40% e afluência abaixo da MLT (100%) são os principais sinais de alerta para alta do PLD.</div>", unsafe_allow_html=True)

    with tab2:
        fig_prec = go.Figure()
        fig_prec.add_trace(go.Bar(
            x=datas_str, y=meteo['precip'], name='Precipitação (mm)',
            marker_color='rgba(96,165,250,0.7)',
            hovertemplate='%{x}<br>Precipitação: %{y:.0f} mm<extra></extra>'
        ))
        lay3 = _layout_fig(); lay3['yaxis']['title'] = 'mm/mês'
        fig_prec.update_layout(**lay3)

        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=datas_str, y=meteo['temp'], mode='lines+markers',
            line=dict(color='#f59e0b', width=2), marker=dict(size=4, color='#f59e0b'),
            hovertemplate='%{x}<br>Temperatura: %{y:.1f}°C<extra></extra>'
        ))
        fig_temp.add_hline(y=30, line_color='#fb7185', line_dash='dash', annotation_text='Calor extremo (30°C)', annotation_font_color='#fb7185')
        lay4 = _layout_fig(); lay4['yaxis']['title'] = '°C'
        fig_temp.update_layout(**lay4)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("<div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#475569; text-transform:uppercase; margin-bottom:4px;'>Precipitação SE/CO</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_prec, use_container_width=True)
        with col_c2:
            st.markdown("<div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#475569; text-transform:uppercase; margin-bottom:4px;'>Temperatura Média SE/CO</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_temp, use_container_width=True)

        st.markdown("<div class='info-box'>💡 <b>Como interpretar:</b> Precipitação baixa por vários meses consecutivos é sinal de risco hídrico. Temperaturas acima de 30°C aumentam a demanda de climatização.</div>", unsafe_allow_html=True)

    with tab3:
        fig_eol = go.Figure()
        fig_eol.add_trace(go.Scatter(
            x=datas_str, y=meteo['eolica'], mode='lines', name='Eólica NE (%)',
            line=dict(color='#a78bfa', width=2), fill='tozeroy', fillcolor='rgba(167,139,250,0.08)',
            hovertemplate='%{x}<br>Eólica: %{y:.1f}%<extra></extra>'
        ))
        lay5 = _layout_fig(); lay5['yaxis']['range'] = [0,105]; lay5['yaxis']['title'] = '% capacidade'
        fig_eol.update_layout(**lay5)

        fig_sol = go.Figure()
        fig_sol.add_trace(go.Scatter(
            x=datas_str, y=meteo['solar'], mode='lines', name='Solar (%)',
            line=dict(color='#f59e0b', width=2), fill='tozeroy', fillcolor='rgba(245,158,11,0.08)',
            hovertemplate='%{x}<br>Solar: %{y:.1f}%<extra></extra>'
        ))
        lay6 = _layout_fig(); lay6['yaxis']['range'] = [0,105]; lay6['yaxis']['title'] = '% capacidade'
        fig_sol.update_layout(**lay6)

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown("<div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#475569; text-transform:uppercase; margin-bottom:4px;'>Fator de Capacidade Eólica (NE)</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_eol, use_container_width=True)
        with col_r2:
            st.markdown("<div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#475569; text-transform:uppercase; margin-bottom:4px;'>Fator de Capacidade Solar</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_sol, use_container_width=True)

        st.markdown("<div class='info-box'>💡 <b>Como interpretar:</b> Alta geração eólica e solar reduz a necessidade de despacho termelétrico, aliviando o CMO e pressionando o PLD para baixo.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔗 Matriz de Impacto no PLD")
    st.markdown("""
    <div style='overflow-x:auto;'>
    <table style='width:100%; border-collapse:collapse; font-family:JetBrains Mono,monospace; font-size:0.8rem;'>
      <thead>
        <tr style='background:#111827; color:#64748b; text-transform:uppercase; font-size:0.65rem; letter-spacing:0.05em;'>
          <th style='padding:8px 12px; text-align:left; border-bottom:1px solid #1e293b;'>Variável</th>
          <th style='padding:8px 12px; text-align:center; border-bottom:1px solid #1e293b;'>Quando SOBE</th>
          <th style='padding:8px 12px; text-align:center; border-bottom:1px solid #1e293b;'>Impacto no PLD</th>
          <th style='padding:8px 12px; text-align:center; border-bottom:1px solid #1e293b;'>Quando CAI</th>
          <th style='padding:8px 12px; text-align:center; border-bottom:1px solid #1e293b;'>Impacto no PLD</th>
          <th style='padding:8px 12px; text-align:left; border-bottom:1px solid #1e293b;'>Intensidade</th>
        </tr>
      </thead>
      <tbody>
        <tr style='border-bottom:1px solid #1e293b;'>
          <td style='padding:8px 12px; color:#e2e8f0;'>💧 Reservatório</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Nível sobe</td>
          <td style='padding:8px 12px; text-align:center; color:#00d4aa; font-weight:700;'>↓ Baixa</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Nível cai</td>
          <td style='padding:8px 12px; text-align:center; color:#fb7185; font-weight:700;'>↑ Sobe forte</td>
          <td style='padding:8px 12px; color:#f59e0b;'>★★★★★ Crítica</td>
        </tr>
        <tr style='border-bottom:1px solid #1e293b; background:rgba(255,255,255,0.01);'>
          <td style='padding:8px 12px; color:#e2e8f0;'>🌧️ Afluência</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Acima MLT</td>
          <td style='padding:8px 12px; text-align:center; color:#00d4aa; font-weight:700;'>↓ Baixa</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Abaixo MLT</td>
          <td style='padding:8px 12px; text-align:center; color:#fb7185; font-weight:700;'>↑ Sobe forte</td>
          <td style='padding:8px 12px; color:#f59e0b;'>★★★★★ Crítica</td>
        </tr>
        <tr style='border-bottom:1px solid #1e293b;'>
          <td style='padding:8px 12px; color:#e2e8f0;'>🌡️ Temperatura</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Onda de calor</td>
          <td style='padding:8px 12px; text-align:center; color:#fb7185; font-weight:700;'>↑ Sobe</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Temperatura amena</td>
          <td style='padding:8px 12px; text-align:center; color:#00d4aa; font-weight:700;'>↓ Leve baixa</td>
          <td style='padding:8px 12px; color:#94a3b8;'>★★★☆☆ Moderada</td>
        </tr>
        <tr style='border-bottom:1px solid #1e293b; background:rgba(255,255,255,0.01);'>
          <td style='padding:8px 12px; color:#e2e8f0;'>💨 Eólica NE</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Vento forte</td>
          <td style='padding:8px 12px; text-align:center; color:#00d4aa; font-weight:700;'>↓ Baixa</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Vento fraco</td>
          <td style='padding:8px 12px; text-align:center; color:#fbbf24; font-weight:700;'>↑ Leve alta</td>
          <td style='padding:8px 12px; color:#94a3b8;'>★★★☆☆ Moderada</td>
        </tr>
        <tr style='border-bottom:1px solid #1e293b;'>
          <td style='padding:8px 12px; color:#e2e8f0;'>☀️ Solar</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Alta irradiação</td>
          <td style='padding:8px 12px; text-align:center; color:#00d4aa; font-weight:700;'>↓ Baixa leve</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Dias nublados</td>
          <td style='padding:8px 12px; text-align:center; color:#fbbf24; font-weight:700;'>↑ Leve alta</td>
          <td style='padding:8px 12px; color:#94a3b8;'>★★☆☆☆ Baixa</td>
        </tr>
        <tr>
          <td style='padding:8px 12px; color:#e2e8f0;'>🌧️ Precipitação</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Chuvas fortes</td>
          <td style='padding:8px 12px; text-align:center; color:#00d4aa; font-weight:700;'>↓ Baixa (futuro)</td>
          <td style='padding:8px 12px; text-align:center; color:#94a3b8;'>Seca prolongada</td>
          <td style='padding:8px 12px; text-align:center; color:#fb7185; font-weight:700;'>↑ Sobe (futuro)</td>
          <td style='padding:8px 12px; color:#fbbf24;'>★★★★☆ Alta</td>
        </tr>
      </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# NOVO CONTRATO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'novo_contrato':
    gdt = st.session_state['game_datetime']
    st.markdown("# 📋 Novo Contrato")
    st.markdown(f"<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Monte e registre um contrato bilateral · Data do jogo: <b style='color:#00d4aa'>{gdt.strftime('%d/%m/%Y %H:%M')}</b></p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<div class='info-box'>💡 <b>Como funciona:</b> Um contrato bilateral é um acordo entre comprador e vendedor com preço, volume e período definidos. O simulador calculará seu PnL comparando o preço acordado com o PLD atual.</div>", unsafe_allow_html=True)

    fator_meteo, alertas = _impacto_meteo_no_pld(st.session_state['meteo'])
    if fator_meteo > 1.15:
        st.markdown(f"<div class='warn-box'>⚠️ <b>Atenção:</b> Condições meteorológicas indicam pressão de alta no PLD (fator {fator_meteo:.2f}×). Considere o impacto ao definir o preço do contrato.</div>", unsafe_allow_html=True)
    elif fator_meteo < 0.95:
        st.markdown(f"<div class='info-box'>✅ <b>Condições favoráveis:</b> Fatores climáticos sugerem pressão de baixa no PLD (fator {fator_meteo:.2f}×). Bom momento para analisar contratos de venda.</div>", unsafe_allow_html=True)

    with st.form("form_contrato"):
        st.markdown("#### Identificação")
        col1, col2 = st.columns(2)
        with col1: nome_contrato = st.text_input("Nome / Referência do Contrato", placeholder="ex: CONTRATO-001")
        with col2: contraparte   = st.text_input("Contraparte", placeholder="ex: Geradora Solar ABC")

        st.markdown("#### Operação")
        col3, col4, col5 = st.columns(3)
        with col3: tipo_op      = st.selectbox("Tipo de Operação", ["Compra", "Venda"])
        with col4: submercado   = st.selectbox("Submercado", list(SUBM.keys()))
        with col5: tipo_energia = st.selectbox("Tipo de Energia", TIPOS_ENERGIA)

        st.markdown("#### Preço e Volume")
        col6, col7, col8 = st.columns(3)
        with col6: preco     = st.number_input("Preço (R$/MWh)", min_value=0.01, value=float(round(st.session_state['pld_atual'],0)), step=1.0)
        with col7: volume_mw = st.number_input("Volume (MW médio)", min_value=0.1, value=1.0, step=0.5)
        with col8: indice    = st.selectbox("Índice de Reajuste", INDICES)

        st.markdown("#### Vigência")
        col9, col10 = st.columns(2)
        with col9:  data_inicio = st.date_input("Data de Início", value=gdt.date().replace(day=1))
        with col10: data_fim    = st.date_input("Data de Fim",    value=gdt.date().replace(day=1) + relativedelta(months=11))

        st.markdown("#### Gross-up")
        col11, col12 = st.columns(2)
        with col11: gross_up = st.checkbox("Aplicar Gross-up de PIS/COFINS (9,25%)", value=False)
        with col12: flag_pc  = st.checkbox("Marcar flag P/C na boleta", value=False)

        obs = st.text_area("Observações", placeholder="Notas adicionais...", height=80)
        submitted = st.form_submit_button("✅  REGISTRAR CONTRATO", type="primary", use_container_width=True)

    if submitted:
        if not nome_contrato:
            st.error("⚠️ Informe o nome do contrato.")
        elif data_fim <= data_inicio:
            st.error("⚠️ A data de fim deve ser posterior à data de início.")
        else:
            horas     = int((data_fim - data_inicio).days * 24)
            preco_adj = preco * 1.0925 if gross_up else preco
            novo = {
                'id': len(st.session_state['contratos']) + 1,
                'nome': nome_contrato, 'contraparte': contraparte,
                'tipo': tipo_op, 'submercado': submercado, 'tipo_energia': tipo_energia,
                'preco': preco_adj, 'preco_orig': preco, 'volume_mw': volume_mw,
                'indice': indice, 'data_inicio': data_inicio, 'data_fim': data_fim,
                'horas': horas, 'gross_up': gross_up, 'flag_pc': flag_pc,
                'obs': obs, 'pnl_atual': 0.0, 'criado_em': datetime.now(),
            }
            _recalc_pnl(novo)
            st.session_state['contratos'].append(novo)
            salvar_estado()
            vol_total_mwh = volume_mw * horas
            receita_bruta = preco_adj * vol_total_mwh
            st.success(f"✅ Contrato **{nome_contrato}** registrado!")
            st.markdown(f"""
            <div style='display:flex; gap:1rem; margin-top:0.5rem;'>
                <div class='card' style='flex:1;'>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem; color:#475569; text-transform:uppercase;'>Volume Total</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.2rem; font-weight:700; color:#e2e8f0;'>{vol_total_mwh:,.0f} MWh</div>
                </div>
                <div class='card' style='flex:1;'>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem; color:#475569; text-transform:uppercase;'>Receita Bruta</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.2rem; font-weight:700; color:#e2e8f0;'>R$ {receita_bruta:,.2f}</div>
                </div>
                <div class='card' style='flex:1;'>
                    <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem; color:#475569; text-transform:uppercase;'>PnL vs PLD atual</div>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.2rem; font-weight:700; color:{_cor_pnl(novo["pnl_atual"])};'>{_fmt_brl(novo["pnl_atual"])}</div>
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
        st.markdown("<div class='warn-box'>⚠️ Nenhum contrato registrado ainda. Acesse <b>Novo Contrato</b> para começar a operar.</div>", unsafe_allow_html=True)
    else:
        contratos  = st.session_state['contratos']
        pos_compra = sum(c['volume_mw'] for c in contratos if c['tipo']=='Compra')
        pos_venda  = sum(c['volume_mw'] for c in contratos if c['tipo']=='Venda')
        pos_liq    = pos_compra - pos_venda

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Posição Comprada", f"{pos_compra:.1f} MW")
        m2.metric("Posição Vendida",  f"{pos_venda:.1f} MW")
        m3.metric("Posição Líquida",  f"{pos_liq:+.1f} MW", delta="Comprado" if pos_liq>0 else "Vendido" if pos_liq<0 else "Zerado")
        m4.metric("Contratos Ativos", len(contratos))
        st.markdown("")

        for c in contratos:
            tag_html = f"<span class='tag-{'compra' if c['tipo']=='Compra' else 'venda'}'>{c['tipo'].upper()}</span>"
            pnl_cor  = _cor_pnl(c['pnl_atual'])
            with st.expander(f"#{c['id']} — {c['nome']}  |  {c['volume_mw']} MW  |  R$ {c['preco']:.2f}/MWh", expanded=False):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.markdown(f"""<div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; line-height:2;'>
                        <b style='color:#64748b;'>Tipo:</b> {tag_html}<br>
                        <b style='color:#64748b;'>Contraparte:</b> <span style='color:#e2e8f0;'>{c['contraparte'] or '—'}</span><br>
                        <b style='color:#64748b;'>Submercado:</b> <span style='color:#e2e8f0;'>{c['submercado']}</span><br>
                        <b style='color:#64748b;'>Energia:</b> <span style='color:#e2e8f0;'>{c['tipo_energia']}</span>
                    </div>""", unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""<div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; line-height:2;'>
                        <b style='color:#64748b;'>Preço:</b> <span style='color:#e2e8f0;'>R$ {c['preco']:.2f}/MWh</span><br>
                        <b style='color:#64748b;'>Volume:</b> <span style='color:#e2e8f0;'>{c['volume_mw']} MW</span><br>
                        <b style='color:#64748b;'>Horas:</b> <span style='color:#e2e8f0;'>{c['horas']:,} h</span><br>
                        <b style='color:#64748b;'>Índice:</b> <span style='color:#e2e8f0;'>{c['indice']}</span>
                    </div>""", unsafe_allow_html=True)
                with col_c:
                    st.markdown(f"""<div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; line-height:2;'>
                        <b style='color:#64748b;'>Início:</b> <span style='color:#e2e8f0;'>{c['data_inicio']}</span><br>
                        <b style='color:#64748b;'>Fim:</b> <span style='color:#e2e8f0;'>{c['data_fim']}</span><br>
                        <b style='color:#64748b;'>Gross-up:</b> <span style='color:#e2e8f0;'>{'✓ 9,25%' if c['gross_up'] else '—'}</span><br>
                        <b style='color:#64748b;'>Flag P/C:</b> <span style='color:#e2e8f0;'>{'✓' if c['flag_pc'] else '—'}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='margin-top:0.75rem; padding:0.75rem 1rem; background:#0d1117;
                            border-radius:6px; display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#475569; text-transform:uppercase;'>PnL vs PLD Atual</span>
                    <span style='font-family:JetBrains Mono,monospace; font-size:1.1rem; font-weight:700; color:{pnl_cor};'>{_fmt_brl(c['pnl_atual'])}</span>
                </div>""", unsafe_allow_html=True)
                if c['obs']:
                    st.markdown(f"<div class='info-box'>📝 {c['obs']}</div>", unsafe_allow_html=True)
                if st.button(f"🗑️ Remover contrato #{c['id']}", key=f"del_{c['id']}"):
                    st.session_state['contratos'] = [x for x in st.session_state['contratos'] if x['id'] != c['id']]
                    salvar_estado(); st.rerun()

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
        pnl_total   = sum(c['pnl_atual'] for c in contratos)
        pnl_compras = sum(c['pnl_atual'] for c in contratos if c['tipo']=='Compra')
        pnl_vendas  = sum(c['pnl_atual'] for c in contratos if c['tipo']=='Venda')

        m1, m2, m3 = st.columns(3)
        m1.metric("PnL Total",   _fmt_brl(pnl_total),   delta=f"{'▲' if pnl_total>=0 else '▼'} vs PLD R${pld:.2f}")
        m2.metric("PnL Compras", _fmt_brl(pnl_compras))
        m3.metric("PnL Vendas",  _fmt_brl(pnl_vendas))
        st.markdown("")

        nomes = [c['nome'] for c in contratos]
        pnls  = [c['pnl_atual'] for c in contratos]
        cores = ['#00d4aa' if v>=0 else '#fb7185' for v in pnls]

        fig_bar = go.Figure(go.Bar(
            x=nomes, y=pnls, marker_color=cores,
            text=[_fmt_brl(v) for v in pnls], textposition='outside',
            textfont=dict(family='JetBrains Mono', size=11),
            hovertemplate='%{x}<br>PnL: R$ %{y:,.2f}<extra></extra>'
        ))
        fig_bar.add_shape(type='line', x0=-0.5, x1=len(nomes)-0.5, y0=0, y1=0, line=dict(color='#475569', width=1, dash='dash'))
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', color='#475569'),
            yaxis=dict(gridcolor='#1e293b', color='#475569', title='PnL (R$)'),
            margin=dict(l=10, r=10, t=40, b=10), height=320,
            font=dict(family='JetBrains Mono', size=11, color='#94a3b8'),
            title=dict(text='PnL por Contrato vs PLD Atual', font=dict(size=13, color='#94a3b8'))
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🔮 Simulador de Cenário")
        st.markdown("<div class='info-box'>Arraste o PLD hipotético para ver como seu portfólio se comportaria em diferentes cenários.</div>", unsafe_allow_html=True)

        pld_sim = st.slider("PLD Hipotético (R$/MWh)", min_value=30.0, max_value=500.0, value=float(round(pld,0)), step=5.0)
        pnl_sim_list = []
        for c in contratos:
            vol = c['volume_mw'] * c['horas']
            pnl_sim_list.append((pld_sim - c['preco'])*vol if c['tipo']=='Compra' else (c['preco']-pld_sim)*vol)

        pnl_sim_total = sum(pnl_sim_list)
        delta_cenario = pnl_sim_total - pnl_total

        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("PLD Hipotético",    f"R$ {pld_sim:.2f}/MWh", f"{pld_sim-pld:+.2f} vs atual")
        sc2.metric("PnL no Cenário",    _fmt_brl(pnl_sim_total))
        sc3.metric("Variação vs Atual", _fmt_brl(delta_cenario))

        pld_range = np.linspace(30, 500, 200)
        pnl_range = []
        for p in pld_range:
            s = sum((p-c['preco'])*c['volume_mw']*c['horas'] if c['tipo']=='Compra' else (c['preco']-p)*c['volume_mw']*c['horas'] for c in contratos)
            pnl_range.append(s)

        fig_sens = go.Figure()
        fig_sens.add_trace(go.Scatter(x=pld_range, y=pnl_range, mode='lines', line=dict(color='#00d4aa', width=2),
            fill='tozeroy', fillcolor='rgba(0,212,170,0.05)', name='PnL Portfólio',
            hovertemplate='PLD: R$ %{x:.0f}<br>PnL: R$ %{y:,.0f}<extra></extra>'))
        fig_sens.add_vline(x=pld, line_color='#94a3b8', line_dash='dash', annotation_text=f"PLD atual: R${pld:.0f}", annotation_font_color='#94a3b8')
        fig_sens.add_vline(x=pld_sim, line_color='#fbbf24', line_dash='dot', annotation_text=f"Cenário: R${pld_sim:.0f}", annotation_font_color='#fbbf24')
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

        st.markdown("---")
        st.markdown("#### 📊 Tabela Resumo")
        rows = []
        for c, pnl_s in zip(contratos, pnl_sim_list):
            rows.append({
                'Contrato': c['nome'], 'Tipo': c['tipo'], 'Submercado': c['submercado'],
                'Preço (R$/MWh)': f"{c['preco']:.2f}", 'Volume (MW)': c['volume_mw'],
                'PnL Atual (R$)': c['pnl_atual'], 'PnL Cenário (R$)': pnl_s,
            })
        df_res = pd.DataFrame(rows)
        st.dataframe(
            df_res.style
                .format({'PnL Atual (R$)': '{:,.2f}', 'PnL Cenário (R$)': '{:,.2f}'})
                .applymap(lambda v: f'color: {"#00d4aa" if v >= 0 else "#fb7185"}', subset=['PnL Atual (R$)', 'PnL Cenário (R$)'])
                .set_properties(**{'text-align': 'center', 'font-family': 'JetBrains Mono, monospace'})
                .set_table_styles([{'selector': 'th', 'props': [('font-weight','bold'),('text-align','center')]}]),
            use_container_width=True, hide_index=True
        )

# ════════════════════════════════════════════════════════════════════════════════
# LOG DE TURNOS
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'log':
    gdt = st.session_state['game_datetime']
    turno = st.session_state['turno']
    st.markdown("# 📜 Log de Turnos")
    st.markdown(f"<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Histórico de eventos do simulador · Turno <b style='color:#00d4aa'>#{turno}</b> · {gdt.strftime('%d/%m/%Y %H:%M')}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Linha do tempo resumida ───────────────────────────────────────────────
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Turnos Jogados",    turno)
    col_b.metric("Horas de Jogo",     turno * HOURS_PER_TURN)
    col_c.metric("Dias Simulados",    turno * HOURS_PER_TURN // 24)
    col_d.metric("Próx. PLD (h)",     PLD_UPDATE_HOURS - (turno % PLD_UPDATE_HOURS) if turno > 0 else PLD_UPDATE_HOURS)

    st.markdown("")
    st.markdown("#### 📋 Eventos Recentes")

    turn_log = st.session_state.get('turn_log', [])
    if not turn_log:
        st.markdown("<div class='warn-box'>⚠️ Nenhum turno avançado ainda. Use o botão <b>⏩ AVANÇAR TURNO</b> na barra lateral para começar.</div>", unsafe_allow_html=True)
    else:
        log_html = ""
        for item in reversed(turn_log):
            log_html += f"<div class='turn-log-item'>{item}</div>"
        st.markdown(f"""
        <div style='background:#0d1117; border:1px solid #1e293b; border-radius:8px;
                    padding:0.75rem 1rem; max-height:500px; overflow-y:auto;'>
            {log_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚙️ Configurações do Motor de Turnos")
    st.markdown(f"""
    <div style='display:flex; gap:1rem; flex-wrap:wrap;'>
        <div class='card' style='flex:1; min-width:180px;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem; color:#475569; text-transform:uppercase;'>Duração do Turno</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.4rem; font-weight:700; color:#00d4aa;'>{HOURS_PER_TURN}h</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#334155;'>por clique</div>
        </div>
        <div class='card' style='flex:1; min-width:180px;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem; color:#475569; text-transform:uppercase;'>Atualização PLD</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.4rem; font-weight:700; color:#60a5fa;'>cada {PLD_UPDATE_HOURS}h</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#334155;'>4× por dia simulado</div>
        </div>
        <div class='card' style='flex:1; min-width:180px;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem; color:#475569; text-transform:uppercase;'>Atualização Meteo</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.4rem; font-weight:700; color:#a78bfa;'>cada {METEO_UPDATE_HOURS}h</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#334155;'>1× por dia simulado</div>
        </div>
        <div class='card' style='flex:1; min-width:180px;'>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.6rem; color:#475569; text-transform:uppercase;'>Data de Início</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:1.0rem; font-weight:700; color:#e2e8f0;'>{(st.session_state["game_datetime"] - timedelta(hours=turno)).strftime("%d/%m/%Y %H:%M")}</div>
            <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#334155;'>origem da timeline</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# GLOSSÁRIO
# ════════════════════════════════════════════════════════════════════════════════
elif pagina == 'glossario':
    st.markdown("# 📚 Glossário")
    st.markdown("<p style='color:#475569; font-size:0.85rem; margin-top:-0.5rem;'>Conceitos essenciais do mercado livre de energia</p>", unsafe_allow_html=True)
    st.markdown("---")

    termos = [
        ("PLD — Preço de Liquidação das Diferenças",
         "Preço calculado semanalmente pela CCEE com base no Custo Marginal de Operação (CMO) do sistema elétrico. Reflete o custo de se produzir mais uma unidade de energia naquele momento. É o principal referencial de preço no mercado de curto prazo."),
        ("CMO — Custo Marginal de Operação",
         "Custo de se atender a mais uma unidade de demanda no sistema. Em períodos secos, com reservatórios baixos, o CMO sobe porque é necessário acionar termoelétricas mais caras. Em períodos úmidos, o CMO cai."),
        ("ACL — Ambiente de Contratação Livre",
         "Segmento do mercado onde consumidores com demanda acima de 500 kW podem comprar energia livremente de qualquer gerador ou comercializador, negociando preço, prazo e condições."),
        ("ACR — Ambiente de Contratação Regulada",
         "Segmento onde distribuidoras compram energia em leilões regulados pela ANEEL para atender consumidores cativos (residências, pequenas empresas etc.)."),
        ("Submercado",
         "O Brasil é dividido em 4 submercados: SE/CO (Sudeste/Centro-Oeste), S (Sul), NE (Nordeste) e N (Norte). Cada um tem seu próprio PLD, que pode diferir dos demais por conta de restrições de transmissão."),
        ("Afluência Natural",
         "Volume de água que chega naturalmente aos reservatórios das usinas hidrelétricas, expresso em % da MLT (Média de Longo Termo). Afluência acima de 100% indica condições hídricas favoráveis."),
        ("MLT — Média de Longo Termo",
         "Média histórica das afluências naturais dos reservatórios, calculada com base em séries de 70+ anos. É a referência para avaliar se um período hidrológico é seco ou úmido."),
        ("Reservatório EAR",
         "Energia Armazenável Real nos reservatórios das hidrelétricas, expressa em % da capacidade total. EAR abaixo de 20% configura estado de atenção; abaixo de 10%, estado crítico."),
        ("Posição Comprada (Long)",
         "Quando você comprou mais energia do que vendeu. Você se beneficia quando o PLD sobe acima do seu preço de compra, pois pode revender no spot com lucro."),
        ("Posição Vendida (Short)",
         "Quando você vendeu mais energia do que comprou. Você se beneficia quando o PLD cai abaixo do seu preço de venda."),
        ("Gross-up de PIS/COFINS",
         "Ajuste no preço da energia para embutir os impostos PIS/COFINS (alíquota de 9,25%). Fórmula: Preço Gross-up = Preço / (1 − 9,25%)."),
        ("Mark to Market (MtM)",
         "Reavaliação dos contratos a preços de mercado correntes (PLD atual). O PnL MtM mostra quanto você ganharia ou perderia se liquidasse tudo hoje."),
        ("Contrato Bilateral",
         "Acordo direto entre duas partes (comprador e vendedor) fora do ambiente de leilão. Permite flexibilidade total na negociação de preço, prazo, volume e índice de reajuste."),
        ("Energia Incentivada",
         "Energia proveniente de fontes renováveis (solar, eólica, PCH, biomassa) que possui desconto de 50% ou 100% na TUSD/TUST. Consumidores que compram esse tipo de energia podem migrar ao ACL com demanda a partir de 500 kW (50%) ou 30 kW (100%)."),
        ("CCEE — Câmara de Comercialização de Energia Elétrica",
         "Entidade que administra o mercado de curto prazo (spot) no Brasil. Calcula e publica o PLD, realiza a liquidação financeira das diferenças entre o contratado e o consumido/gerado."),
        ("Fator de Capacidade",
         "Relação entre a geração efetiva de uma usina e sua capacidade instalada máxima, em %. Para eólica no NE, valores acima de 50% são considerados excelentes."),
        ("Delta",
         "Variação do PnL para uma variação unitária no PLD. Indica a sensibilidade do portfólio. Um delta positivo (posição comprada) significa que o portfólio ganha quando o PLD sobe."),
        ("Spread",
         "Diferença entre o preço de compra e o preço de venda. O lucro de um comercializador vem em parte desse spread entre o que paga ao gerador e o que cobra do consumidor."),
        ("Turno (Jogo)",
         f"Unidade de tempo do simulador. Cada turno avança {HOURS_PER_TURN} hora(s) no relógio do jogo. O PLD é recalculado a cada {PLD_UPDATE_HOURS} turnos; os dados meteorológicos, a cada {METEO_UPDATE_HOURS} turnos."),
    ]

    for termo, definicao in termos:
        with st.expander(f"📌 {termo}"):
            st.markdown(f"""
            <div style='font-family: Syne, sans-serif; font-size: 0.88rem; color: #94a3b8; line-height: 1.7; padding: 0.25rem 0;'>
                {definicao}
            </div>
            """, unsafe_allow_html=True)