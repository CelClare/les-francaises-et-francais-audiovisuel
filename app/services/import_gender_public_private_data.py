from pathlib import Path
import pandas as pd
from sqlalchemy import text

from app.core.database import engine

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data" / "processed" / "tv_gender_by_year_public_private.csv"


def main() -> None:
    print("CSV_PATH =", CSV_PATH)
    print("DB_URL =", engine.url)

    df = pd.read_csv(CSV_PATH)
    print(df.head())
    print("Nombre de lignes CSV :", len(df))

    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE tv_gender_by_year_public_private RESTART IDENTITY;")
        )

    df.to_sql(
        "tv_gender_by_year_public_private",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"{len(df)} lignes importées dans tv_gender_by_year_public_private.")


if __name__ == "__main__":
    main()