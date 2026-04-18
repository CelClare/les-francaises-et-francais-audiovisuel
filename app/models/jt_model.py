from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class JTTopicByYearTheme(Base):
    __tablename__ = "jt_topics_by_year_theme"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    theme = Column(String, nullable=False, index=True)

    total_subjects = Column(Integer, nullable=False)
    total_duration = Column(Float, nullable=False)
    n_days = Column(Integer, nullable=False)