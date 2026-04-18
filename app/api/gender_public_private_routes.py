from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_api_key
from app.models.gender_public_private_model import TVGenderByYearPublicPrivate
from app.schemas.gender_public_private_schema import TVGenderByYearPublicPrivateRead

router = APIRouter()


@router.get(
    "/gender/public-private",
    response_model=list[TVGenderByYearPublicPrivateRead],
)
def read_gender_public_private(
    year: Optional[int] = None,
    is_public_channel: Optional[bool] = None,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key),
):
    query = db.query(TVGenderByYearPublicPrivate)

    if year is not None:
        query = query.filter(TVGenderByYearPublicPrivate.year == year)

    if is_public_channel is not None:
        query = query.filter(
            TVGenderByYearPublicPrivate.is_public_channel == is_public_channel
        )

    return query.all()