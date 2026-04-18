from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_api_key
from app.models.jt_model import JTTopicByYearTheme
from app.schemas.jt_schema import JTTopicByYearThemeRead

router = APIRouter()


@router.get("/jt/topics/year-theme", response_model=list[JTTopicByYearThemeRead])
def read_jt_topics_by_year_theme(
    year: Optional[int] = None,
    theme: Optional[str] = None,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key),
):
    query = db.query(JTTopicByYearTheme)

    if year is not None:
        query = query.filter(JTTopicByYearTheme.year == year)

    if theme is not None:
        query = query.filter(JTTopicByYearTheme.theme == theme)

    return query.all()