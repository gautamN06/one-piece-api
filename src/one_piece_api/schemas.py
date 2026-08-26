from pydantic import BaseModel 


class Character(BaseModel):
    name:str 
    age: int 
    crew: str 
    devil_fruit: str


