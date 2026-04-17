import streamlit as st
import plotly.express as px

from utils import (
    inject_global_css,
    load_data,
    beautify_plot,
)

st.set_page_config(
    page_title="Contextes thématiques des écarts",
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
) = load_data()

st.title("Dans quels contextes thématiques apparaissent les écarts ?")
st.markdown(
    '<div class="subtitle">Cette page n’analyse pas directement la représentation femmes / hommes : elle éclaire le contexte éditorial dans lequel ces écarts prennent forme, à travers les thématiques des journaux télévisés.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-note">Cette page s’appuie sur le baromètre thématique des journaux télévisés. Le périmètre est donc plus restreint que celui des pages précédentes et concerne uniquement les chaînes présentes dans ce jeu de données.</div>',
    unsafe_allow_html=True,
)

st.divider()

# =========================================================
# 1. VUE GLOBALE DES THÉMATIQUES SUR 2000–2020
# =========================================================
st.markdown(
    '<div class="section-title">Quels thèmes structurent les JT ?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Cette visualisation agrège les sujets sur toute la période 2000–2020. Elle permet d’identifier les thématiques structurellement les plus présentes dans les JT.</div>',
    unsafe_allow_html=True,
)

fig_top_themes = px.bar(
    jt_topics_global,
    x="theme",
    y="total_subjects_all_years",
    labels={
        "theme": "Thématique",
        "total_subjects_all_years": "Nombre total de sujets",
    },
    title="Nombre total de sujets par thématique sur 2000–2020",
)
fig_top_themes.update_traces(
    marker_color="#3D405B",
    marker_line_color="#3D405B",
    marker_line_width=0.5,
)
fig_top_themes = beautify_plot(fig_top_themes)
st.plotly_chart(fig_top_themes, width="stretch")

