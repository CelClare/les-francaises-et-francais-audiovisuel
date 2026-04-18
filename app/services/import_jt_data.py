from pathlib import Path
import pandas as pd
from sqlalchemy import text

from app.core.database import engine

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data" / "processed" / "jt_topics_by_year_theme.csv"


def main() -> None:
    print("CSV_PATH =", CSV_PATH)
    print("DB_URL =", engine.url)

    df = pd.read_csv(CSV_PATH)
    print(df.head())
    print("Nombre de lignes CSV :", len(df))

    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE jt_topics_by_year_theme RESTART IDENTITY;"))

    df.to_sql(
        "jt_topics_by_year_theme",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"{len(df)} lignes importées dans jt_topics_by_year_theme.")


if __name__ == "__main__":
    main()