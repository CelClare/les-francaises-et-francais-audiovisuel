from pathlib import Path

from app.pipelines.collect import load_stats, load_barometer_jt
from app.pipelines.clean import clean_stats, clean_barometer_jt
from app.pipelines.aggregate import (
    aggregate_gender_by_year_channel,
    aggregate_jt_topics_by_year_channel_theme,
    aggregate_gender_by_year_public_private,
    aggregate_jt_topics_by_year_theme,
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
    # Agrégations à partir de 20190308-stats.csv
    gender_year_channel = aggregate_gender_by_year_channel(stats_clean)
    gender_year_public_private = aggregate_gender_by_year_public_private(stats_clean)

    # Agrégations à partir du baromètre JT
    jt_year_channel_theme = aggregate_jt_topics_by_year_channel_theme(jt_clean)
    jt_year_theme = aggregate_jt_topics_by_year_theme(jt_clean)

    # Save
    # Sauvegarde des tables nettoyées
    stats_clean.to_csv(PROCESSED_DIR / "tv_gender_stats_clean.csv", index=False)
    jt_clean.to_csv(PROCESSED_DIR / "jt_topics_clean.csv", index=False)

    # Sauvegarde des tables agrégées issues de 20190308-stats.csv
    gender_year_channel.to_csv(PROCESSED_DIR / "tv_gender_by_year_channel.csv", index=False)
    gender_year_public_private.to_csv(
        PROCESSED_DIR / "tv_gender_by_year_public_private.csv", index=False
    )

    # Sauvegarde des tables agrégées issues du baromètre JT
    jt_year_channel_theme.to_csv(PROCESSED_DIR / "jt_topics_by_year_channel_theme.csv", index=False)
    jt_year_theme.to_csv(PROCESSED_DIR / "jt_topics_by_year_theme.csv", index=False)

    print("Pipeline terminé. Fichiers enregistrés dans data/processed.")


if __name__ == "__main__":
    main()