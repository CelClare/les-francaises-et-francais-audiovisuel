import streamlit as st
import plotly.express as px

from utils import (
    inject_global_css,
    load_data,
    beautify_plot,
    CHAIN_COMPARE_COLORS,
)

st.set_page_config(
    page_title="Thématiques et représentation",
    layout="wide",
)

inject_global_css()

(
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
    jt_editorial_composition,
    gender_by_hour,
    csa_program_genres,
) = load_data()

st.title("Mettre en regard thèmes et temps de parole")

st.markdown(
    '<div class="subtitle">Cette page explore une hypothèse : certains contextes thématiques peuvent être associés à des niveaux différents de représentation femmes / hommes. Le croisement proposé reste indirect : il met en regard le poids d’un thème dans les JT et la part féminine moyenne d’une chaîne sur une année.</div>',
    unsafe_allow_html=True,
)

st.info(
    "Important : ce graphique ne mesure pas la part de parole féminine à l’intérieur de chaque sujet. "
    "Il observe seulement si, pour une chaîne et une année données, le poids d’une thématique varie avec la part féminine moyenne globale."
)

st.divider()

# =========================================================
# 1. CROISEMENT EXPLORATOIRE THÈME × GENRE
# =========================================================
st.markdown(
    '<div class="section-title">Thématique choisie et représentation moyenne</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Chaque point correspond à une combinaison chaîne × année. Il ne s’agit pas d’une mesure directe du temps de parole femmes / hommes à l’intérieur des sujets, mais d’une mise en regard exploratoire entre contexte thématique et représentation moyenne.</div>',
    unsafe_allow_html=True,
)

themes_proxy = sorted(theme_gender_proxy["theme"].dropna().unique())
selected_proxy_theme = st.selectbox(
    "Choisir une thématique à explorer",
    options=themes_proxy,
    index=0,
)

proxy_filtered = theme_gender_proxy[
    theme_gender_proxy["theme"] == selected_proxy_theme
].copy()

proxy_filtered = proxy_filtered.dropna(
    subset=["theme_share", "avg_female_share", "total_subjects", "channel_name", "year"]
)

# On limite la palette aux chaînes présentes
channels_present = proxy_filtered["channel_name"].dropna().unique().tolist()
channel_colors = {
    channel: CHAIN_COMPARE_COLORS[channel]
    for channel in channels_present
    if channel in CHAIN_COMPARE_COLORS
}

fig_proxy = px.scatter(
    proxy_filtered,
    x="theme_share",
    y="avg_female_share",
    color="channel_name",
    size="total_subjects",
    size_max=26,
    color_discrete_map=channel_colors,
    hover_data={
        "year": True,
        "channel_name": True,
        "total_subjects": True,
        "theme_share": ":.1%",
        "avg_female_share": ":.1%",
    },
    labels={
        "theme_share": "Poids de la thématique dans le JT",
        "avg_female_share": "Part féminine moyenne",
        "channel_name": "Chaîne",
        "total_subjects": "Nombre de sujets",
    },
    title=f"Association exploratoire — {selected_proxy_theme}",
)

fig_proxy.update_traces(
    marker=dict(
        opacity=0.82,
        line=dict(width=0.8, color="white"),
    )
)

fig_proxy.update_xaxes(tickformat=".0%")
fig_proxy.update_yaxes(tickformat=".0%")
fig_proxy = beautify_plot(fig_proxy, legend_orientation="v", right_margin=170)
fig_proxy.update_layout(height=650)
st.plotly_chart(fig_proxy, width="stretch")

selected_theme_summary_df = theme_gender_proxy_by_theme[
    theme_gender_proxy_by_theme["theme"] == selected_proxy_theme
]

if selected_theme_summary_df.empty:
    st.warning("Aucune donnée synthétique disponible pour cette thématique.")
    st.stop()

selected_theme_summary = selected_theme_summary_df.iloc[0]

female_share_range = (
    proxy_filtered["avg_female_share"].max() - proxy_filtered["avg_female_share"].min()
    if not proxy_filtered.empty
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Poids moyen du thème",
    f"{selected_theme_summary['avg_theme_share']:.1%}",
    delta_color="off",
)
col2.metric(
    "Part féminine moyenne observée",
    f"{selected_theme_summary['avg_female_share']:.1%}",
    delta_color="off",
)
col3.metric(
    "Nombre de contextes observés",
    f"{int(selected_theme_summary['n_points'])}",
    delta_color="off",
)
col4.metric(
    "Amplitude observée",
    f"{female_share_range:.1%}",
    delta_color="off",
)

st.divider()

# =========================================================
# 3. CE QUE CETTE EXPLORATION PERMET — ET NE PERMET PAS ENCORE
# =========================================================
st.markdown(
    '<div class="section-title">Ce que cette exploration permet</div>',
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(
        """
        <div style="background:white; padding:18px; border-radius:18px; border:1px solid rgba(61,64,91,0.08); min-height:210px;">
            <div style="font-weight:700; font-size:1.05rem; color:#3D405B; margin-bottom:0.7rem;">Ce que l’on observe</div>
            <div style="color:#5E503F; line-height:1.7;">
                • des écarts de représentation selon les contextes éditoriaux<br>
                • des hiérarchies thématiques différentes selon l’échelle d’observation<br>
                • des associations possibles entre poids d’un thème et représentation moyenne
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        """
        <div style="background:white; padding:18px; border-radius:18px; border:1px solid rgba(61,64,91,0.08); min-height:210px;">
            <div style="font-weight:700; font-size:1.05rem; color:#3D405B; margin-bottom:0.7rem;">Ce que l’on ne peut pas conclure</div>
            <div style="color:#5E503F; line-height:1.7;">
                • qu’un thème est directement “féminin” ou “masculin”<br>
                • que les femmes parlent davantage à l’intérieur d’un sujet précis<br>
                • qu’une relation causale existe entre thème traité et temps de parole
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_c:
    st.markdown(
        """
        <div style="background:white; padding:18px; border-radius:18px; border:1px solid rgba(61,64,91,0.08); min-height:210px;">
            <div style="font-weight:700; font-size:1.05rem; color:#3D405B; margin-bottom:0.7rem;">Pistes d’amélioration</div>
            <div style="color:#5E503F; line-height:1.7;">
                • accéder à une granularité plus fine au niveau du sujet<br>
                • relier thème, segment audiovisuel et temps de parole<br>
                • enrichir l’analyse avec audio, transcription ou segmentation automatique
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    """
    <div class="section-note">
    <strong>Conclusion :</strong> cette page montre les limites d’un croisement indirect entre thèmes des JT et part féminine moyenne.
    Pour aller plus loin, la page suivante mobilise un autre jeu de données : les genres de programmes, qui permettent
    d’approcher plus directement les contextes dans lesquels la parole féminine est mesurée.
    </div>
    """,
    unsafe_allow_html=True,
)