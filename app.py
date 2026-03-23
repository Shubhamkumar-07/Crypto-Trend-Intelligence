from __future__ import annotations

import os
from typing import Any

import pandas as pd  # type: ignore
import plotly.graph_objects as go
import requests
import streamlit as st  # type: ignore
from streamlit_autorefresh import st_autorefresh  # type: ignore


BACKEND_URL = os.getenv("HYPESHIELD_BACKEND_URL", "http://127.0.0.1:8000/api")
ACCENT_GREEN = "#31f28b"
ACCENT_RED = "#ff5d73"
ACCENT_GOLD = "#ffca5f"
PANEL_BG = "#101826"
CARD_BG = "#0b1220"
TEXT_DIM = "#8da2c0"
LOGIN_ACCENT = "#6bf2ff"
LOGIN_USER = os.getenv("HYPESHIELD_LOGIN_USER", "admin")
LOGIN_PASSWORD = os.getenv("HYPESHIELD_LOGIN_PASSWORD", "hypeshield")


def fetch_json(path: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    try:
        response = requests.get(f"{BACKEND_URL}{path}", params=params, timeout=8)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def render_metric_card(label: str, value: str, accent: str, caption: str) -> None:
    st.markdown(
        f"""
        <div style="background:{CARD_BG}; border:1px solid rgba(255,255,255,0.06); border-left:4px solid {accent};
                    border-radius:18px; padding:18px 18px 14px 18px; min-height:132px;">
            <div style="color:{TEXT_DIM}; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.08em;">{label}</div>
            <div style="color:white; font-size:2rem; font-weight:700; margin-top:10px;">{value}</div>
            <div style="color:{TEXT_DIM}; font-size:0.9rem; margin-top:10px;">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def series_to_frame(points: list[dict[str, Any]], column: str) -> pd.DataFrame:
    frame = pd.DataFrame(points)
    if frame.empty:
        return pd.DataFrame(columns=["timestamp", column])
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    frame.rename(columns={"value": column}, inplace=True)
    return frame


def build_line_chart(frame: pd.DataFrame, y_col: str, title: str, color: str) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=frame["timestamp"],
            y=frame[y_col],
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=6),
            fill="tozeroy",
            fillcolor=f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.12)",
            name=title,
        )
    )
    figure.update_layout(
        title=title,
        paper_bgcolor=PANEL_BG,
        plot_bgcolor=PANEL_BG,
        margin=dict(l=24, r=24, t=52, b=24),
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        height=300,
    )
    return figure


def inject_base_styles() -> None:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background:
                    radial-gradient(circle at top left, rgba(49,242,139,0.14), transparent 26%),
                    radial-gradient(circle at top right, rgba(255,93,115,0.10), transparent 20%),
                    linear-gradient(180deg, #04070d 0%, #08111d 48%, #050913 100%);
                color: white;
            }}
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #08111d 0%, #050913 100%);
                border-right: 1px solid rgba(255,255,255,0.06);
            }}
            div[data-testid="stMetric"] {{
                background: {CARD_BG};
                border: 1px solid rgba(255,255,255,0.06);
                padding: 10px 12px;
                border-radius: 16px;
            }}
            div[data-testid="stForm"] {{
                border: none;
                background: transparent;
                padding: 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_login_page() -> None:
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebar"] {{
                display: none;
            }}
            .block-container {{
                padding-top: 1.5rem;
                padding-bottom: 1.5rem;
            }}
            .login-shell {{
                position: relative;
                min-height: calc(100vh - 3rem);
                overflow: hidden;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 28px;
                background:
                    radial-gradient(circle at 15% 20%, rgba(107,242,255,0.16), transparent 20%),
                    radial-gradient(circle at 82% 18%, rgba(255,93,115,0.14), transparent 18%),
                    radial-gradient(circle at 50% 88%, rgba(49,242,139,0.12), transparent 26%),
                    linear-gradient(135deg, rgba(4,8,16,0.96), rgba(8,17,29,0.88));
                box-shadow: 0 30px 80px rgba(0,0,0,0.45);
            }}
            .login-orb {{
                position: absolute;
                border-radius: 999px;
                filter: blur(8px);
                opacity: 0.85;
                animation: drift 14s ease-in-out infinite;
            }}
            .orb-one {{
                width: 240px;
                height: 240px;
                top: 8%;
                left: 6%;
                background: radial-gradient(circle, rgba(107,242,255,0.55), rgba(107,242,255,0.02) 70%);
            }}
            .orb-two {{
                width: 320px;
                height: 320px;
                right: -6%;
                top: 12%;
                background: radial-gradient(circle, rgba(255,93,115,0.48), rgba(255,93,115,0.02) 72%);
                animation-delay: -5s;
            }}
            .orb-three {{
                width: 260px;
                height: 260px;
                left: 42%;
                bottom: -10%;
                background: radial-gradient(circle, rgba(49,242,139,0.38), rgba(49,242,139,0.02) 72%);
                animation-delay: -9s;
            }}
            .login-grid {{
                position: relative;
                z-index: 2;
                display: grid;
                grid-template-columns: 1.15fr 0.85fr;
                gap: 28px;
                padding: 52px;
                min-height: calc(100vh - 3rem);
            }}
            .login-copy {{
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}
            .eyebrow {{
                display: inline-flex;
                align-items: center;
                gap: 10px;
                padding: 10px 16px;
                border-radius: 999px;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.08);
                color: #d7e7ff;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.16em;
                backdrop-filter: blur(14px);
            }}
            .eyebrow::before {{
                content: "";
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: {LOGIN_ACCENT};
                box-shadow: 0 0 18px {LOGIN_ACCENT};
            }}
            .login-title {{
                margin-top: 28px;
                max-width: 720px;
                font-size: clamp(3rem, 5vw, 5.2rem);
                line-height: 0.96;
                font-weight: 900;
                letter-spacing: -0.04em;
            }}
            .login-title .accent {{
                color: {LOGIN_ACCENT};
                text-shadow: 0 0 28px rgba(107,242,255,0.28);
            }}
            .login-subtitle {{
                margin-top: 20px;
                max-width: 620px;
                color: #9fb3d1;
                font-size: 1.05rem;
                line-height: 1.8;
            }}
            .signal-row {{
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 16px;
                margin-top: 36px;
                max-width: 760px;
            }}
            .signal-card {{
                padding: 18px;
                border-radius: 22px;
                background: rgba(9, 16, 30, 0.72);
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
                backdrop-filter: blur(18px);
                transform: translateY(0);
                animation: riseIn 0.9s ease forwards;
            }}
            .signal-label {{
                color: #8da2c0;
                font-size: 0.82rem;
                text-transform: uppercase;
                letter-spacing: 0.12em;
            }}
            .signal-value {{
                margin-top: 14px;
                font-size: 1.8rem;
                font-weight: 800;
            }}
            .signal-caption {{
                margin-top: 8px;
                color: #9fb3d1;
                font-size: 0.92rem;
            }}
            .login-panel {{
                align-self: center;
                padding: 28px;
                border-radius: 30px;
                background: linear-gradient(180deg, rgba(10,16,28,0.82), rgba(6,10,20,0.9));
                border: 1px solid rgba(255,255,255,0.10);
                box-shadow: 0 18px 60px rgba(0,0,0,0.42);
                backdrop-filter: blur(20px);
                animation: floatPanel 4.5s ease-in-out infinite;
            }}
            .panel-kicker {{
                color: #8da2c0;
                text-transform: uppercase;
                letter-spacing: 0.18em;
                font-size: 0.8rem;
            }}
            .panel-title {{
                margin-top: 14px;
                font-size: 2rem;
                line-height: 1.05;
                font-weight: 800;
            }}
            .panel-copy {{
                margin-top: 12px;
                color: #9fb3d1;
                line-height: 1.7;
            }}
            .demo-note {{
                margin-top: 18px;
                padding: 12px 14px;
                border-radius: 16px;
                background: rgba(107,242,255,0.08);
                color: #dffaff;
                font-size: 0.95rem;
                border: 1px solid rgba(107,242,255,0.18);
            }}
            @keyframes drift {{
                0%, 100% {{ transform: translate3d(0, 0, 0) scale(1); }}
                50% {{ transform: translate3d(18px, -24px, 0) scale(1.08); }}
            }}
            @keyframes floatPanel {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-8px); }}
            }}
            @keyframes riseIn {{
                from {{ opacity: 0; transform: translateY(24px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @media (max-width: 980px) {{
                .login-grid {{
                    grid-template-columns: 1fr;
                    padding: 28px;
                    min-height: auto;
                }}
                .signal-row {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        <div class="login-shell">
            <div class="login-orb orb-one"></div>
            <div class="login-orb orb-two"></div>
            <div class="login-orb orb-three"></div>
            <div class="login-grid">
                <div class="login-copy">
                    <div>
                        <div class="eyebrow">Realtime Crypto Intelligence</div>
                        <div class="login-title">
                            Catch the <span class="accent">hype cycle</span><br>before the crowd does.
                        </div>
                        <div class="login-subtitle">
                            HypeShield AI tracks social surges, fake-hype pressure, and momentum decay across meme coins,
                            then turns that chaos into a clean signal desk your team can act on.
                        </div>
                        <div class="signal-row">
                            <div class="signal-card">
                                <div class="signal-label">Pump Detection</div>
                                <div class="signal-value">Live velocity</div>
                                <div class="signal-caption">Spot abnormal mention acceleration before it peaks.</div>
                            </div>
                            <div class="signal-card">
                                <div class="signal-label">Fake Hype Radar</div>
                                <div class="signal-value">Bot pressure</div>
                                <div class="signal-caption">Flag inorganic engagement and suspicious crowd behavior.</div>
                            </div>
                            <div class="signal-card">
                                <div class="signal-label">Crash Readiness</div>
                                <div class="signal-value">Exit timing</div>
                                <div class="signal-caption">Watch the sentiment rollover before momentum breaks.</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="login-panel">
                    <div class="panel-kicker">Secure Access</div>
                    <div class="panel-title">Enter the HypeShield command room</div>
                    <div class="panel-copy">
                        Sign in to unlock the animated live dashboard, coin radar, and alert stream.
                    </div>
                    <div class="demo-note">
                        Demo login: <strong>{LOGIN_USER}</strong> / <strong>{LOGIN_PASSWORD}</strong>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([0.18, 0.64, 0.18])
    with center:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Launch Dashboard", use_container_width=True, type="primary")

        if submitted:
            if username == LOGIN_USER and password == LOGIN_PASSWORD:
                st.session_state["authenticated"] = True
                st.session_state["auth_user"] = username
                st.success("Access granted. Opening the dashboard...")
                st.rerun()
            else:
                st.error("Invalid credentials. Use the demo login shown on the panel.")


def main() -> None:
    st.set_page_config(
        page_title="HypeShield AI - Meme Coin Predictor",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
    )

    inject_base_styles()

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        render_login_page()
        return

    with st.sidebar:
        st.markdown("## HypeShield AI")
        st.caption("Meme coin bubble and crash predictor")
        st.caption(f"Signed in as {st.session_state.get('auth_user', LOGIN_USER)}")
        auto_refresh = st.toggle("Auto-refresh", value=True)
        refresh_seconds = st.slider("Refresh interval (seconds)", 5, 30, 8, 1)
        if st.button("Logout", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state.pop("auth_user", None)
            st.rerun()

    if auto_refresh:
        st_autorefresh(interval=refresh_seconds * 1000, key="dashboard_refresh")

    coins_payload = fetch_json("/coins") or {"coins": ["DOGE", "SHIB", "PEPE"], "data_mode": "simulated", "cards": []}
    cards = coins_payload.get("cards", [])
    available_coins = coins_payload.get("coins", ["DOGE", "SHIB", "PEPE"])
    selected_coin = st.sidebar.selectbox("Select coin", available_coins, index=0)

    analysis = fetch_json(f"/analyze/{selected_coin}")
    alerts_payload = fetch_json("/alerts", params={"coin": selected_coin}) or {"alerts": []}

    st.markdown(
        f"""
        <div style="padding: 8px 0 22px 0;">
            <div style="color:{TEXT_DIM}; text-transform:uppercase; letter-spacing:0.14em; font-size:0.85rem;">Live Intelligence Layer</div>
            <div style="font-size:3rem; font-weight:800; line-height:1.05; margin-top:8px;">HypeShield AI - Meme Coin Predictor</div>
            <div style="color:{TEXT_DIM}; font-size:1rem; margin-top:10px; max-width:760px;">
                Detects fake hype, tracks sentiment velocity, and estimates pump versus crash probability before meme coin moves go mainstream.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not analysis:
        st.error("Backend data is unavailable. Start FastAPI with `uvicorn app.main:app --reload` from the `backend` folder.")
        return

    top_cards = st.columns(4)
    with top_cards[0]:
        render_metric_card("Sentiment", f"{analysis['sentiment_score']:+.2f}", ACCENT_GREEN, "Aggregated social sentiment")
    with top_cards[1]:
        render_metric_card("Pump Probability", f"{analysis['pump_probability']:.1f}%", ACCENT_GREEN, "Likelihood of upside momentum")
    with top_cards[2]:
        render_metric_card("Crash Risk", f"{analysis['crash_probability']:.1f}%", ACCENT_RED, "Probability of a dump event")
    with top_cards[3]:
        render_metric_card("Fake Hype", f"{analysis['fake_hype_score']:.2f}", ACCENT_GOLD, "Manipulation pressure score")

    status_left, status_right = st.columns([1.35, 1])
    with status_left:
        st.markdown(
            f"""
            <div style="background:{PANEL_BG}; border:1px solid rgba(255,255,255,0.06); border-radius:22px; padding:22px;">
                <div style="color:{TEXT_DIM}; font-size:0.9rem;">CURRENT STAGE</div>
                <div style="font-size:2rem; font-weight:700; margin-top:8px;">{analysis['hype_stage']}</div>
                <div style="display:flex; gap:16px; margin-top:18px; flex-wrap:wrap;">
                    <div><span style="color:{TEXT_DIM};">Confidence</span><br><span style="font-size:1.4rem;">{analysis['confidence_score']:.2f}</span></div>
                    <div><span style="color:{TEXT_DIM};">Trend Strength</span><br><span style="font-size:1.4rem;">{analysis['trend_strength']:.2f}</span></div>
                    <div><span style="color:{TEXT_DIM};">Mentions</span><br><span style="font-size:1.4rem;">{analysis['mention_volume']}</span></div>
                    <div><span style="color:{TEXT_DIM};">Velocity / hr</span><br><span style="font-size:1.4rem;">{analysis['velocity_per_hour']:.1f}</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with status_right:
        mode_color = ACCENT_GREEN if analysis["source_mode"] == "live" else ACCENT_GOLD
        st.markdown(
            f"""
            <div style="background:{PANEL_BG}; border:1px solid rgba(255,255,255,0.06); border-radius:22px; padding:22px;">
                <div style="color:{TEXT_DIM}; font-size:0.9rem;">DATA SOURCE</div>
                <div style="font-size:2rem; font-weight:700; margin-top:8px; color:{mode_color};">{analysis['source_mode'].upper()}</div>
                <div style="color:{TEXT_DIM}; margin-top:12px;">Data quality score: {analysis['data_quality']:.2f}</div>
                <div style="color:{TEXT_DIM}; margin-top:8px;">Total engagement: {analysis['engagement_total']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    mention_frame = series_to_frame(analysis["mention_series"], "mentions")
    sentiment_frame = series_to_frame(analysis["sentiment_series"], "sentiment")
    engagement_frame = series_to_frame(analysis["engagement_series"], "engagement")

    chart_left, chart_mid, chart_right = st.columns(3)
    with chart_left:
        st.plotly_chart(build_line_chart(mention_frame, "mentions", "Mention Volume Trend", ACCENT_GOLD), use_container_width=True)
    with chart_mid:
        st.plotly_chart(build_line_chart(sentiment_frame, "sentiment", "Sentiment Flow", ACCENT_GREEN), use_container_width=True)
    with chart_right:
        st.plotly_chart(build_line_chart(engagement_frame, "engagement", "Engagement Heat", ACCENT_RED), use_container_width=True)

    lower_left, lower_right = st.columns([1.25, 0.95])
    with lower_left:
        st.markdown("### Market Radar")
        coin_cards = pd.DataFrame(cards)
        if not coin_cards.empty:
            st.dataframe(
                coin_cards[["coin", "source_mode", "sentiment_score", "pump_probability", "crash_probability", "fake_hype_score", "hype_stage", "mention_volume"]],
                use_container_width=True,
                hide_index=True,
            )

        st.markdown("### Recent Social Posts")
        for post in analysis["recent_posts"]:
            st.markdown(
                f"""
                <div style="background:{PANEL_BG}; border:1px solid rgba(255,255,255,0.06); border-radius:16px; padding:14px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; color:{TEXT_DIM}; font-size:0.9rem;">
                        <span>{post['platform']} / @{post['username']}</span>
                        <span>{pd.to_datetime(post['timestamp']).strftime('%d %b %H:%M')}</span>
                    </div>
                    <div style="margin-top:8px; color:white;">{post['text']}</div>
                    <div style="margin-top:10px; color:{TEXT_DIM}; font-size:0.9rem;">
                        engagement {post['engagement']} | followers {post.get('follower_count') or 'n/a'} | account age {post.get('account_age_days') or 'n/a'} days
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with lower_right:
        st.markdown("### Alerts Panel")
        alerts = alerts_payload.get("alerts", [])
        if alerts:
            for alert in alerts:
                if alert["severity"] == "warning":
                    st.warning(alert["message"])
                elif alert["severity"] == "error":
                    st.error(alert["message"])
                else:
                    st.success(alert["message"])
        else:
            st.info("No high-priority alerts right now.")

        st.markdown("### Signal Balance")
        pump = analysis["pump_probability"]
        crash = analysis["crash_probability"]
        signal_figure = go.Figure(
            data=[
                go.Bar(
                    x=["Pump", "Crash"],
                    y=[pump, crash],
                    marker_color=[ACCENT_GREEN, ACCENT_RED],
                    text=[f"{pump:.1f}%", f"{crash:.1f}%"],
                    textposition="outside",
                )
            ]
        )
        signal_figure.update_layout(
            paper_bgcolor=PANEL_BG,
            plot_bgcolor=PANEL_BG,
            font=dict(color="white"),
            margin=dict(l=16, r=16, t=32, b=16),
            height=280,
            yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(signal_figure, use_container_width=True)


if __name__ == "__main__":
    main()
