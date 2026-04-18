from pathlib import Path
import os
import pandas as pd
import requests
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://les-francaises-et-francais-audiovisuel.onrender.com/api/v1"
)
API_KEY = os.getenv("API_KEY", "")

def fetch_api_data(endpoint: str, params: dict | None = None) -> pd.DataFrame:
    headers = {}
    if API_KEY:
        headers["X-API-Key"] = API_KEY

    response = requests.get(
        f"{API_BASE_URL}{endpoint}",
        headers=headers,
        params=params,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data)

# Fallback pour le développement local sans accès à l'API
def load_csv_fallback(filename: str) -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / filename)

def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        .main {
            background-color: #F4F1DE;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        h1, h2, h3 {
            color: #3D405B;
            letter-spacing: -0.02em;
        }

        .subtitle {
            font-size: 1.05rem;
            color: #5E503F;
            margin-top: -0.4rem;
            margin-bottom: 1.4rem;
            line-height: 1.6;
        }

        .section-title {
            font-size: 1.45rem;
            font-weight: 700;
            margin-top: 1.8rem;
            margin-bottom: 0.8rem;
            color: #3D405B;
        }

        .section-note {
            font-size: 0.96rem;
            color: #5E503F;
            margin-bottom: 1rem;
        }

        div[data-testid="stMetric"] {
            background: white;
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 4px 18px rgba(61, 64, 91, 0.08);
            border: 1px solid rgba(61, 64, 91, 0.08);
        }

        div[data-testid="stTabs"] button {
            font-size: 1rem;
            color: #3D405B !important;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #3D405B !important;
            border-bottom-color: #3D405B !important;
        }

        div[data-testid="stExpander"] {
            background: white;
            border-radius: 16px;
            border: 1px solid rgba(61, 64, 91, 0.08);
        }

        div[data-baseweb="tag"] {
            background: #EAE0D5 !important;
            border: 1px solid #C6AC8F !important;
            border-radius: 10px !important;
            color: #3D405B !important;
        }

        div[data-baseweb="tag"] * {
            color: #3D405B !important;
        }

        div[data-baseweb="tag"] span {
            color: #3D405B !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="tag"] svg {
            fill: #5E503F !important;
            color: #5E503F !important;
        }

        div[data-baseweb="tag"] button {
            background: transparent !important;
            color: #5E503F !important;
        }

        [data-baseweb="tag"] {
            background: #EAE0D5 !important;
            border: 1px solid #C6AC8F !important;
        }

        [data-baseweb="tag"] * {
            color: #3D405B !important;
        }

        div[data-baseweb="select"] > div {
            border-color: rgba(61, 64, 91, 0.16) !important;
            box-shadow: none !important;
        }

        div[data-baseweb="select"] > div:focus-within {
            border-color: #3D405B !important;
            box-shadow: 0 0 0 1px #3D405B !important;
        }

        input:focus, textarea:focus, select:focus {
            outline: none !important;
            box-shadow: none !important;
            border-color: #3D405B !important;
        }

        /* Slider */
        div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
            background: #3D405B !important;   /* bouton */
            border: 2px solid #3D405B !important;
            box-shadow: none !important;
        }

        div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]::before,
        div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]::after {
            display: none !important;
        }

        div[data-testid="stSlider"] p {
            color: #3D405B !important;   /* valeur affichée */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


PUBLIC_PRIVATE_COLORS = {
    "Public": "#3D405B",
    "Privé": "#F2CC8F",
}

CATEGORY_COLORS = {
    "Information": "#3D405B",
    "Sport": "#E07A5F",
    "Généraliste": "#81B29A",
    "Documentaire / Découverte": "#F2CC8F",
    "Documentaire / Histoire": "#6D597A",
    "Animaux / Nature": "#A3B18A",
    "Voyage / Découverte": "#E9C46A",
    "Autre": "#B7B7A4",
}

VARIATION_COLORS = {
    "Hausse": "#F2CC8F",
    "Baisse": "#E07A5F",
}

CHAIN_COMPARE_COLORS = {
    "France 2": "#3D405B",
    "TF1": "#81B29A",
    "France 3": "#5E503F",
    "M6": "#E07A5F",
    "Arte": "#6D597A",
    "BFM TV": "#22333B",
    "LCI": "#A3B18A",
    "I-Télé/CNews": "#C6AC8F",
}

HEATMAP_SCALE = [
    "#E07A5F",
    "#F2CC8F",
    "#F4F1DE",
    "#81B29A",
    "#3D405B",
]


@st.cache_data
def load_data():

    # Certaines tables sont récupérées via l’API déployée.
    # En cas d’indisponibilité de l’API, un fallback CSV est utilisé.

    # Représentation femmes / hommes
    try:
        gender_year_channel = fetch_api_data("/gender/year-channel")
    except Exception:
        gender_year_channel = load_csv_fallback("tv_gender_by_year_channel.csv")

    try:
        gender_year_public_private = fetch_api_data("/gender/public-private")
    except Exception:
        gender_year_public_private = load_csv_fallback("tv_gender_by_year_public_private.csv")

    gender_year_category = load_csv_fallback("tv_gender_by_year_category.csv")
    gender_public_private_global = load_csv_fallback("tv_gender_public_private_global.csv")

    # Thématiques JT
    jt_year_channel_theme = load_csv_fallback("jt_topics_by_year_channel_theme.csv")

    try:
        jt_year_theme = fetch_api_data("/jt/topics/year-theme")
    except Exception:
        jt_year_theme = load_csv_fallback("jt_topics_by_year_theme.csv")

    jt_topics_global = load_csv_fallback("jt_topics_global.csv")
    jt_theme_volatility = load_csv_fallback("jt_theme_volatility.csv")

    # Croisement exploratoire thème × genre
    theme_gender_proxy = load_csv_fallback("theme_gender_proxy.csv")
    theme_gender_proxy_by_theme = load_csv_fallback("theme_gender_proxy_by_theme.csv")

    return (
        gender_year_channel,
        gender_year_public_private,
        gender_year_category,
        gender_public_private_global,
        jt_year_channel_theme,
        jt_year_theme,
        jt_topics_global,
        theme_gender_proxy,
        theme_gender_proxy_by_theme,
        jt_theme_volatility,
    )


def beautify_plot(fig, legend_orientation="h", right_margin=20):
    if legend_orientation == "h":
        legend_config = dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text="",
        )
    else:
        legend_config = dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            title_text="",
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Arial, sans-serif",
            size=14,
            color="#3D405B",
        ),
        margin=dict(l=20, r=right_margin, t=80, b=20),
        legend=legend_config,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_color="#3D405B",
            bordercolor="rgba(61,64,91,0.12)",
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=False,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(61,64,91,0.10)",
        gridwidth=1,
        zeroline=False,
        showline=False,
    )
    return fig