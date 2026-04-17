import streamlit as st
import requests
import time
from datetime import datetime

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Núi Lửa FPL 🌋",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

/* Dark background */
.stApp { background-color: #1a1a2e; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #16213e;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
[data-testid="metric-container"] label {
    color: #aaaaaa !important;
    font-size: 11px !important;
    font-family: 'Space Mono', monospace !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f0f0f0 !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
    background: #16213e !important;
    border-bottom: 1px solid rgba(255,69,0,0.3) !important;
    gap: 4px;
}
[data-baseweb="tab"] {
    color: #aaaaaa !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border-bottom: 3px solid transparent !important;
}
[aria-selected="true"] {
    color: #ff4500 !important;
    border-bottom-color: #ff4500 !important;
    background: transparent !important;
}

/* Dataframes / tables */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Headers */
h1 { color: #f0f0f0 !important; font-weight: 800 !important; }
h2, h3 { color: #f0f0f0 !important; font-weight: 700 !important; }

/* Divider */
hr { border-color: rgba(255,69,0,0.2) !important; }

/* Cards */
.fpl-card {
    background: #16213e;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.fpl-card-title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #aaaaaa;
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.8rem;
}
.award-king   { background:rgba(0,229,255,.15); color:#00e5ff; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; }
.award-queen  { background:rgba(255,23,68,.15);  color:#ff4f70; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; }
.award-bench  { background:rgba(255,214,0,.15);  color:#ffd600; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; }
.award-double { background:rgba(0,230,118,.15);  color:#00e676; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; }
.award-orange { background:rgba(255,109,0,.15);  color:#ff6d00; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:700; }
.chip-wc { background:rgba(213,0,249,.2); color:#e040fb; padding:2px 8px; border-radius:99px; font-size:11px; font-weight:700; border:1px solid rgba(213,0,249,.3); }
.chip-tc { background:rgba(255,214,0,.2); color:#ffd600; padding:2px 8px; border-radius:99px; font-size:11px; font-weight:700; border:1px solid rgba(255,214,0,.3); }
.chip-bb { background:rgba(0,230,118,.2); color:#00e676; padding:2px 8px; border-radius:99px; font-size:11px; font-weight:700; border:1px solid rgba(0,230,118,.3); }
.chip-fh { background:rgba(41,121,255,.2); color:#82b1ff; padding:2px 8px; border-radius:99px; font-size:11px; font-weight:700; border:1px solid rgba(41,121,255,.3); }
.rank-gold   { background:#ffd700; color:#1a1a00; width:26px; height:26px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:800; font-size:12px; }
.rank-silver { background:#c0c0c0; color:#1a1a1a; width:26px; height:26px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:800; font-size:12px; }
.rank-bronze { background:#cd7f32; color:#1a0a00; width:26px; height:26px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:800; font-size:12px; }
.player-card {
    background:#2a2a4a; border:1px solid rgba(255,255,255,.1);
    border-radius:10px; padding:10px 12px; text-align:center;
    margin:4px;
}
.pc-pos-gk  { color:#ffd600; font-size:9px; font-weight:700; letter-spacing:1px; font-family:'Space Mono',monospace; }
.pc-pos-def { color:#82b1ff; font-size:9px; font-weight:700; letter-spacing:1px; font-family:'Space Mono',monospace; }
.pc-pos-mid { color:#00e676; font-size:9px; font-weight:700; letter-spacing:1px; font-family:'Space Mono',monospace; }
.pc-pos-fwd { color:#ff4500; font-size:9px; font-weight:700; letter-spacing:1px; font-family:'Space Mono',monospace; }
.pc-name { font-size:13px; font-weight:700; color:#f0f0f0; margin:3px 0; }
.pc-team { font-size:10px; color:#aaaaaa; }
.pc-pts  { font-size:18px; font-weight:800; color:#ffd700; font-family:'Space Mono',monospace; margin-top:4px; }
.formation-row { display:flex; justify-content:center; flex-wrap:wrap; gap:8px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
CLASSIC_ID = 37679
H2H_ID     = 294115
FPL_BASE   = "https://fantasy.premierleague.com/api"

ENTRIES = [
    {"id": 198683,  "name": "Lêds",               "manager": "An Ng"},
    {"id": 3973873, "name": "The Liems FC",        "manager": "Hiếu Nguyễn"},
    {"id": 888937,  "name": "bún chả ngon",        "manager": "Bach Tran"},
    {"id": 1537418, "name": "Nhẵng cực",           "manager": "Manh Linh Tran"},
    {"id": 7897954, "name": "Doi bong nho",        "manager": "Gia Bách Nguyễn"},
    {"id": 848693,  "name": "đày ải 100 năm",      "manager": "Khoi Nguyen"},
    {"id": 5221586, "name": "Pamiuoi",             "manager": "Hà Phạm"},
    {"id": 4979754, "name": "NAtoEU",              "manager": "Trung Le"},
    {"id": 208451,  "name": "Sa Làh Nhớ",          "manager": "Hai V"},
    {"id": 1727691, "name": "Thành Cát Thư Giãn",  "manager": "Vũ Hoàng"},
    {"id": 5126841, "name": "Tung Dich FC",        "manager": "Tùng Nguyễn"},
    {"id": 910084,  "name": "Hẹ hẹ",              "manager": "Phú Nguyễn"},
]

TEAM_COLORS = [
    "#ff4500","#ffd700","#00e676","#2979ff","#d500f9",
    "#ff6b35","#00e5ff","#ff1744","#76ff03","#ff6d00","#e040fb","#40c4ff"
]

# ─── DATA FETCHING ────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://fantasy.premierleague.com/",
}

def fpl_get(path, retries=3):
    for attempt in range(retries):
        try:
            r = requests.get(FPL_BASE + path, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                return r.json()
            time.sleep(2)
        except Exception:
            time.sleep(2)
    return None

@st.cache_data(ttl=300, show_spinner=False)
def load_bootstrap():
    return fpl_get("/bootstrap-static/")

@st.cache_data(ttl=300, show_spinner=False)
def load_classic():
    d = fpl_get(f"/leagues-classic/{CLASSIC_ID}/standings/")
    return d["standings"]["results"] if d else []

@st.cache_data(ttl=300, show_spinner=False)
def load_h2h():
    d = fpl_get(f"/leagues-h2h/{H2H_ID}/standings/")
    return d["standings"]["results"] if d else []

@st.cache_data(ttl=300, show_spinner=False)
def load_history(entry_id):
    d = fpl_get(f"/entry/{entry_id}/history/")
    return d if d else {"current": [], "chips": []}

@st.cache_data(ttl=300, show_spinner=False)
def load_picks(entry_id, gw):
    return fpl_get(f"/entry/{entry_id}/event/{gw}/picks/")

@st.cache_data(ttl=300, show_spinner=False)
def load_live(gw):
    d = fpl_get(f"/event/{gw}/live/")
    if not d:
        return {}
    return {el["id"]: el["stats"] for el in d.get("elements", [])}

@st.cache_data(ttl=300, show_spinner=False)
def load_h2h_fixtures(gw):
    results = []
    for g in range(1, gw + 1):
        d = fpl_get(f"/leagues-h2h-matches/league/{H2H_ID}/?page=1&event={g}")
        if d and "results" in d:
            results.extend(d["results"])
        time.sleep(0.1)
    return results

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0d0d1a 0%,#1a0a00 50%,#0d0d1a 100%);
     border-bottom:2px solid #ff4500; padding:1.2rem 1.5rem; margin:-1.5rem -1rem 1.5rem;
     display:flex; align-items:center; gap:16px;">
  <div style="font-size:2.5rem; animation:none;">🌋</div>
  <div>
    <div style="font-size:1.5rem; font-weight:800; color:#f0f0f0; letter-spacing:-0.5px;">
      Núi Lửa <span style="color:#ff4500;">FPL</span>
    </div>
    <div style="font-size:11px; color:#aaaaaa; font-family:'Space Mono',monospace; letter-spacing:1px;">
      2025 / 26 SEASON
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
with st.spinner("🔥 Loading league data..."):
    bootstrap = load_bootstrap()

if not bootstrap:
    st.error("⚠️ Could not connect to the FPL API. Please try again in a moment.")
    st.stop()

# Parse bootstrap
current_gw = next(
    (e["id"] for e in bootstrap["events"] if e.get("is_current")),
    next((e["id"] for e in reversed(bootstrap["events"]) if e.get("finished")), 38)
)
player_map = {p["id"]: p for p in bootstrap["elements"]}
team_map   = {t["id"]: t["short_name"] for t in bootstrap["teams"]}

# Load standings
classic_standings = load_classic()
h2h_standings     = load_h2h()

# Show current GW pill
col_gw, col_updated = st.columns([1, 5])
with col_gw:
    st.markdown(f"""
    <div style="background:#ff4500;color:white;font-size:12px;font-weight:700;
         padding:4px 14px;border-radius:99px;font-family:'Space Mono',monospace;
         display:inline-block;margin-bottom:1rem;">
      GW {current_gw}
    </div>
    """, unsafe_allow_html=True)
with col_updated:
    st.markdown(f"<div style='color:#aaaaaa;font-size:11px;padding-top:6px;font-family:Space Mono,monospace;'>Live · refreshes every 5 min · {datetime.utcnow().strftime('%H:%M UTC')}</div>", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🏆 Classic", "⚔️ Premier H2H", "📊 GW Scores", "🥇 Awards", "📈 Stats", "🌟 Team of the GW", "🗺️ H2H Matrix"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CLASSIC
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("### 🏆 Classic League Standings")
    if not classic_standings:
        st.warning("Could not load classic standings.")
    else:
        sorted_classic = sorted(classic_standings, key=lambda x: -x["total"])
        gw_leader = max(classic_standings, key=lambda x: x["event_total"])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Teams", len(classic_standings))
        c2.metric("Current GW", current_gw)
        c3.metric("GW Winner", gw_leader["entry_name"], f"{gw_leader['event_total']} pts")
        c4.metric("Season Leader", sorted_classic[0]["entry_name"], f"{sorted_classic[0]['total']} pts")

        st.markdown("---")

        rows = []
        for m in sorted_classic:
            move = m["last_rank"] - m["rank"]
            move_str = f"▲{move}" if move > 0 else (f"▼{abs(move)}" if move < 0 else "—")
            entry = next((e for e in ENTRIES if e["id"] == m["entry"]), {})
            rows.append({
                "Rank": m["rank"],
                "Team": m["entry_name"],
                "Manager": entry.get("manager", m["player_name"]),
                f"GW {current_gw}": m["event_total"],
                "Total": m["total"],
                "Move": move_str,
            })

        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(
            df, hide_index=True, use_container_width=True,
            column_config={
                "Rank": st.column_config.NumberColumn(width="small"),
                "Total": st.column_config.NumberColumn(width="small"),
                f"GW {current_gw}": st.column_config.NumberColumn(width="small"),
            }
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PREMIER H2H
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("### ⚔️ Premier H2H Standings")
    if not h2h_standings:
        st.warning("Could not load H2H standings.")
    else:
        sorted_h2h = sorted(h2h_standings, key=lambda x: (-x["total"], -x["points_for"]))

        rows = []
        for m in sorted_h2h:
            wr = round(m["matches_won"] / m["matches_played"] * 100) if m["matches_played"] > 0 else 0
            entry = next((e for e in ENTRIES if e["id"] == m["entry"]), {})
            rows.append({
                "Rank": m["rank"],
                "Team": m["entry_name"],
                "Manager": entry.get("manager", m["player_name"]),
                "MP": m["matches_played"],
                "W": m["matches_won"],
                "D": m["matches_drawn"],
                "L": m["matches_lost"],
                "H2H Pts": m["total"],
                "FPL Pts": m["points_for"],
                "Win %": f"{wr}%",
            })

        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df, hide_index=True, use_container_width=True,
            column_config={
                "Rank": st.column_config.NumberColumn(width="small"),
                "MP": st.column_config.NumberColumn(width="small"),
                "W":  st.column_config.NumberColumn(width="small"),
                "D":  st.column_config.NumberColumn(width="small"),
                "L":  st.column_config.NumberColumn(width="small"),
                "H2H Pts": st.column_config.NumberColumn(width="small"),
                "FPL Pts": st.column_config.NumberColumn(width="small"),
            }
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — GW SCORES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("### 📊 Gameweek Scores")

    with st.spinner("Loading histories..."):
        histories = {e["id"]: load_history(e["id"]) for e in ENTRIES}

    import plotly.graph_objects as go

    gw_labels = [f"GW{i}" for i in range(1, current_gw + 1)]

    # GW points chart
    fig_gw = go.Figure()
    for i, e in enumerate(ENTRIES):
        hist = histories[e["id"]].get("current", [])
        pts = [h["points"] for h in hist]
        fig_gw.add_trace(go.Scatter(
            x=gw_labels[:len(pts)], y=pts,
            name=e["name"], mode="lines+markers",
            line=dict(color=TEAM_COLORS[i], width=2),
            marker=dict(size=4),
        ))
    fig_gw.update_layout(
        title="Points per gameweek",
        paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e",
        font=dict(color="#f0f0f0", family="Be Vietnam Pro"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        height=380, margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_gw, use_container_width=True)

    # Cumulative chart
    fig_cum = go.Figure()
    for i, e in enumerate(ENTRIES):
        hist = histories[e["id"]].get("current", [])
        cum, totals = 0, []
        for h in hist:
            cum += h["points"]
            totals.append(cum)
        fig_cum.add_trace(go.Scatter(
            x=gw_labels[:len(totals)], y=totals,
            name=e["name"], mode="lines",
            line=dict(color=TEAM_COLORS[i], width=2),
        ))
    fig_cum.update_layout(
        title="Cumulative total points",
        paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e",
        font=dict(color="#f0f0f0", family="Be Vietnam Pro"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        height=380, margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_cum, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — AWARDS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("### 🥇 GW Awards")

    with st.spinner("Calculating awards..."):
        histories = {e["id"]: load_history(e["id"]) for e in ENTRIES}

    tally = {e["id"]: {"king": 0, "queen": 0, "bench": 0, "double": 0, "orange": 0} for e in ENTRIES}
    gw_award_data = []

    for gw in range(1, current_gw + 1):
        scores = []
        for e in ENTRIES:
            hist = histories[e["id"]].get("current", [])
            row = next((h for h in hist if h["event"] == gw), None)
            if row and row["points"] > 0:
                scores.append({"id": e["id"], "name": e["name"], "pts": row["points"], "bench": row.get("points_on_bench", 0)})

        if not scores:
            continue

        max_pts   = max(s["pts"] for s in scores)
        min_pts   = min(s["pts"] for s in scores)
        max_bench = max(s["bench"] for s in scores)
        avg_pts   = round(sum(s["pts"] for s in scores) / len(scores))

        kings    = [s for s in scores if s["pts"] == max_pts]
        queens   = [s for s in scores if s["pts"] == min_pts]
        benchers = [s for s in scores if s["bench"] == max_bench and max_bench > 0]

        for s in scores:
            is_k = any(k["id"] == s["id"] for k in kings)
            is_q = any(q["id"] == s["id"] for q in queens)
            is_b = any(b["id"] == s["id"] for b in benchers)
            if is_k and is_b:
                tally[s["id"]]["double"] += 1
            elif is_k:
                tally[s["id"]]["king"] += 1
            if is_q and is_b:
                tally[s["id"]]["orange"] += 1
            elif is_q:
                tally[s["id"]]["queen"] += 1
            if is_b and not is_k and not is_q:
                tally[s["id"]]["bench"] += 1

        gw_award_data.append({"gw": gw, "scores": scores, "kings": kings, "queens": queens, "benchers": benchers, "avg": avg_pts})

    # Award tally table
    import pandas as pd
    tally_rows = []
    for e in ENTRIES:
        t = tally[e["id"]]
        tally_rows.append({
            "Team": e["name"],
            "👑 King": t["king"],
            "✨ King+Bench": t["double"],
            "👸 Queen": t["queen"],
            "🏅 Bench": t["bench"],
            "🟠 Queen+Bench": t["orange"],
        })
    tally_df = pd.DataFrame(tally_rows).sort_values("👑 King", ascending=False)
    st.markdown("#### Season award tally")
    st.dataframe(tally_df, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Per-gameweek breakdown")

    for item in reversed(gw_award_data):
        with st.expander(f"GW {item['gw']} — avg {item['avg']} pts", expanded=(item['gw'] == current_gw)):
            rows = []
            for s in sorted(item["scores"], key=lambda x: -x["pts"]):
                is_k = any(k["id"] == s["id"] for k in item["kings"])
                is_q = any(q["id"] == s["id"] for q in item["queens"])
                is_b = any(b["id"] == s["id"] for b in item["benchers"])
                awards = []
                if is_k and is_b: awards.append("👑🏅 King+Bench")
                elif is_k:        awards.append("👑 King")
                if is_q and is_b: awards.append("👸🏅 Queen+Bench")
                elif is_q:        awards.append("👸 Queen")
                if is_b and not is_k and not is_q: awards.append("🏅 Bench")
                rows.append({
                    "Team": s["name"],
                    "Points": s["pts"],
                    "Bench Pts": s["bench"],
                    "Award": " · ".join(awards) if awards else "",
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — STATS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("### 📈 Season Stats")

    with st.spinner("Loading stats..."):
        histories = {e["id"]: load_history(e["id"]) for e in ENTRIES}

    import pandas as pd
    import plotly.graph_objects as go

    stats_data = []
    for e in ENTRIES:
        hist = histories[e["id"]].get("current", [])
        chips = histories[e["id"]].get("chips", [])
        chip_map = {c["name"]: c["event"] for c in chips}
        total_pts      = sum(h["points"] for h in hist)
        total_bench    = sum(h.get("points_on_bench", 0) for h in hist)
        total_transfers = sum(h.get("event_transfers", 0) for h in hist)
        total_hits     = sum(h.get("event_transfers_cost", 0) for h in hist)
        avg_pts        = round(total_pts / len(hist)) if hist else 0
        best_gw        = max((h["points"] for h in hist), default=0)
        worst_gw       = min((h["points"] for h in hist), default=0)
        stats_data.append({
            "entry": e,
            "total_pts": total_pts,
            "total_bench": total_bench,
            "total_transfers": total_transfers,
            "total_hits": total_hits,
            "avg_pts": avg_pts,
            "best_gw": best_gw,
            "worst_gw": worst_gw,
            "chip_map": chip_map,
        })

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Total points")
        sorted_pts = sorted(stats_data, key=lambda x: -x["total_pts"])
        max_pts = sorted_pts[0]["total_pts"] if sorted_pts else 1
        for s in sorted_pts:
            pct = s["total_pts"] / max_pts
            st.markdown(f"""
            <div style='margin-bottom:8px'>
              <div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px'>
                <span style='color:#f0f0f0'>{s['entry']['name']}</span>
                <span style='color:#aaaaaa;font-family:Space Mono,monospace'>{s['total_pts']}</span>
              </div>
              <div style='height:6px;background:rgba(255,255,255,.08);border-radius:99px;overflow:hidden'>
                <div style='height:100%;width:{pct*100:.0f}%;background:#ff4500;border-radius:99px'></div>
              </div>
            </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("#### Points wasted on bench 💸")
        sorted_bench = sorted(stats_data, key=lambda x: -x["total_bench"])
        max_bench = sorted_bench[0]["total_bench"] if sorted_bench else 1
        for s in sorted_bench:
            pct = s["total_bench"] / max_bench
            st.markdown(f"""
            <div style='margin-bottom:8px'>
              <div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px'>
                <span style='color:#f0f0f0'>{s['entry']['name']}</span>
                <span style='color:#aaaaaa;font-family:Space Mono,monospace'>{s['total_bench']}</span>
              </div>
              <div style='height:6px;background:rgba(255,255,255,.08);border-radius:99px;overflow:hidden'>
                <div style='height:100%;width:{pct*100:.0f}%;background:#ffd700;border-radius:99px'></div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("#### Transfer activity")
    sorted_tr = sorted(stats_data, key=lambda x: -x["total_transfers"])
    max_tr = sorted_tr[0]["total_transfers"] if sorted_tr else 1
    for s in sorted_tr:
        pct = s["total_transfers"] / max_tr
        st.markdown(f"""
        <div style='margin-bottom:8px'>
          <div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px'>
            <span style='color:#f0f0f0'>{s['entry']['name']}</span>
            <span style='color:#aaaaaa;font-family:Space Mono,monospace'>{s['total_transfers']} transfers
            <span style='color:#ff1744'> · -{s['total_hits']} hit pts</span></span>
          </div>
          <div style='height:6px;background:rgba(255,255,255,.08);border-radius:99px;overflow:hidden'>
            <div style='height:100%;width:{pct*100:.0f}%;background:#00e5ff;border-radius:99px'></div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Chips & season extremes")

    def chip_html(name, chip_map):
        labels = {"wildcard": ("WC","chip-wc"), "triple_captain": ("TC","chip-tc"), "bboost": ("BB","chip-bb"), "freehit": ("FH","chip-fh")}
        if name in chip_map:
            lbl, cls = labels[name]
            return f'<span class="{cls}">{lbl}</span> <small style="color:#aaaaaa">GW{chip_map[name]}</small>'
        return '<span style="color:#555">—</span>'

    chip_rows = []
    for s in stats_data:
        chip_rows.append({
            "Team": s["entry"]["name"],
            "WC": "GW" + str(s["chip_map"]["wildcard"]) if "wildcard" in s["chip_map"] else "—",
            "TC": "GW" + str(s["chip_map"]["triple_captain"]) if "triple_captain" in s["chip_map"] else "—",
            "BB": "GW" + str(s["chip_map"]["bboost"]) if "bboost" in s["chip_map"] else "—",
            "FH": "GW" + str(s["chip_map"]["freehit"]) if "freehit" in s["chip_map"] else "—",
            "Best GW": s["best_gw"],
            "Worst GW": s["worst_gw"],
            "Avg GW": s["avg_pts"],
        })
    st.dataframe(pd.DataFrame(chip_rows), hide_index=True, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — TEAM OF THE GW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("### 🌟 Team of the Gameweek")
    st.markdown("Best 11 players across all squads — 1 GK + 10 outfielders")

    selected_gw = st.selectbox(
        "Select Gameweek",
        options=list(range(current_gw, 0, -1)),
        format_func=lambda x: f"GW {x}" + (" (latest)" if x == current_gw else ""),
    )

    with st.spinner(f"Loading GW {selected_gw} picks..."):
        live_map = load_live(selected_gw)
        all_players = []
        for e in ENTRIES:
            picks_data = load_picks(e["id"], selected_gw)
            if not picks_data:
                continue
            active_chip = picks_data.get("active_chip")
            for pick in picks_data.get("picks", []):
                if pick["multiplier"] == 0:
                    continue
                p = player_map.get(pick["element"])
                if not p:
                    continue
                live = live_map.get(pick["element"], {})
                raw_pts = live.get("total_points", 0)
                pts = raw_pts * pick["multiplier"]
                all_players.append({
                    "id": pick["element"],
                    "name": p["web_name"],
                    "team": team_map.get(p["team"], ""),
                    "pos": p["element_type"],
                    "pts": pts,
                    "raw_pts": raw_pts,
                    "multiplier": pick["multiplier"],
                    "entry_name": e["name"],
                })

    gks      = sorted([p for p in all_players if p["pos"] == 1], key=lambda x: -x["pts"])
    outfield = sorted([p for p in all_players if p["pos"] != 1], key=lambda x: -x["pts"])
    best11   = ([gks[0]] if gks else []) + outfield[:10]
    total_pts = sum(p["pts"] for p in best11)

    c1, c2, c3 = st.columns(3)
    c1.metric("Gameweek", selected_gw)
    c2.metric("Team Total", total_pts, "pts incl. captaincy")
    c3.metric("Top Scorer", best11[0]["name"] if best11 else "—", f"{best11[0]['pts']} pts" if best11 else "")

    st.markdown("---")

    pos_groups = {1: [], 2: [], 3: [], 4: []}
    for p in best11:
        pos_groups[p["pos"]].append(p)

    pos_labels  = {1: "GK",  2: "DEF",  3: "MID",  4: "FWD"}
    pos_classes = {1: "pc-pos-gk", 2: "pc-pos-def", 3: "pc-pos-mid", 4: "pc-pos-fwd"}

    def player_card_html(p):
        mult = f" ×{p['multiplier']}" if p["multiplier"] > 1 else ""
        return f"""<div class="player-card">
            <div class="{pos_classes[p['pos']]}">{pos_labels[p['pos']]}</div>
            <div class="pc-name">{p['name']}{mult}</div>
            <div class="pc-team">{p['team']} · {p['entry_name']}</div>
            <div class="pc-pts">{p['pts']}</div>
        </div>"""

    for pos in [1, 2, 3, 4]:
        if pos_groups[pos]:
            cards_html = "".join(player_card_html(p) for p in pos_groups[pos])
            st.markdown(f'<div class="formation-row">{cards_html}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — H2H MATRIX
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("### 🗺️ Head-to-Head Matrix")
    st.markdown("Win–Draw–Loss record for every head-to-head matchup")

    with st.spinner("Loading H2H fixtures..."):
        fixtures = load_h2h_fixtures(current_gw)

    record = {e["id"]: {e2["id"]: {"w": 0, "d": 0, "l": 0} for e2 in ENTRIES} for e in ENTRIES}

    for f in fixtures:
        if not f.get("finished"):
            continue
        e1, e2 = f.get("entry_1_entry"), f.get("entry_2_entry")
        p1, p2 = f.get("entry_1_points", 0), f.get("entry_2_points", 0)
        if e1 not in record or e2 not in record:
            continue
        if p1 > p2:
            record[e1][e2]["w"] += 1; record[e2][e1]["l"] += 1
        elif p2 > p1:
            record[e2][e1]["w"] += 1; record[e1][e2]["l"] += 1
        else:
            record[e1][e2]["d"] += 1; record[e2][e1]["d"] += 1

    import pandas as pd
    short = [e["name"].split()[0] for e in ENTRIES]
    matrix_data = {}
    for i, row_e in enumerate(ENTRIES):
        row = {}
        for j, col_e in enumerate(ENTRIES):
            if row_e["id"] == col_e["id"]:
                row[short[j]] = "—"
            else:
                r = record[row_e["id"]][col_e["id"]]
                row[short[j]] = f"{r['w']}-{r['d']}-{r['l']}"
        matrix_data[short[i]] = row

    matrix_df = pd.DataFrame(matrix_data).T
    st.dataframe(matrix_df, use_container_width=True)

    st.markdown("""
    <div style='font-size:12px;color:#aaaaaa;margin-top:0.5rem'>
      Format: <strong style='color:#f0f0f0'>W-D-L</strong> from the row team's perspective
    </div>
    """, unsafe_allow_html=True)
