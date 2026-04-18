from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_api_key
from app.models.gender_model import TVGenderByYearChannel
from app.schemas.gender_schema import TVGenderByYearChannelRead

router = APIRouter()


@router.get("/gender/year-channel", response_model=list[TVGenderByYearChannelRead])
def read_gender_year_channel(
    year: Optional[int] = None,
    channel_name: Optional[str] = None,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key),
):
    query = db.query(TVGenderByYearChannel)

    if year is not None:
        query = query.filter(TVGenderByYearChannel.year == year)

    if channel_name is not None:
        query = query.filter(TVGenderByYearChannel.channel_name == channel_name)

    return query.all()