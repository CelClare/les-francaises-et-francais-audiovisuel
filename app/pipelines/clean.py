import pandas as pd
import numpy as np

def clean_stats(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["media_type"] == "tv"].copy()

    # On garde uniquement les colonnes d’intérêt pour le pipeline, et on calcule les indicateurs de part de parole féminine et masculine
    df["date"] = pd.to_datetime(df["date"])
    df["total_gender_duration"] = df["male_duration"] + df["female_duration"]

    df["female_share"] = np.where(
        df["total_gender_duration"] > 0,
        df["female_duration"] / df["total_gender_duration"],
        np.nan,
    )
    df["male_share"] = np.where(
        df["total_gender_duration"] > 0,
        df["male_duration"] / df["total_gender_duration"],
        np.nan,
    )

    CHANNEL_CATEGORY_MAP = {
    "BFM TV": "Information",
    "LCI": "Information",
    "I-Télé/CNews": "Information",
    "Euronews": "Information",
    "France 24": "Information",
    "Canal+ Sport": "Sport",
    "L'Equipe 21": "Sport",
    "Eurosport France": "Sport",
    "Animaux": "Animaux / Nature",
    "Chasse et pêche": "Animaux / Nature",
    "Voyage": "Voyage / Découverte",
    "Planète+": "Documentaire / Découverte",
    "Toute l'Histoire": "Documentaire / Histoire",
    "Histoire": "Documentaire / Histoire",
    "TF1": "Généraliste",
    "France 2": "Généraliste",
    "France 3": "Généraliste",
    "France 5": "Généraliste",
    "M6": "Généraliste",
    "W9": "Généraliste",
    "Monte Carlo TMC": "Généraliste",
    "Canal+": "Généraliste",
    "Chérie 25": "Généraliste",
    "NRJ 12": "Généraliste",
    "France O": "Généraliste",
    "TV Breizh": "Généraliste",
    "La chaîne Météo": "Information",
}

    df["channel_category"] = df["channel_name"].map(CHANNEL_CATEGORY_MAP).fillna("Autre")
    columns_to_keep = [
        "channel_code",
        "channel_name",
        "is_public_channel",
        "date",
        "week_day",
        "hour",
        "male_duration",
        "female_duration",
        "music_duration",
        "total_gender_duration",
        "female_share",
        "male_share",
        "channel_category",
    ]

    return df[columns_to_keep]


def clean_barometer_jt(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = ["date", "channel_name", "empty_col", "theme", "nb_subjects", "duration"]
    df = df.drop(columns=["empty_col"])

    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df["nb_subjects"] = df["nb_subjects"].astype(int)
    df["duration"] = df["duration"].astype(int)

    return df