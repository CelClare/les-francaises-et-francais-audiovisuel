from app.core.database import engine, Base
from app.models.gender_model import TVGenderByYearChannel
from app.models.jt_model import JTTopicByYearTheme
from app.models.gender_public_private_model import TVGenderByYearPublicPrivate

Base.metadata.create_all(bind=engine)
print("Tables créées.")