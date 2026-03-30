from pathlib import Path

from app.pipelines.collect import load_stats, load_barometer_jt
from app.pipelines.clean import clean_stats, clean_barometer_jt
from app.pipelines.aggregate import (
    aggregate_gender_by_year_channel,
    aggregate_jt_topics_by_year_channel_theme,
)

BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # Collect
    stats_raw = load_stats()
    jt_raw = load_barometer_jt()

    # Clean
    stats_clean = clean_stats(stats_raw)
    jt_clean = clean_barometer_jt(jt_raw)

    # Aggregate
    gender_year_channel = aggregate_gender_by_year_channel(stats_clean)
    jt_year_channel_theme = aggregate_jt_topics_by_year_channel_theme(jt_clean)

    # Save
    stats_clean.to_csv(PROCESSED_DIR / "tv_gender_stats_clean.csv", index=False)
    jt_clean.to_csv(PROCESSED_DIR / "jt_topics_clean.csv", index=False)
    gender_year_channel.to_csv(PROCESSED_DIR / "tv_gender_by_year_channel.csv", index=False)
    jt_year_channel_theme.to_csv(PROCESSED_DIR / "jt_topics_by_year_channel_theme.csv", index=False)

    print("Pipeline terminé. Fichiers enregistrés dans data/processed.")


if __name__ == "__main__":
    main()