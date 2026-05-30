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

highest = latest_data.iloc[-1]
lowest = latest_data.iloc[0]

st.markdown(
    f"""
    <div class="section-note">
    <strong>À retenir :</strong> en {latest_year},
    <strong>{highest['program_genre']}</strong> présente la part de parole féminine la plus élevée
    ({highest['women_expression_rate']:.1%}),
    tandis que <strong>{lowest['program_genre']}</strong> présente la plus faible
    ({lowest['women_expression_rate']:.1%}).
    Les écarts observés montrent que tous les genres de programmes ne donnent pas la même visibilité à la parole féminine.
    </div>
    """,
    unsafe_allow_html=True,
)

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

best = pivot.sort_values("delta", ascending=False).iloc[0]
worst = pivot.sort_values("delta", ascending=True).iloc[0]

st.markdown(
    f"""
    <div class="section-note">
    <strong>À retenir :</strong>
    entre 2019 et 2020, la plus forte progression de la part féminine est observée pour
    <strong>{best.name}</strong> ({best['delta']:.1%}),
    tandis que la plus forte baisse concerne
    <strong>{worst.name}</strong> ({worst['delta']:.1%}).
    Ces évolutions montrent que les écarts de représentation ne sont pas figés et peuvent évoluer rapidement selon les contextes audiovisuels.
    </div>
    """,
    unsafe_allow_html=True,
)

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

corr = latest_data["speech_rate"].corr(
    latest_data["women_expression_rate"]
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

if corr > 0.3:
    interpretation = (
        "Les genres de programmes où la parole occupe une place importante "
        "tendent également à présenter davantage de parole féminine."
    )
elif corr < -0.3:
    interpretation = (
        "Les genres de programmes les plus bavards "
        "sont aussi ceux où la parole féminine est la plus faible."
    )
else:
    interpretation = (
        "Aucune relation nette n'apparaît entre le volume global de parole "
        "et la part de parole féminine."
    )

col1, col2 = st.columns([1, 3])

with col1:
    st.metric(
        "Corrélation",
        f"{corr:.2f}",
    )

with col2:
    st.info(interpretation)

st.divider()

# =========================================================
# CONCLUSION
# =========================================================

st.markdown(
    """
    <div class="section-note">
    <strong>Conclusion :</strong>
    les écarts de représentation observés ne dépendent pas uniquement des chaînes
    ou des thématiques. Les genres de programmes apparaissent eux aussi associés
    à des niveaux très différents de parole féminine. Certains formats s'approchent
    davantage de l'équilibre tandis que d'autres restent largement dominés par la parole masculine.
    Cette observation suggère que la forme des programmes joue probablement un rôle important
    dans la visibilité des femmes à l'écran.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-note">
    <strong>Question suivante :</strong>
    ces différences s'expliquent-elles uniquement par les thématiques et les formats des programmes,
    ou existe-t-il d'autres facteurs plus fins liés aux contenus eux-mêmes ?
    La page suivante teste une première hypothèse statistique à partir de la composition thématique des JT.
    </div>
    """,
    unsafe_allow_html=True,
)