import streamlit as st
import plotly.express as px

from utils import (
    inject_global_css,
    load_data,
    beautify_plot,
)

st.set_page_config(
    page_title="Genres de programmes et parole",
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

# =========================================================
# TITRE
# =========================================================
st.title("Genres de programmes : où la parole féminine apparaît-elle ?")

st.markdown(
    '<div class="subtitle">Cette page change de niveau d’analyse : au lieu d’un proxy, elle utilise un jeu de données mesurant directement la parole dans les programmes audiovisuels selon leur genre.</div>',
    unsafe_allow_html=True,
)

st.info(
    "Ici, la parole est mesurée directement (durée et taux d’expression), mais sans distinction du rôle des intervenant·es."
)

st.divider()

# =========================================================
# 1. PART FÉMININE PAR GENRE
# =========================================================
st.markdown(
    '<div class="section-title">Part de parole féminine selon le genre de programme</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-note">Chaque barre représente la part de parole féminine moyenne dans un type de programme audiovisuel.</div>',
    unsafe_allow_html=True,
)

latest_year = csa_program_genres["year"].max()

latest_data = csa_program_genres[
    csa_program_genres["year"] == latest_year
].copy()

latest_data = latest_data.sort_values("women_expression_rate")

fig_genre = px.bar(
    latest_data,
    x="women_expression_rate",
    y="program_genre",
    orientation="h",
    labels={
        "women_expression_rate": "Part de parole féminine",
        "program_genre": "Genre de programme",
    },
    title=f"Part de parole féminine par genre de programme ({latest_year})",
)

fig_genre.update_xaxes(tickformat=".0%")

fig_genre.update_traces(
    marker_color="#F2CC8F",
    texttemplate="%{x:.1%}",
    textposition="outside",
    cliponaxis=False,
)

fig_genre = beautify_plot(fig_genre)

fig_genre.update_layout(
    height=max(500, 28 * len(latest_data)),
)

st.plotly_chart(fig_genre, width="stretch")

st.divider()

# =========================================================
# 2. ÉVOLUTION 2019 → 2020
# =========================================================
st.markdown(
    '<div class="section-title">Évolution selon les genres de programmes</div>',
    unsafe_allow_html=True,
)

pivot = csa_program_genres.pivot(
    index="program_genre",
    columns="year",
    values="women_expression_rate",
)

pivot = pivot.dropna()

pivot["delta"] = pivot[2020] - pivot[2019]
pivot = pivot.sort_values("delta")

fig_delta = px.bar(
    pivot,
    x="delta",
    y=pivot.index,
    orientation="h",
    labels={
        "delta": "Variation de la part féminine",
        "y": "Genre de programme",
    },
    title="Évolution de la part de parole féminine entre 2019 et 2020",
)

fig_delta.update_xaxes(tickformat=".0%")

fig_delta.update_traces(
    marker_color="#E07A5F",
    texttemplate="%{x:.1%}",
    textposition="outside",
    cliponaxis=False,
)

fig_delta = beautify_plot(fig_delta)

st.plotly_chart(fig_delta, width="stretch")

st.divider()

# =========================================================
# 3. PAROLE GLOBALE VS PAROLE FÉMININE
# =========================================================
st.markdown(
    '<div class="section-title">Volume de parole et part féminine</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-note">Ce graphique met en relation le volume global de parole et la part de parole féminine selon les genres de programmes.</div>',
    unsafe_allow_html=True,
)

fig_scatter = px.scatter(
    latest_data,
    x="speech_rate",
    y="women_expression_rate",
    size="total_declarations_duration",
    hover_name="program_genre",
    labels={
        "speech_rate": "Taux de parole global",
        "women_expression_rate": "Part de parole féminine",
    },
    title="Relation entre volume de parole et part féminine",
)

fig_scatter.update_xaxes(tickformat=".0%")
fig_scatter.update_yaxes(tickformat=".0%")

fig_scatter.update_traces(
    marker=dict(
        color="#3D405B",
        opacity=0.8,
        line=dict(width=0.8, color="white"),
    )
)

fig_scatter = beautify_plot(fig_scatter)

st.plotly_chart(fig_scatter, width="stretch")

st.divider()

# =========================================================
# CONCLUSION
# =========================================================
st.markdown(
    """
    <div class="section-note">
    <strong>Lecture :</strong> la représentation femmes / hommes ne dépend pas uniquement des chaînes ou des thématiques,
    mais aussi du type de programme. Certains formats apparaissent plus favorables à la parole féminine, tandis que d’autres
    restent plus déséquilibrés.
    </div>
    """,
    unsafe_allow_html=True,
)