from pathlib import Path

from app.pipelines.collect import load_stats, load_barometer_jt
from app.pipelines.clean import clean_stats, clean_barometer_jt
from app.pipelines.aggregate import (
    aggregate_gender_by_year_channel,
    aggregate_jt_topics_by_year_channel_theme,
    aggregate_gender_by_year_public_private,
    aggregate_jt_topics_by_year_theme,
    aggregate_gender_by_year_category,
    aggregate_gender_by_category,
    aggregate_jt_topics_global,
    aggregate_gender_public_private_global,
    aggregate_theme_gender_proxy,
    aggregate_theme_gender_proxy_by_theme,
    aggregate_jt_theme_volatility,
)

BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # Collect
    stats_raw = load_stats()
    jt_raw = load_barometer_jt()

    # Clean
    # Source 1 : 20190308-stats.csv -> représentation femmes / hommes à la TV
    stats_clean = clean_stats(stats_raw)

    # Source 2 : baromètre JT -> thématiques des journaux télévisés
    jt_clean = clean_barometer_jt(jt_raw)

    # Aggregate
    # ---------------------------------------------------------
    # Agrégations issues de 20190308-stats.csv
    # ---------------------------------------------------------
    gender_year_channel = aggregate_gender_by_year_channel(stats_clean)
    gender_year_public_private = aggregate_gender_by_year_public_private(stats_clean)
    gender_year_category = aggregate_gender_by_year_category(stats_clean)
    gender_category = aggregate_gender_by_category(stats_clean)
    gender_public_private_global = aggregate_gender_public_private_global(stats_clean)

    # ---------------------------------------------------------
    # Agrégations issues du baromètre JT
    # ---------------------------------------------------------
    jt_year_channel_theme = aggregate_jt_topics_by_year_channel_theme(jt_clean)
    jt_year_theme = aggregate_jt_topics_by_year_theme(jt_clean)
    jt_topics_global = aggregate_jt_topics_global(jt_clean)

    jt_theme_volatility = aggregate_jt_theme_volatility(jt_year_theme)

    # ---------------------------------------------------------
    # Croisement exploratoire thème × genre
    # Sources intermédiaires :
    # - gender_year_channel (issu de 20190308-stats.csv)
    # - jt_year_channel_theme (issu du baromètre JT)
    # ---------------------------------------------------------
    theme_gender_proxy = aggregate_theme_gender_proxy(
        gender_year_channel,
        jt_year_channel_theme,
    )
    theme_gender_proxy_by_theme = aggregate_theme_gender_proxy_by_theme(
        theme_gender_proxy
    )

    # Save
    # ---------------------------------------------------------
    # Sauvegarde des tables nettoyées
    # ---------------------------------------------------------
    stats_clean.to_csv(PROCESSED_DIR / "tv_gender_stats_clean.csv", index=False)
    jt_clean.to_csv(PROCESSED_DIR / "jt_topics_clean.csv", index=False)

    # ---------------------------------------------------------
    # Sauvegarde des tables agrégées issues de 20190308-stats.csv
    # ---------------------------------------------------------
    gender_year_channel.to_csv(
        PROCESSED_DIR / "tv_gender_by_year_channel.csv", index=False
    )
    gender_year_public_private.to_csv(
        PROCESSED_DIR / "tv_gender_by_year_public_private.csv", index=False
    )
    gender_year_category.to_csv(
        PROCESSED_DIR / "tv_gender_by_year_category.csv", index=False
    )
    gender_category.to_csv(
        PROCESSED_DIR / "tv_gender_by_category.csv", index=False
    )
    gender_public_private_global.to_csv(
        PROCESSED_DIR / "tv_gender_public_private_global.csv", index=False
    )

    # ---------------------------------------------------------
    # Sauvegarde des tables agrégées issues du baromètre JT
    # ---------------------------------------------------------
    jt_year_channel_theme.to_csv(
        PROCESSED_DIR / "jt_topics_by_year_channel_theme.csv", index=False
    )
    jt_year_theme.to_csv(
        PROCESSED_DIR / "jt_topics_by_year_theme.csv", index=False
    )
    jt_topics_global.to_csv(
        PROCESSED_DIR / "jt_topics_global.csv", index=False
    )
    jt_theme_volatility.to_csv(
        PROCESSED_DIR / "jt_theme_volatility.csv", index=False
    )

    # ---------------------------------------------------------
    # Sauvegarde des tables du croisement exploratoire thème × genre
    # ---------------------------------------------------------
    theme_gender_proxy.to_csv(
        PROCESSED_DIR / "theme_gender_proxy.csv", index=False
    )
    theme_gender_proxy_by_theme.to_csv(
        PROCESSED_DIR / "theme_gender_proxy_by_theme.csv", index=False
    )

    print("Pipeline terminé. Fichiers enregistrés dans data/processed.")


if __name__ == "__main__":
    main()