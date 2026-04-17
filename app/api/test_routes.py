from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.test_model import TestItem
from app.schemas.test_schema import TestItemCreate, TestItemRead

router = APIRouter()

@router.post("/test-items", response_model=TestItemRead)
def create_test_item(item: TestItemCreate, db: Session = Depends(get_db)):
    db_item = TestItem(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/test-items", response_model=list[TestItemRead])
def read_test_items(db: Session = Depends(get_db)):
    return db.query(TestItem).all()