from app.core.database import engine, Base
from app.models.gender_model import TVGenderByYearChannel
from app.models.jt_model import JTTopicByYearTheme

Base.metadata.create_all(bind=engine)
print("Tables créées.")