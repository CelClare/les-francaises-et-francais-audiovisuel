from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.gender_model import TVGenderByYearChannel
from app.schemas.gender_schema import TVGenderByYearChannelRead

router = APIRouter()


@router.get("/gender/year-channel", response_model=list[TVGenderByYearChannelRead])
def read_gender_year_channel(db: Session = Depends(get_db)):
    return db.query(TVGenderByYearChannel).all()