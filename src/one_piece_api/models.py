from sqlalchemy.orm import Mapped, mapped_column 
from .database import Base 



class CharacterDB(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    affiliation: Mapped[str]
    crew: Mapped[str | None]
    devil_fruit: Mapped[str | None]
    devil_fruit_type: Mapped[str | None]
    bounty: Mapped[int | None]
    status: Mapped[str]



