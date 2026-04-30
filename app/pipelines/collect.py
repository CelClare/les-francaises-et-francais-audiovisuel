from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

def load_stats() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "20190308-stats.csv")

def load_barometer_jt() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "ina-barometre-jt-tv-donnees-quotidiennes-2000-2020-nbre-sujets-durees-202410.csv",
        sep=";",
        encoding="latin1",
        header=None
    )

def load_csa_program_genres() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "ina-csa-parole-femmes-genreprogramme.csv")