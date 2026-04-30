import streamlit as st
import plotly.express as px

from utils import (
    inject_global_css,
    load_page1_data,
    beautify_plot,
    PUBLIC_PRIVATE_COLORS,
    VARIATION_COLORS,
    HEATMAP_SCALE
)

st.set_page_config(
    page_title="Mesurer le temps de parole femmes / hommes",
    layout="wide",
)

inject_global_css()

(
    gender_year_channel,
    gender_year_public_private,
    gender_year_category,
    gender_by_hour,
) = load_page1_data()

st.title("Mesurer le temps de parole femmes / hommes")

st.markdown(
    '<div class="subtitle">Cette page pose le premier constat : les femmes disposent d’un temps de parole inférieur à celui des hommes à la télévision, avec des écarts qui varient selon les années, les chaînes et les catégories éditoriales.</div>',
    unsafe_allow_html=True,
)

st.info(
    "Présence, parole et autorité ne se confondent pas : cette page mesure la parole, les pages suivantes interrogent les contextes dans lesquels cette parole apparaît."
)

st.markdown(
    '<div class="subtitle">Le temps de parole permet de mesurer une inégalité quantitative. Mais il ne dit pas encore si les femmes parlent comme journalistes, expertes, invitées politiques, témoins ou anonymes.</div>',
    unsafe_allow_html=True,
)

st.divider()

# =========================
# MÉTRIQUES DE SYNTHÈSE
# =========================
global_avg = gender_year_channel["avg_female_share"].mean()

latest_year = gender_year_public_private["year"].max()
latest_public_private = gender_year_public_private[
    gender_year_public_private["year"] == latest_year
].copy()

latest_public_private["channel_type"] = latest_public_private["is_public_channel"].map(
    {True: "Public", False: "Privé"}
)

public_val = latest_public_private.loc[
    latest_public_private["channel_type"] == "Public", "avg_female_share"
].values[0]

private_val = latest_public_private.loc[
    latest_public_private["channel_type"] == "Privé", "avg_female_share"
].values[0]

gap = public_val - private_val

category_variation_base = (
    gender_year_category.sort_values(["channel_category", "year"])
    .groupby("channel_category")
    .agg(
        start_year=("year", "min"),
        end_year=("year", "max"),
    )
    .reset_index()
)

start_values = (
    gender_year_category.merge(
        category_variation_base[["channel_category", "start_year"]],
        left_on=["channel_category", "year"],
        right_on=["channel_category", "start_year"],
        how="inner",
    )[["channel_category", "avg_female_share"]]
    .rename(columns={"avg_female_share": "start_value"})
)

end_values = (
    gender_year_category.merge(
        category_variation_base[["channel_category", "end_year"]],
        left_on=["channel_category", "year"],
        right_on=["channel_category", "end_year"],
        how="inner",
    )[["channel_category", "avg_female_share"]]
    .rename(columns={"avg_female_share": "end_value"})
)

category_variation_base = (
    category_variation_base
    .merge(start_values, on="channel_category", how="left")
    .merge(end_values, on="channel_category", how="left")
)

category_variation_base["delta"] = (
    category_variation_base["end_value"] - category_variation_base["start_value"]
)

strongest_decline = (
    category_variation_base[
        category_variation_base["channel_category"] != "Autre"
    ]
    .sort_values("delta")
    .iloc[0]
)

col1, col2, col3 = st.columns(3)

col1.metric("Part féminine moyenne globale", f"{global_avg:.1%}")
col2.metric("Écart public / privé en fin de période", f"{gap:.1%}")
col3.metric(
    "Catégorie en plus forte baisse",
    strongest_decline["channel_category"],
    f"{strongest_decline['delta']:.1%}",
)

st.divider()

# =========================
# PUBLIC VS PRIVÉ
# =========================
st.markdown(
    '<div class="section-title">Vue d’ensemble : chaînes publiques et privées</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-note">Cette visualisation agrège l’ensemble des chaînes publiques d’un côté et privées de l’autre. Elle donne une tendance globale, et non une comparaison entre chaînes individuelles.</div>',
    unsafe_allow_html=True,
)

gender_year_public_private_plot = gender_year_public_private.copy()
gender_year_public_private_plot["channel_type"] = gender_year_public_private_plot[
    "is_public_channel"
].map({True: "Public", False: "Privé"})

fig_public_private = px.line(
    gender_year_public_private_plot,
    x="year",
    y="avg_female_share",
    color="channel_type",
    color_discrete_map=PUBLIC_PRIVATE_COLORS,
    markers=True,
    labels={
        "year": "Année",
        "avg_female_share": "Part féminine moyenne",
        "channel_type": "Type de chaîne",
    },
    title="Évolution de la part féminine moyenne : public vs privé",
)

fig_public_private.update_yaxes(tickformat=".0%")
fig_public_private.update_xaxes(
    tickmode="array",
    tickvals=sorted(gender_year_public_private_plot["year"].unique()),
    ticktext=[str(year) for year in sorted(gender_year_public_private_plot["year"].unique())],
)

fig_public_private.update_traces(
    line=dict(width=4),
    marker=dict(size=8),
    line_shape="spline",
)

fig_public_private = beautify_plot(fig_public_private)
st.plotly_chart(fig_public_private, width="stretch")

st.divider()

