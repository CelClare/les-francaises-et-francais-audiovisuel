from pydantic import BaseModel


class TVGenderByYearPublicPrivateRead(BaseModel):
    id: int
    year: int
    is_public_channel: bool
    avg_female_share: float
    avg_male_share: float
    total_female_duration: float
    total_male_duration: float
    n_obs: int

    class Config:
        from_attributes = True