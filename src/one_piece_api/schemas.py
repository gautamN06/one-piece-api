from pydantic import BaseModel 


class Character(BaseModel):
    name:str 
    age: int 
    affiliation: str
    crew: str | None = None
    devil_fruit: str | None = None
    devil_fruit_type: str | None = None
    bounty: int | None = None
    status: str 