if len(jt_topics_global) >= 2:
    top_theme = jt_topics_global.iloc[0]
    second_theme = jt_topics_global.iloc[1]

    st.markdown(
        f"""
        <div class="section-note">
        <strong>Lecture rapide :</strong> sur l’ensemble de la période, la thématique la plus présente est
        <strong>{top_theme['theme']}</strong> ({int(top_theme['total_subjects_all_years'])} sujets),
        suivie de <strong>{second_theme['theme']}</strong>. Cette vue cumulative peut différer des impressions
        laissées par certaines années particulières ou par certains événements marquants.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# =========================================================
# 2. RÉPARTITION PAR CHAÎNE / ANNÉE
# =========================================================
st.markdown(
    '<div class="section-title">Quels thèmes dominent selon les chaînes et les années ?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Observer, pour une chaîne donnée et une année choisie, quelles thématiques dominent dans les journaux télévisés.</div>',
    unsafe_allow_html=True,
)

channels_topics = sorted(jt_year_channel_theme["channel_name"].unique())
selected_channel = st.selectbox(
    "Choisir une chaîne",
    options=channels_topics,
    index=0,
)

years = sorted(jt_year_channel_theme["year"].unique())
selected_year = st.selectbox(
    "Choisir une année",
    options=years,
    index=len(years) - 1,
)

filtered_topics = jt_year_channel_theme[
    (jt_year_channel_theme["channel_name"] == selected_channel)
    & (jt_year_channel_theme["year"] == selected_year)
].copy()

filtered_topics = filtered_topics.sort_values("total_subjects", ascending=False)

fig_topics = px.bar(
    filtered_topics,
    x="theme",
    y="total_subjects",
    labels={
        "theme": "Thématique",
        "total_subjects": "Nombre total de sujets",
    },
    title=f"Répartition des thématiques — {selected_channel} ({selected_year})",
)
fig_topics.update_traces(
    marker_color="#3D405B",
    marker_line_color="#3D405B",
    marker_line_width=0.5,
)
fig_topics = beautify_plot(fig_topics)
st.plotly_chart(fig_topics, width="stretch")

if not filtered_topics.empty:
    top_topic_local = filtered_topics.iloc[0]

    st.markdown(
        f"""
        <div class="section-note">
        <strong>Lecture rapide :</strong> pour <strong>{selected_channel}</strong> en <strong>{selected_year}</strong>,
        la thématique dominante est <strong>{top_topic_local['theme']}</strong>
        avec <strong>{int(top_topic_local['total_subjects'])}</strong> sujets. Cette lecture locale peut différer
        de la hiérarchie observée sur l’ensemble de la période.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# =========================================================
# 3. ÉVOLUTION D’UNE THÉMATIQUE DANS LE TEMPS
# =========================================================
st.markdown(
    '<div class="section-title">Comment une thématique évolue-t-elle dans le temps ?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Suivre l’évolution d’une thématique sur l’ensemble de la période observée.</div>',
    unsafe_allow_html=True,
)

themes = sorted(jt_year_theme["theme"].unique())
selected_theme = st.selectbox(
    "Choisir une thématique",
    options=themes,
    index=0,
)

filtered_theme = jt_year_theme[jt_year_theme["theme"] == selected_theme].copy()

fig_theme = px.line(
    filtered_theme,
    x="year",
    y="total_subjects",
    markers=True,
    labels={
        "year": "Année",
        "total_subjects": "Nombre total de sujets",
    },
    title=f"Évolution de la thématique : {selected_theme}",
)
fig_theme.update_traces(
    line=dict(width=3, color="#3D405B"),
    marker=dict(size=7, color="#3D405B"),
    line_shape="spline",
)
fig_theme = beautify_plot(fig_theme)
st.plotly_chart(fig_theme, width="stretch")

if not filtered_theme.empty:
    peak_row = filtered_theme.sort_values("total_subjects", ascending=False).iloc[0]
    min_row = filtered_theme.sort_values("total_subjects", ascending=True).iloc[0]

    st.markdown(
        f"""
        <div class="section-note">
        <strong>Lecture rapide :</strong> la thématique <strong>{selected_theme}</strong> atteint son niveau le plus élevé
        en <strong>{int(peak_row['year'])}</strong> avec <strong>{int(peak_row['total_subjects'])}</strong> sujets,
        tandis que son niveau le plus faible est observé en <strong>{int(min_row['year'])}</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# =========================================================
# 4. POINT D’INTERPRÉTATION
# =========================================================
st.markdown(
    '<div class="section-title">Pourquoi ce contexte éditorial compte-t-il ?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="section-note">
    La hiérarchie des thématiques dépend fortement de l’échelle d’observation. Une thématique peut apparaître très
    dominante dans une année particulière — par exemple dans un contexte exceptionnel comme 2020 — sans pour autant
    structurer l’ensemble de la période 2000–2020. Cette différence entre lecture ponctuelle et lecture cumulative
    est essentielle pour interpréter correctement les journaux télévisés.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# =========================================================
# 5. CE QUI RESTE, CE QUI FLUCTUE
# =========================================================
st.markdown(
    '<div class="section-title">Ce qui reste, ce qui fluctue</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Toutes les thématiques ne connaissent pas la même stabilité dans le temps. Certaines occupent une place relativement constante dans les JT, tandis que d’autres réagissent davantage au contexte historique, politique ou médiatique.</div>',
    unsafe_allow_html=True,
)

volatility_display = jt_theme_volatility.copy().sort_values(
    "coeff_variation", ascending=False
)

max_themes = min(12, len(volatility_display))
default_themes = min(8, max_themes) if max_themes >= 5 else max_themes

top_n_volatility = st.slider(
    "Nombre de thématiques à afficher",
    min_value=5 if max_themes >= 5 else 1,
    max_value=max_themes,
    value=default_themes,
)

volatility_display = volatility_display.head(top_n_volatility).sort_values(
    "coeff_variation", ascending=True
)

fig_volatility = px.bar(
    volatility_display,
    x="coeff_variation",
    y="theme",
    orientation="h",
    labels={
        "coeff_variation": "Indice de variabilité",
        "theme": "Thématique",
    },
    title="Thématiques les plus variables au fil du temps",
    text="coeff_variation",
)

fig_volatility.update_traces(
    marker_color="#3D405B",
    marker_line_color="#3D405B",
    marker_line_width=0.5,
    texttemplate="%{text:.2f}",
    textposition="outside",
)

fig_volatility = beautify_plot(fig_volatility)
st.plotly_chart(fig_volatility, width="stretch")

if not jt_theme_volatility.empty:
    most_variable = jt_theme_volatility.sort_values(
        "coeff_variation", ascending=False
    ).iloc[0]
    most_stable = jt_theme_volatility.sort_values(
        "coeff_variation", ascending=True
    ).iloc[0]

    st.markdown(
        f"""
        <div class="section-note">
        <strong>Lecture rapide :</strong> la thématique la plus variable sur la période est
        <strong>{most_variable['theme']}</strong>, tandis que <strong>{most_stable['theme']}</strong>
        apparaît comme la plus stable. Cela montre que certaines thématiques sont davantage
        sensibles au contexte, quand d’autres occupent une place plus régulière dans les journaux télévisés.
        </div>
        """,
        unsafe_allow_html=True,
    )