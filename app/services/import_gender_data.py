from pathlib import Path
import pandas as pd
from sqlalchemy import text

from app.core.database import engine

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data" / "processed" / "tv_gender_by_year_channel.csv"


def main() -> None:
    df = pd.read_csv(CSV_PATH)

    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE tv_gender_by_year_channel RESTART IDENTITY;"))

    df.to_sql(
        "tv_gender_by_year_channel",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"{len(df)} lignes importées dans tv_gender_by_year_channel.")


if __name__ == "__main__":
    main()