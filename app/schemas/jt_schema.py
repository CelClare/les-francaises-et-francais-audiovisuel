from pydantic import BaseModel


class JTTopicByYearThemeRead(BaseModel):
    id: int
    year: int
    theme: str
    total_subjects: int
    total_duration: float
    n_days: int

    class Config:
        from_attributes = True