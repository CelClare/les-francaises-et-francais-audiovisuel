from sqlalchemy import Column, Integer, Float, Boolean
from app.core.database import Base


class TVGenderByYearPublicPrivate(Base):
    __tablename__ = "tv_gender_by_year_public_private"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    is_public_channel = Column(Boolean, nullable=False, index=True)

    avg_female_share = Column(Float, nullable=False)
    avg_male_share = Column(Float, nullable=False)
    total_female_duration = Column(Float, nullable=False)
    total_male_duration = Column(Float, nullable=False)
    n_obs = Column(Integer, nullable=False)