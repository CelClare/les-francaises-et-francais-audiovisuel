import streamlit as st
import plotly.express as px

from utils import (
    inject_global_css,
    load_data,
    beautify_plot,
    CHAIN_COMPARE_COLORS,
    HEATMAP_SCALE,
    PUBLIC_PRIVATE_COLORS
)

st.set_page_config(
    page_title="Comparer les écarts selon les chaînes",
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

st.title("Comparer les chaînes : des écarts structurels ?")

st.markdown(
    '<div class="subtitle">Après une première lecture globale, cette page observe comment les écarts de représentation femmes / hommes se traduisent à l’échelle de chaînes particulières.</div>',
    unsafe_allow_html=True,
)

st.info(
    "Un écart global peut masquer des situations très différentes selon les chaînes. "
    "Cette page permet d’observer quelles chaînes contribuent le plus aux déséquilibres, "
    "et lesquelles présentent des trajectoires plus favorables."
)

st.markdown(
    '<div class="subtitle">L’objectif n’est plus de décrire une tendance générale, mais de comparer des trajectoires particulières. Cette étape permet de voir si la lecture globale masque des profils de chaînes plus contrastés, ou au contraire confirme une dynamique plus générale.</div>',
    unsafe_allow_html=True,
)

st.divider()

public_channels = sorted(
    gender_year_channel.loc[
        gender_year_channel["is_public_channel"] == True, "channel_name"
    ].unique()
)

private_channels = sorted(
    gender_year_channel.loc[
        gender_year_channel["is_public_channel"] == False, "channel_name"
    ].unique()
)

with st.expander("Choisir les chaînes à comparer", expanded=True):
    col_a, col_b = st.columns(2)

    with col_a:
        selected_public_channels = st.multiselect(
            "Chaînes publiques",
            options=public_channels,
            default=["France 2"] if "France 2" in public_channels else public_channels[:1],
        )

    with col_b:
        selected_private_channels = st.multiselect(
            "Chaînes privées",
            options=private_channels,
            default=["TF1"] if "TF1" in private_channels else private_channels[:1],
        )

selected_compare_channels = selected_public_channels + selected_private_channels

filtered_compare = gender_year_channel.copy()
if selected_compare_channels:
    filtered_compare = filtered_compare[
        filtered_compare["channel_name"].isin(selected_compare_channels)
    ]

st.markdown(
    '<div class="section-title">Comment les chaînes se situent-elles ?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Cette vue permet de comparer des trajectoires particulières et de voir si la tendance globale masque des profils de chaînes plus contrastés.</div>',
    unsafe_allow_html=True,
)

n_selected = len(selected_compare_channels)

if n_selected == 0:
    st.info("Sélectionnez au moins une chaîne pour afficher la comparaison.")

else:
    if n_selected <= 4:
        fig_compare = px.line(
            filtered_compare,
            x="year",
            y="avg_female_share",
            color="channel_name",
            color_discrete_map=CHAIN_COMPARE_COLORS,
            markers=True,
            labels={
                "year": "Année",
                "avg_female_share": "Part féminine moyenne",
                "channel_name": "Chaîne",
            },
            title="Comparaison de chaînes publiques et privées sélectionnées",
        )

        fig_compare.update_yaxes(tickformat=".0%")

        fig_compare.update_xaxes(
            tickmode="array",
            tickvals=sorted(filtered_compare["year"].unique()),
            ticktext=[str(year) for year in sorted(filtered_compare["year"].unique())],
        )

        fig_compare.update_traces(
            line=dict(width=3),
            marker=dict(size=7),
            line_shape="spline",
        )
        fig_compare = beautify_plot(fig_compare)
        st.plotly_chart(fig_compare, width="stretch")

    else:
        heatmap_compare = filtered_compare.pivot(
            index="channel_name",
            columns="year",
            values="avg_female_share",
        )

        fig_compare_heatmap = px.imshow(
            heatmap_compare,
            aspect="auto",
            color_continuous_scale=HEATMAP_SCALE,
            labels={
                "x": "Année",
                "y": "Chaîne",
                "color": "Part féminine moyenne",
            },
            title="Heatmap de la part féminine moyenne des chaînes sélectionnées",
        )
        fig_compare_heatmap.update_coloraxes(colorbar_tickformat=".0%")

        fig_compare_heatmap.update_xaxes(
            tickmode="array",
            tickvals=sorted(filtered_compare["year"].unique()),
            ticktext=[str(year) for year in sorted(filtered_compare["year"].unique())],
        )

        fig_compare_heatmap.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Inter, Arial, sans-serif",
                size=14,
                color="#3D405B",
            ),
            margin=dict(l=20, r=20, t=80, b=20),
        )
        st.plotly_chart(fig_compare_heatmap, width="stretch")

    # =========================
    # KPI / REPÈRES DE LECTURE
    # =========================
    summary = (
        filtered_compare.sort_values(["channel_name", "year"])
        .groupby("channel_name")
        .agg(
            start_year=("year", "min"),
            end_year=("year", "max"),
        )
        .reset_index()
    )

    start_vals = (
        filtered_compare.merge(
            summary[["channel_name", "start_year"]],
            left_on=["channel_name", "year"],
            right_on=["channel_name", "start_year"],
            how="inner",
        )[["channel_name", "avg_female_share"]]
        .rename(columns={"avg_female_share": "start_value"})
    )

    end_vals = (
        filtered_compare.merge(
            summary[["channel_name", "end_year"]],
            left_on=["channel_name", "year"],
            right_on=["channel_name", "end_year"],
            how="inner",
        )[["channel_name", "avg_female_share"]]
        .rename(columns={"avg_female_share": "end_value"})
    )

    summary = (
        summary.merge(start_vals, on="channel_name", how="left")
        .merge(end_vals, on="channel_name", how="left")
    )
    summary["delta"] = summary["end_value"] - summary["start_value"]

    st.divider()

    st.markdown(
        '<div class="section-title">Repères de lecture</div>',
        unsafe_allow_html=True,
    )

    if len(summary) == 1:
        row = summary.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Chaîne sélectionnée",
            row["channel_name"],
        )

        col2.metric(
            "Niveau final",
            f"{row['end_value']:.1%}",
            delta_color="off",
        )

        col3.metric(
            "Variation sur la période",
            f"{row['delta']:.1%}",
            delta_color="off",
        )

        col4.metric(
            "Période observée",
            f"{int(row['start_year'])}–{int(row['end_year'])}",
            delta_color="off",
        )

        st.markdown(
            f"""
            <div class="section-note">
            <strong>Lecture rapide :</strong> la chaîne sélectionnée, <strong>{row['channel_name']}</strong>,
            atteint un niveau final de <strong>{row['end_value']:.1%}</strong> et évolue de
            <strong>{row['delta']:.1%}</strong> entre <strong>{int(row['start_year'])}</strong> et
            <strong>{int(row['end_year'])}</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        highest_end = summary.sort_values("end_value", ascending=False).iloc[0]
        lowest_end = summary.sort_values("end_value", ascending=True).iloc[0]
        biggest_progress = summary.sort_values("delta", ascending=False).iloc[0]
        biggest_decline = summary.sort_values("delta", ascending=True).iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Niveau final le plus élevé",
            highest_end["channel_name"],
            f"{highest_end['end_value']:.1%}",
            delta_color="off",
        )

        col2.metric(
            "Niveau final le plus faible",
            lowest_end["channel_name"],
            f"{lowest_end['end_value']:.1%}",
            delta_color="off",
        )

        col3.metric(
            "Hausse la plus marquée",
            biggest_progress["channel_name"],
            f"{biggest_progress['delta']:.1%}",
            delta_color="off",
        )

        col4.metric(
            "Baisse la plus marquée",
            biggest_decline["channel_name"],
            f"{biggest_decline['delta']:.1%}",
            delta_color="off",
        )

        st.markdown(
            f"""
            <div class="section-note">
            <strong>Lecture rapide :</strong> parmi les chaînes sélectionnées, <strong>{highest_end['channel_name']}</strong>
            atteint le niveau final le plus élevé ({highest_end['end_value']:.1%}), tandis que
            <strong>{lowest_end['channel_name']}</strong> se situe au niveau final le plus faible
            ({lowest_end['end_value']:.1%}). Sur la période observée, la hausse la plus marquée concerne
            <strong>{biggest_progress['channel_name']}</strong> ({biggest_progress['delta']:.1%}) et la baisse la plus marquée
            <strong>{biggest_decline['channel_name']}</strong> ({biggest_decline['delta']:.1%}).
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================
# CLASSEMENT FINAL DES CHAÎNES
# ============================

st.divider()

st.markdown(
    '<div class="section-title">Classement des chaînes en fin de période</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-note">Ce classement permet d’identifier rapidement les chaînes où la part féminine moyenne est la plus élevée ou la plus faible en fin de période.</div>',
    unsafe_allow_html=True,
)

latest_year = gender_year_channel["year"].max()

latest_ranking = (
    gender_year_channel[gender_year_channel["year"] == latest_year]
    .copy()
    .sort_values("avg_female_share", ascending=True)
)

latest_ranking["channel_type"] = latest_ranking["is_public_channel"].map(
    {True: "Public", False: "Privé"}
)

fig_ranking = px.bar(
    latest_ranking,
    x="avg_female_share",
    y="channel_name",
    orientation="h",
    color="channel_type",
    color_discrete_map=PUBLIC_PRIVATE_COLORS,
    labels={
        "avg_female_share": "Part féminine moyenne",
        "channel_name": "Chaîne",
        "is_public_channel": "Chaîne publique",
    },
    title=f"Classement des chaînes selon la part féminine moyenne en {latest_year}",
)

fig_ranking.update_xaxes(tickformat=".0%")

fig_ranking.update_traces(
    texttemplate="%{x:.1%}",
    textposition="outside",
    cliponaxis=False,
)

fig_ranking = beautify_plot(fig_ranking, legend_orientation="h")

fig_ranking.update_layout(
    height=max(650, 28 * len(latest_ranking)),
    margin=dict(l=140, r=80, t=80, b=40),
    showlegend=True,
)

st.plotly_chart(fig_ranking, width="stretch")