# =========================
# HEURE DE DIFFUSION
# =========================
st.markdown(
    '<div class="section-title">À quelles heures les femmes parlent-elles le plus ?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-note">Cette visualisation observe la part féminine moyenne selon l’heure de diffusion. Elle permet de questionner les écarts entre moments de forte audience et autres créneaux.</div>',
    unsafe_allow_html=True,
)

fig_hour = px.line(
    gender_by_hour,
    x="hour",
    y="avg_female_share",
    markers=True,
    labels={
        "hour": "Heure de diffusion",
        "avg_female_share": "Part féminine moyenne",
    },
    title="Part féminine moyenne selon l’heure de diffusion",
)

fig_hour.update_yaxes(tickformat=".0%")

fig_hour.update_xaxes(
    tickmode="array",
    tickvals=sorted(gender_by_hour["hour"].unique()),
    ticktext=[str(hour) for hour in sorted(gender_by_hour["hour"].unique())],
)

fig_hour.update_traces(
    line=dict(width=4, color="#E07A5F"),
    marker=dict(size=8, color="#E07A5F"),
    line_shape="spline",
)

fig_hour = beautify_plot(fig_hour)
st.plotly_chart(fig_hour, width="stretch")

st.markdown(
    """
    <div class="section-note">
    <strong>Point d’attention :</strong> les heures de diffusion ne disent pas seulement quand les femmes parlent.
    Elles permettent aussi d’interroger la visibilité de cette parole aux moments les plus exposés.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# =========================
# HEATMAP PAR CATÉGORIE
# =========================
st.markdown(
    '<div class="section-title">Lecture par catégories éditoriales</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-note">Cette lecture ne correspond pas directement à l’opposition public / privé. Elle permet plutôt d’identifier des univers de programmation plus ou moins favorables à la représentation féminine.</div>',
    unsafe_allow_html=True,
)

categories = sorted(gender_year_category["channel_category"].unique())

with st.expander("Choisir les catégories à afficher", expanded=False):
    selected_categories = st.multiselect(
        "Catégories",
        options=categories,
        default=categories,
    )

filtered_category_year = gender_year_category.copy()

if selected_categories:
    filtered_category_year = filtered_category_year[
        filtered_category_year["channel_category"].isin(selected_categories)
    ]

heatmap_data = filtered_category_year.pivot(
    index="channel_category",
    columns="year",
    values="avg_female_share",
)

fig_category_heatmap = px.imshow(
    heatmap_data,
    aspect="auto",
    color_continuous_scale=HEATMAP_SCALE,
    labels={
        "x": "Année",
        "y": "Catégorie de chaîne",
        "color": "Part féminine moyenne",
    },
    title="Heatmap de la part féminine moyenne par catégorie de chaîne",
)

fig_category_heatmap.update_coloraxes(colorbar_tickformat=".0%")
fig_category_heatmap.update_xaxes(
    tickmode="array",
    tickvals=sorted(filtered_category_year["year"].unique()),
    ticktext=[str(year) for year in sorted(filtered_category_year["year"].unique())],
)

fig_category_heatmap.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Inter, Arial, sans-serif",
        size=14,
        color="#3D405B",
    ),
    margin=dict(l=20, r=20, t=80, b=20),
)

st.plotly_chart(fig_category_heatmap, width="stretch")

st.divider()

# =========================
# VARIATION 2010-2019
# =========================
st.markdown(
    '<div class="section-title">Qui monte, qui baisse, entre 2010 et 2019 ?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-note">Cette visualisation montre la variation entre le début et la fin de période par catégorie, afin de mieux repérer les progressions, stagnations et régressions.</div>',
    unsafe_allow_html=True,
)

category_variation = category_variation_base.copy()
category_variation["direction"] = category_variation["delta"].apply(
    lambda x: "Hausse" if x >= 0 else "Baisse"
)

show_other = st.checkbox("Inclure la catégorie « Autre »", value=False)

variation_chart = category_variation.copy()

if not show_other:
    variation_chart = variation_chart[
        variation_chart["channel_category"] != "Autre"
    ]

variation_chart = variation_chart.sort_values("delta", ascending=True)

fig_variation = px.bar(
    variation_chart,
    x="delta",
    y="channel_category",
    orientation="h",
    color="direction",
    color_discrete_map=VARIATION_COLORS,
    labels={
        "delta": "Variation de la part féminine moyenne",
        "channel_category": "Catégorie de chaîne",
        "direction": "Tendance",
    },
    title="Variation de la part féminine moyenne entre 2010 et 2019 par catégorie",
    text="delta",
)

fig_variation.update_xaxes(tickformat=".0%")
fig_variation.update_traces(
    texttemplate="%{text:.1%}",
    textposition="outside",
)

fig_variation = beautify_plot(fig_variation)
st.plotly_chart(fig_variation, width="stretch")

if not variation_chart.empty:
    biggest_drop = variation_chart.sort_values("delta").iloc[0]
    biggest_gain = variation_chart.sort_values("delta", ascending=False).iloc[0]

    st.markdown(
        f"""
        <div class="section-note">
        <strong>Lecture rapide :</strong> la catégorie la plus en baisse est <strong>{biggest_drop['channel_category']}</strong>
        ({biggest_drop['delta']:.1%}), tandis que la plus forte progression observée concerne
        <strong>{biggest_gain['channel_category']}</strong> ({biggest_gain['delta']:.1%}).
        </div>
        """,
        unsafe_allow_html=True,
    )