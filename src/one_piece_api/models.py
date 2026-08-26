from sqlalchemy.orm import Mapped, mapped_column 
from .database import Base 



class CharacterDB(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    crew: Mapped[str]
    devil_fruit: Mapped[str]


