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