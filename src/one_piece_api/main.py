from fastapi import FastAPI, HTTPException 
from .database import SessionLocal, engine, Base 
from .models import CharacterDB
from .schemas import Character 

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/character")
def get_characters():
    db = SessionLocal()
    characters=db.query(CharacterDB).all()
    db.close()

    return characters 

@app.get("/characters/{character_id}")
def get_character(character_id: int):
    db = SessionLocal()
    character = db.query(CharacterDB).filter(
        CharacterDB.id == character_id
    ).first()
    db.close()

    if character is None:
        raise HTTPException(
            status_code=404,
            detail="Character not found!:("
        )

    return character 



@app.post("/characters")
def create_character(character: Character):
    db = SessionLocal()
    new_character = CharacterDB(
        name=character.name,
        age=character.age,
        crew=character.crew,
        devil_fruit=character.devil_fruit
    )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    db.close()

    return new_character 

@app.put("/characters/{character_id}")
def update_character(character_id: int, character: Character):
    db = SessionLocal()

    db_character = db.query(CharacterDB).filter(
        CharacterDB.id == character_id
    ).first()

    if db_character is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Character not found :("
        )

    db_character.name = character.name
    db_character.age = character.age 
    db_character.crew = character.crew
    db_character.devil_fruit = character.devil_fruit 

    db.commit()
    db.refresh(db_character)
    db.close() 

    return db_character 



@app.delete("/characters/{character_id}")
def delete_character(character_id: int):
    db = SessionLocal()
    db_character = db.query(CharacterDB).filter(
        CharacterDB.id == character_id 
    ).first()

    if db_character is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Character not found :("
        )

    db.delete(db_character)
    db.commit()
    db.close()

    return{
        "message":f"{db_character.name} was deleted!"
    }
    

