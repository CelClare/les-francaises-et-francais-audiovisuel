import pandas as pd


def aggregate_gender_by_year_channel(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    temp["year"] = temp["date"].dt.year

    return (
        temp.groupby(["year", "channel_name", "is_public_channel"], as_index=False)
        .agg(
            avg_female_share=("female_share", "mean"),
            avg_male_share=("male_share", "mean"),
            total_female_duration=("female_duration", "sum"),
            total_male_duration=("male_duration", "sum"),
            n_obs=("date", "count"),
        )
    )


def aggregate_jt_topics_by_year_channel_theme(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    temp["year"] = temp["date"].dt.year

    return (
        temp.groupby(["year", "channel_name", "theme"], as_index=False)
        .agg(
            total_subjects=("nb_subjects", "sum"),
            total_duration=("duration", "sum"),
            n_days=("date", "nunique"),
        )
    )

def aggregate_gender_by_year_public_private(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    temp["year"] = temp["date"].dt.year

    return (
        temp.groupby(["year", "is_public_channel"], as_index=False)
        .agg(
            avg_female_share=("female_share", "mean"),
            avg_male_share=("male_share", "mean"),
            total_female_duration=("female_duration", "sum"),
            total_male_duration=("male_duration", "sum"),
            n_obs=("date", "count"),
        )
    )   

def aggregate_jt_topics_by_year_theme(df: pd.DataFrame) -> pd.DataFrame:
     temp = df.copy()
     temp["year"] = temp["date"].dt.year

     return (
         temp.groupby(["year", "theme"], as_index=False)
         .agg(
             total_subjects=("nb_subjects", "sum"),
             total_duration=("duration", "sum"),
             n_days=("date", "nunique"),
         )
     )

def aggregate_gender_by_year_category(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    temp["year"] = temp["date"].dt.year

    return (
        temp.groupby(["year", "channel_category"], as_index=False)
        .agg(
            avg_female_share=("female_share", "mean"),
            avg_male_share=("male_share", "mean"),
            total_female_duration=("female_duration", "sum"),
            total_male_duration=("male_duration", "sum"),
            n_obs=("date", "count"),
        )
    )

def aggregate_gender_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["channel_category"], as_index=False)
        .agg(
            avg_female_share=("female_share", "mean"),
            avg_male_share=("male_share", "mean"),
            total_female_duration=("female_duration", "sum"),
            total_male_duration=("male_duration", "sum"),
            n_obs=("date", "count"),
        )
    )

def aggregate_jt_topics_global(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège les thématiques des JT sur toute la période.
    Utile pour la page 3 : vue globale 2000–2020.
    """
    return (
        df.groupby("theme", as_index=False)
        .agg(
            total_subjects_all_years=("nb_subjects", "sum"),
            total_duration_all_years=("duration", "sum"),
            n_days_all_years=("date", "nunique"),
        )
        .sort_values("total_subjects_all_years", ascending=False)
    )


def aggregate_gender_public_private_global(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège la représentation femmes / hommes sur toute la période
    par type de chaîne (public / privé).
    Utile pour la page 3 : mise en regard visuelle cohérente.
    """
    return (
        df.groupby("is_public_channel", as_index=False)
        .agg(
            avg_female_share_all_years=("female_share", "mean"),
            avg_male_share_all_years=("male_share", "mean"),
            total_female_duration_all_years=("female_duration", "sum"),
            total_male_duration_all_years=("male_duration", "sum"),
            n_obs=("date", "count"),
        )
    )


def aggregate_theme_gender_proxy(
    gender_year_channel_df: pd.DataFrame,
    jt_year_channel_theme_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Croisement exploratoire thème × genre au niveau chaîne × année.

    On calcule la part d’un thème dans un JT (theme_share),
    puis on la joint à la part féminine moyenne de la même chaîne et année.

    Utile pour la page 4 : analyse exploratoire, sans prétendre mesurer
    directement le temps de parole femmes / hommes à l’intérieur de chaque sujet.
    """
    topic_totals = (
        jt_year_channel_theme_df.groupby(["year", "channel_name"], as_index=False)
        .agg(total_subjects_all_themes=("total_subjects", "sum"))
    )

    proxy = jt_year_channel_theme_df.merge(
        topic_totals,
        on=["year", "channel_name"],
        how="left",
    )

    proxy["theme_share"] = (
        proxy["total_subjects"] / proxy["total_subjects_all_themes"]
    )

    proxy = proxy.merge(
        gender_year_channel_df[
            ["year", "channel_name", "avg_female_share", "avg_male_share"]
        ],
        on=["year", "channel_name"],
        how="inner",
    )

    return proxy.sort_values(["theme", "year", "channel_name"])


def aggregate_theme_gender_proxy_by_theme(proxy_df: pd.DataFrame) -> pd.DataFrame:
    """
    Version simplifiée du proxy, agrégée par thématique.
    Utile pour résumer les tendances exploratoires en page 4.
    """
    return (
        proxy_df.groupby("theme", as_index=False)
        .agg(
            avg_theme_share=("theme_share", "mean"),
            avg_female_share=("avg_female_share", "mean"),
            avg_male_share=("avg_male_share", "mean"),
            n_points=("channel_name", "count"),
        )
        .sort_values("avg_theme_share", ascending=False)
    )

def aggregate_jt_theme_volatility(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()

    volatility = (
        df.groupby("theme", as_index=False)
        .agg(
            mean_subjects=("total_subjects", "mean"),
            std_subjects=("total_subjects", "std"),
            min_subjects=("total_subjects", "min"),
            max_subjects=("total_subjects", "max"),
            n_years=("year", "count"),
        )
    )

    volatility["coeff_variation"] = (
        volatility["std_subjects"] / volatility["mean_subjects"]
    )

    return volatility.sort_values("coeff_variation", ascending=False)
